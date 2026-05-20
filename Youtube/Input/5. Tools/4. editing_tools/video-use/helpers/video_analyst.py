"""Video analysis tool — detect visual events aligned to transcript.

Two use cases:
  1. Own video: pass path to {project_id}_cut_final.mp4 — transcript auto-resolved.
  2. Reference video: pass a YouTube URL or a local file.

Usage:
    python video_analyst.py path/to/video.mp4
    python video_analyst.py "https://youtube.com/watch?v=..."
    python video_analyst.py path/to/video.mp4 --transcript path/to/t.json
    python video_analyst.py path/to/video.mp4 --output /out/dir
    python video_analyst.py path/to/video.mp4 --detect scene,motion,zoom
    python video_analyst.py path/to/video.mp4 --sample-rate 2.0 --chunk-minutes 5

Outputs (written to --output dir or same dir as video):
    {stem}_analysis.json   — full event list + summary stats (machine-readable)
    {stem}_analysis.md     — human-readable timeline grouped by minute
    {stem}_timeline.png    — filmstrip + waveform + color-coded event lane

Optional deps (tool runs without them, detectors are skipped with a hint):
    text detection: brew install tesseract && pip install pytesseract
    face detection: pip install opencv-python-headless
    YouTube download: brew install yt-dlp
"""

from __future__ import annotations

import argparse
import bisect
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

# ── Optional deps ──────────────────────────────────────────────────────────

try:
    from tqdm import tqdm as _tqdm
    _HAS_TQDM = True
except ImportError:
    _HAS_TQDM = False

try:
    import pytesseract as _tess
    from PIL import ImageFilter as _ImageFilter
    _HAS_OCR = True
except ImportError:
    _HAS_OCR = False

try:
    import cv2 as _cv2
    _HAS_CV2 = True
except ImportError:
    _HAS_CV2 = False


def _progress(items: list, desc: str = "") -> list:
    if _HAS_TQDM:
        return _tqdm(items, desc=desc, leave=True)
    print(f"  {desc}: {len(items)} chunk(s)...", flush=True)
    return items


# ── Constants ──────────────────────────────────────────────────────────────

CACHE_DIR   = Path.home() / ".claude" / "video_analyst_cache"
HELPERS_DIR = Path(__file__).resolve().parent

BG   = (18,  18,  22)
FG   = (235, 235, 235)
DIM  = (110, 110, 120)
WAVE = (140, 180, 255)

EVENT_COLORS: dict[str, tuple[int, int, int]] = {
    "scene_change":   (220,  50,  50),
    "zoom_in":        ( 50, 200, 100),
    "zoom_out":       ( 50, 180, 200),
    "text_overlay":   (220, 200,  50),
    "screen_content": ( 80, 120, 220),
    "motion_high":    (220, 140,  50),
    "face_visible":   (180, 120, 220),
}

# Row assignment in the event lane (0 = top, 3 = bottom)
_EVENT_ROW: dict[str, int] = {
    "scene_change":   0,
    "zoom_in":        1,
    "zoom_out":       1,
    "text_overlay":   2,
    "screen_content": 2,
    "motion_high":    3,
    "face_visible":   3,
}


# ── Data structures ────────────────────────────────────────────────────────

@dataclass
class FrameStat:
    timestamp: float
    scd_score: float = 0.0
    y_avg:     float = 128.0
    sat_avg:   float = 0.0
    y_dif:     float = 0.0
    y_min:     float = 0.0
    y_max:     float = 255.0
    bit_depth: int   = 8

    @property
    def y_avg_norm(self) -> float:
        return self.y_avg / ((2 ** self.bit_depth) - 1)

    @property
    def sat_avg_norm(self) -> float:
        return self.sat_avg / ((2 ** self.bit_depth) - 1)

    @property
    def y_dif_norm(self) -> float:
        return self.y_dif / ((2 ** self.bit_depth) - 1)


def _event(ts: float, etype: str, dur: float = 0.0,
           conf: float = 1.0, **props) -> dict:
    return {
        "id": 0,
        "timestamp": round(ts, 3),
        "type": etype,
        "duration": round(max(dur, 0.0), 3),
        "confidence": round(max(0.0, min(conf, 1.0)), 3),
        "properties": props,
        "transcript_context": None,
    }


# ── API key ────────────────────────────────────────────────────────────────

def _load_api_key() -> str:
    search = [
        HELPERS_DIR.parent / ".env",
        Path.home() / ".claude" / ".env",
        Path(".env"),
    ]
    for p in search:
        if p.exists():
            for line in p.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == "ELEVENLABS_API_KEY":
                    return v.strip().strip('"').strip("'")
    v = os.environ.get("ELEVENLABS_API_KEY", "")
    if not v:
        raise RuntimeError("ELEVENLABS_API_KEY not found in .env files or environment")
    return v


# ── VideoProbe ─────────────────────────────────────────────────────────────

class VideoProbe:
    @staticmethod
    def probe(path: Path) -> dict:
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,r_frame_rate:format=duration",
            "-of", "json", str(path),
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(r.stdout)
        streams = data.get("streams", [{}])
        fmt     = data.get("format", {})

        width  = int(streams[0].get("width",  1920)) if streams else 1920
        height = int(streams[0].get("height", 1080)) if streams else 1080

        fps_str = (streams[0].get("r_frame_rate", "30/1")) if streams else "30/1"
        try:
            n, d = fps_str.split("/")
            fps = float(n) / float(d)
        except Exception:
            fps = 30.0

        duration = float(fmt.get("duration", 0.0))
        return {"path": str(path), "duration": duration, "fps": fps,
                "resolution": [width, height]}


# ── VideoDownloader ────────────────────────────────────────────────────────

class VideoDownloader:
    @staticmethod
    def is_url(s: str) -> bool:
        return s.startswith("http://") or s.startswith("https://")

    @staticmethod
    def download(url: str) -> Path:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        # Get video info
        info_cmd = [
            "yt-dlp",
            "--print", "%(id)s",
            "--print", "%(title)s",
            "--print", "%(duration)s",
            "--no-playlist", url,
        ]
        try:
            r = subprocess.run(info_cmd, capture_output=True, text=True, check=True)
            lines = [l.strip() for l in r.stdout.strip().splitlines() if l.strip()]
            video_id = lines[0] if lines else "unknown"
            title    = lines[1] if len(lines) > 1 else "unknown"
            duration = lines[2] if len(lines) > 2 else "?"
        except subprocess.CalledProcessError:
            raise RuntimeError(
                "yt-dlp failed — install with: brew install yt-dlp"
            )
        except FileNotFoundError:
            raise RuntimeError(
                "yt-dlp not found — install with: brew install yt-dlp"
            )

        out_path = CACHE_DIR / f"{video_id}.mp4"
        if out_path.exists():
            print(f"cached: {title} ({video_id}.mp4)")
            return out_path

        print(f"downloading: {title} (~{duration}s)")
        dl_cmd = [
            "yt-dlp",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best",
            "--merge-output-format", "mp4",
            "--no-playlist",
            "-o", str(CACHE_DIR / f"{video_id}.%(ext)s"),
            url,
        ]
        subprocess.run(dl_cmd, check=True)

        if out_path.exists():
            return out_path

        candidates = sorted(CACHE_DIR.glob(f"{video_id}.*"))
        if candidates:
            candidates[0].rename(out_path)
            return out_path

        raise RuntimeError(f"yt-dlp download failed for {url}")


# ── TranscriptLoader ───────────────────────────────────────────────────────

class TranscriptLoader:
    def resolve(
        self,
        video: Path,
        transcript_arg: Path | None,
        output_dir: Path,
    ) -> tuple[dict | None, str]:
        """Return (transcript_dict, source_label).

        source_label: 'provided' | 'cached' | 'elevenlabs' | 'none'
        """
        if transcript_arg is not None:
            data = json.loads(transcript_arg.read_text())
            print(f"transcript: {transcript_arg.name} (provided)")
            return data, "provided"

        # Derive project_id by stripping common suffixes
        stem = video.stem
        project_id = stem
        for suffix in ("_cut_final", "_cut", "_overlaid", "_final"):
            if stem.endswith(suffix):
                project_id = stem[: -len(suffix)]
                break

        candidates = [
            video.parent / f"{project_id}_transcript.json",
            video.parent / f"{stem}_transcript.json",
            video.parent / "transcripts" / f"{project_id}.json",
            video.parent / "transcripts" / f"{stem}.json",
            video.parent / "edit" / "transcripts" / f"{stem}.json",
            output_dir / f"{stem}_transcript.json",
            output_dir / "transcripts" / f"{stem}.json",
        ]
        for c in candidates:
            if c.exists():
                data = json.loads(c.read_text())
                print(f"transcript: {c.name} (cached)")
                return data, "cached"

        print("no transcript found — transcribing with ElevenLabs Scribe...")
        try:
            api_key = _load_api_key()
        except RuntimeError as e:
            print(f"  warning: {e}")
            print("  analysis will run without transcript alignment")
            return None, "none"

        sys.path.insert(0, str(HELPERS_DIR))
        from transcribe import transcribe_one  # noqa: PLC0415

        out = transcribe_one(
            video=video,
            edit_dir=output_dir,
            api_key=api_key,
            verbose=True,
        )
        data = json.loads(out.read_text())

        # Cache a flat sibling copy next to the video
        sibling = video.parent / f"{project_id}_transcript.json"
        if not sibling.exists():
            sibling.write_text(json.dumps(data, indent=2))
            print(f"  cached: {sibling.name}")

        return data, "elevenlabs"


# ── TranscriptAligner ──────────────────────────────────────────────────────

_SENT_END_RE = re.compile(r"[.!?]$")


class TranscriptAligner:
    def __init__(self, words: list[dict]):
        self.words  = [w for w in words if w.get("type") == "word"]
        self._starts = [w["start"] for w in self.words]

    # -- lookup ---

    def find_word_at(self, timestamp: float) -> dict | None:
        if not self.words:
            return None
        idx = max(0, bisect.bisect_right(self._starts, timestamp) - 1)
        return self.words[idx]

    def _word_index(self, word: dict) -> int:
        try:
            return self._starts.index(word["start"])
        except ValueError:
            return 0

    def find_sentence_around(self, word_idx: int) -> tuple[str, float, float]:
        if not self.words:
            return "", 0.0, 0.0
        start_i = word_idx
        for i in range(word_idx - 1, -1, -1):
            if _SENT_END_RE.search((self.words[i].get("text") or "").strip()):
                break
            start_i = i
        end_i = word_idx
        for i in range(word_idx, len(self.words)):
            end_i = i
            if _SENT_END_RE.search((self.words[i].get("text") or "").strip()):
                break
        sentence = " ".join(
            (w.get("text") or "").strip()
            for w in self.words[start_i : end_i + 1]
        )
        s_start = self.words[start_i].get("start", 0.0)
        s_end   = self.words[end_i].get("end", s_start)
        return sentence, s_start, s_end

    def context_at(self, timestamp: float) -> dict | None:
        w = self.find_word_at(timestamp)
        if w is None:
            return None
        idx = self._word_index(w)
        sentence, s_start, s_end = self.find_sentence_around(idx)
        dur = w.get("end", w["start"]) - w["start"]
        return {
            "word":           (w.get("text") or "").strip(),
            "word_start":     round(w["start"], 3),
            "sentence":       sentence,
            "sentence_start": round(s_start, 3),
            "sentence_end":   round(s_end, 3),
            "is_emphasis_word": dur >= 0.12,
        }

    # -- stats ---

    def alignment_stats(self, events: list[dict]) -> dict:
        if not self.words or not events:
            return {}

        overlay_types = {"text_overlay", "screen_content"}
        zoom_types    = {"zoom_in", "zoom_out"}

        overlays = [e for e in events if e["type"] in overlay_types]
        zooms    = [e for e in events if e["type"] in zoom_types]

        def _at_emphasis(ts: float) -> bool:
            ctx = self.context_at(ts)
            return bool(ctx and ctx["is_emphasis_word"])

        def _near_sent_end(ts: float, window: float = 0.5) -> bool:
            for w in self.words:
                if (_SENT_END_RE.search((w.get("text") or "").strip())
                        and abs(w.get("end", 0) - ts) <= window):
                    return True
            return False

        oe = sum(1 for e in overlays if _at_emphasis(e["timestamp"]))
        ze = sum(1 for e in zooms    if _near_sent_end(e["timestamp"]))

        return {
            "overlays_during_key_words": round(oe / max(len(overlays), 1), 3),
            "zooms_at_sentence_end":     round(ze / max(len(zooms),    1), 3),
        }


# ── FfmpegPassDetector ─────────────────────────────────────────────────────

class FfmpegPassDetector:
    """Single ffmpeg filter pass per chunk: scene changes, motion, screen content."""

    SCD_THRESHOLD    = 0.3
    MOTION_THRESHOLD = 0.025   # normalized YDIF (out of 1.0)
    SCREEN_SAT_MAX   = 0.06    # screen recordings: low saturation
    SCREEN_Y_MIN     = 0.55    # screen recordings: bright background
    SCREEN_STATIC    = 0.008   # screen recordings: nearly no frame diff

    def run_chunk(
        self, video: Path, chunk_start: float, chunk_end: float, sample_rate: float
    ) -> list[FrameStat]:
        duration = chunk_end - chunk_start
        fps = max(0.5, min(sample_rate, 4.0))

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            meta_path = Path(f.name)

        try:
            cmd = [
                "ffmpeg", "-y", "-hide_banner", "-nostats",
                "-ss", f"{chunk_start:.3f}",
                "-i", str(video),
                "-t", f"{duration:.3f}",
                "-vf", (
                    f"fps={fps:.3f},"
                    "scdet=threshold=0.3:sc_pass=1,"
                    "signalstats,"
                    f"metadata=print:file={meta_path}"
                ),
                "-an", "-f", "null", "-",
            ]
            subprocess.run(
                cmd, check=True,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            return self._parse_meta(meta_path, chunk_start)
        except subprocess.CalledProcessError:
            return []
        finally:
            meta_path.unlink(missing_ok=True)

    @staticmethod
    def _parse_value(line: str) -> float | None:
        try:
            return float(line.rsplit("=", 1)[1])
        except (ValueError, IndexError):
            return None

    def _parse_meta(self, path: Path, chunk_start: float) -> list[FrameStat]:
        stats: list[FrameStat] = []
        cur: dict = {}

        with open(path) as f:
            for raw in f:
                line = raw.strip()
                if not line:
                    continue

                if line.startswith("frame:"):
                    if cur:
                        stats.append(self._build_stat(cur))
                    m = re.search(r"pts_time:([\d.]+)", line)
                    pts = float(m.group(1)) if m else 0.0
                    cur = {
                        "timestamp": round(pts + chunk_start, 3),
                        "scd_score": 0.0,
                        "y_avg":     128.0,
                        "sat_avg":   0.0,
                        "y_dif":     0.0,
                        "y_min":     0.0,
                        "y_max":     255.0,
                        "bit_depth": 8,
                    }
                    continue

                v = self._parse_value(line)
                if v is None:
                    continue

                if   "lavfi.scd.score"            in line: cur["scd_score"] = v
                elif "lavfi.signalstats.YAVG"     in line: cur["y_avg"]     = v
                elif "lavfi.signalstats.SATAVG"   in line: cur["sat_avg"]   = v
                elif "lavfi.signalstats.YDIF"     in line: cur["y_dif"]     = v
                elif "lavfi.signalstats.YMIN"     in line: cur["y_min"]     = v
                elif "lavfi.signalstats.YMAX"     in line: cur["y_max"]     = v
                elif "lavfi.signalstats.YBITDEPTH" in line: cur["bit_depth"] = int(v)

        if cur:
            stats.append(self._build_stat(cur))

        return stats

    @staticmethod
    def _build_stat(d: dict) -> FrameStat:
        return FrameStat(
            timestamp = d["timestamp"],
            scd_score = d["scd_score"],
            y_avg     = d["y_avg"],
            sat_avg   = d["sat_avg"],
            y_dif     = d["y_dif"],
            y_min     = d["y_min"],
            y_max     = d["y_max"],
            bit_depth = d["bit_depth"],
        )

    # -- detectors ---

    def detect_scene_changes(self, stats: list[FrameStat]) -> list[dict]:
        events: list[dict] = []
        i = 0
        while i < len(stats):
            s = stats[i]
            if s.scd_score < self.SCD_THRESHOLD:
                i += 1
                continue
            # Look ahead to distinguish hard cut vs dissolve
            window = stats[i : min(i + 8, len(stats))]
            above  = [x for x in window if x.scd_score >= self.SCD_THRESHOLD]
            if len(above) >= 3:
                kind = "dissolve"
                dur  = above[-1].timestamp - above[0].timestamp
                conf = min(s.scd_score / 8.0, 1.0)
                events.append(_event(s.timestamp, "scene_change", dur, conf,
                                     kind=kind, scd_score=round(s.scd_score, 2)))
                i += len(above)
            else:
                events.append(_event(s.timestamp, "scene_change", 0.0,
                                     min(s.scd_score / 8.0, 1.0),
                                     kind="cut", scd_score=round(s.scd_score, 2)))
                i += 1
        return events

    def detect_motion_high(
        self, stats: list[FrameStat], scene_times: set[float]
    ) -> list[dict]:
        events: list[dict] = []
        run_start: float | None = None
        run_end: float = 0.0

        for s in stats:
            near_cut = any(abs(s.timestamp - t) < 0.7 for t in scene_times)
            if s.y_dif_norm > self.MOTION_THRESHOLD and not near_cut:
                if run_start is None:
                    run_start = s.timestamp
                run_end = s.timestamp
            else:
                if run_start is not None and (run_end - run_start) >= 0.4:
                    events.append(_event(run_start, "motion_high",
                                         run_end - run_start, 0.7))
                run_start = None

        if run_start is not None and (run_end - run_start) >= 0.4:
            events.append(_event(run_start, "motion_high",
                                  run_end - run_start, 0.7))
        return events

    def detect_screen_content(self, stats: list[FrameStat]) -> list[dict]:
        events: list[dict] = []
        run_start: float | None = None
        run_end: float = 0.0

        for s in stats:
            is_screen = (
                s.sat_avg_norm < self.SCREEN_SAT_MAX
                and s.y_avg_norm  > self.SCREEN_Y_MIN
                and s.y_dif_norm  < self.SCREEN_STATIC
            )
            if is_screen:
                if run_start is None:
                    run_start = s.timestamp
                run_end = s.timestamp
            else:
                if run_start is not None and (run_end - run_start) >= 2.0:
                    events.append(_event(run_start, "screen_content",
                                          run_end - run_start, 0.8))
                run_start = None

        if run_start is not None and (run_end - run_start) >= 2.0:
            events.append(_event(run_start, "screen_content",
                                  run_end - run_start, 0.8))
        return events

    def run_and_detect(
        self,
        video: Path,
        chunk_start: float,
        chunk_end: float,
        sample_rate: float,
        detect: set[str],
    ) -> tuple[list[dict], list[FrameStat]]:
        stats = self.run_chunk(video, chunk_start, chunk_end, sample_rate)
        events: list[dict] = []

        scene_times: set[float] = set()
        if "scene" in detect:
            sc = self.detect_scene_changes(stats)
            scene_times = {e["timestamp"] for e in sc}
            events.extend(sc)

        if "motion" in detect:
            events.extend(self.detect_motion_high(stats, scene_times))

        if "screen" in detect:
            events.extend(self.detect_screen_content(stats))

        return events, stats


# ── ZoomDetector ───────────────────────────────────────────────────────────

class ZoomDetector:
    """Detect zoom-in / zoom-out events via numpy 3×3 zone frame-pair analysis.

    Zoom-in signature: corners of frame change more than center — the subject
    expands, pushing the background edges off-screen.
    Zoom-out signature: center changes more than corners — the background
    floods in around a shrinking subject.
    """

    ZI_THRESHOLD = 0.22   # (corner_diff - center_diff) / (corner + center)
    ZO_THRESHOLD = 0.18   # (center_diff - corner_diff) / (corner + center)
    MIN_DIFF     = 4.0    # absolute pixel diff floor (out of 255)
    MERGE_GAP    = 1.5    # seconds — merge consecutive same-type detections

    def run_chunk(
        self,
        video: Path,
        chunk_start: float,
        chunk_end: float,
        sample_rate: float,
        scene_times: set[float],
    ) -> list[dict]:
        fps = min(sample_rate * 2, 4.0)   # 2× sample rate, capped at 4fps
        duration = chunk_end - chunk_start

        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            cmd = [
                "ffmpeg", "-y", "-hide_banner", "-nostats",
                "-ss", f"{chunk_start:.3f}",
                "-i", str(video),
                "-t", f"{duration:.3f}",
                "-vf", f"fps={fps:.3f},scale=320:-2",
                "-f", "image2", "-q:v", "6",
                str(tmp_dir / "f%05d.jpg"),
            ]
            try:
                subprocess.run(
                    cmd, check=True,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            except subprocess.CalledProcessError:
                return []

            frames = sorted(tmp_dir.glob("f*.jpg"))
            if len(frames) < 2:
                return []

            step = 1.0 / fps
            arrays: list[tuple[float, np.ndarray]] = []
            for i, fp in enumerate(frames):
                ts  = round(chunk_start + i * step, 3)
                arr = np.array(Image.open(fp).convert("L"), dtype=np.float32)
                arrays.append((ts, arr))

            raw: list[tuple[float, str, float]] = []
            for i in range(len(arrays) - 1):
                ts, a1 = arrays[i]
                _,  a2 = arrays[i + 1]
                if any(abs(ts - st) < 0.8 for st in scene_times):
                    continue
                etype, conf = self._classify_pair(a1, a2)
                if etype:
                    raw.append((ts, etype, conf))

        return self._merge_raw(raw)

    @staticmethod
    def _classify_pair(a1: np.ndarray, a2: np.ndarray) -> tuple[str | None, float]:
        h, w = a1.shape
        ys = [0, h // 3, 2 * h // 3, h]
        xs = [0, w // 3, 2 * w // 3, w]

        diffs: list[float] = []
        for r in range(3):
            for c in range(3):
                z1 = a1[ys[r]:ys[r+1], xs[c]:xs[c+1]]
                z2 = a2[ys[r]:ys[r+1], xs[c]:xs[c+1]]
                diffs.append(float(np.mean(np.abs(z1 - z2))))

        center  = diffs[4]
        corners = (diffs[0] + diffs[2] + diffs[6] + diffs[8]) / 4.0
        overall = sum(diffs) / 9.0

        if overall < 4.0:
            return None, 0.0

        denom    = max(corners + center, 0.01)
        zi_score = (corners - center) / denom
        zo_score = (center  - corners) / denom

        if zi_score > 0.22 and corners > 5.0:
            return "zoom_in",  min(zi_score * 2.2, 1.0)
        if zo_score > 0.18 and center  > 5.0:
            return "zoom_out", min(zo_score * 2.2, 1.0)

        return None, 0.0

    def _merge_raw(
        self, raw: list[tuple[float, str, float]]
    ) -> list[dict]:
        if not raw:
            return []

        result: list[dict] = []
        run_ts, run_type, run_conf = raw[0]
        run_end = run_ts

        for ts, etype, conf in raw[1:]:
            if etype == run_type and (ts - run_end) < self.MERGE_GAP:
                run_end  = ts
                run_conf = max(run_conf, conf)
            else:
                result.append(_event(run_ts, run_type,
                                      run_end - run_ts, run_conf))
                run_ts, run_type, run_conf = ts, etype, conf
                run_end = ts

        result.append(_event(run_ts, run_type, run_end - run_ts, run_conf))
        return result


# ── TextOverlayDetector ────────────────────────────────────────────────────

class TextOverlayDetector:
    EDGE_THRESHOLD = 0.08    # PIL edge density floor for OCR eligibility
    MIN_CONF       = 40      # pytesseract word confidence threshold (0–100)
    MERGE_GAP      = 1.5     # seconds

    @staticmethod
    def available() -> bool:
        return _HAS_OCR

    def run_chunk(
        self,
        video: Path,
        chunk_start: float,
        chunk_end: float,
        stats: list[FrameStat],
    ) -> list[dict]:
        from PIL import ImageFilter

        # Only check frames that are bright enough to contain overlays
        candidate_ts = [s.timestamp for s in stats if s.y_avg_norm > 0.3]
        if not candidate_ts:
            return []

        events: list[dict] = []
        active: dict | None = None

        with tempfile.TemporaryDirectory() as tmp:
            for ts in candidate_ts:
                fp = Path(tmp) / f"f_{ts:.3f}.jpg"
                cmd = [
                    "ffmpeg", "-y", "-hide_banner", "-nostats",
                    "-ss", f"{ts:.3f}", "-i", str(video),
                    "-frames:v", "1", "-vf", "scale=960:-2",
                    "-q:v", "3", str(fp),
                ]
                try:
                    subprocess.run(
                        cmd, check=True,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    )
                except subprocess.CalledProcessError:
                    continue

                img   = Image.open(fp).convert("L")
                edges = np.array(img.filter(ImageFilter.FIND_EDGES), dtype=np.float32)
                edge_density = float(edges.mean()) / 255.0
                fp.unlink(missing_ok=True)

                if edge_density < self.EDGE_THRESHOLD:
                    continue

                try:
                    ocr_data = _tess.image_to_data(
                        img,
                        output_type=_tess.Output.DICT,
                        config="--psm 6",
                    )
                except Exception:
                    continue

                texts: list[str] = []
                y_pos: list[int] = []
                for i, word in enumerate(ocr_data["text"]):
                    word = word.strip()
                    conf = int(ocr_data["conf"][i])
                    if word and conf >= self.MIN_CONF:
                        texts.append(word)
                        y_pos.append(ocr_data["top"][i])

                if not texts:
                    if active:
                        events.append(active)
                        active = None
                    continue

                text  = " ".join(texts)
                avg_y = sum(y_pos) / len(y_pos) if y_pos else img.height / 2
                h     = img.height
                pos   = (
                    "upper" if avg_y < h / 3
                    else "lower" if avg_y > 2 * h / 3
                    else "middle"
                )

                if (
                    active
                    and active["properties"].get("text_detected") == text
                    and (ts - active["timestamp"] - active["duration"]) < self.MERGE_GAP
                ):
                    active["duration"] = round(ts - active["timestamp"], 3)
                else:
                    if active:
                        events.append(active)
                    active = _event(ts, "text_overlay", 0.0, 0.75,
                                     text_detected=text, position=pos)

        if active:
            events.append(active)

        return events


# ── FaceDetector ───────────────────────────────────────────────────────────

class FaceDetector:
    MIN_DURATION = 1.0   # seconds — ignore very brief face detections

    @staticmethod
    def available() -> bool:
        return _HAS_CV2

    def run_chunk(
        self,
        video: Path,
        chunk_start: float,
        chunk_end: float,
        sample_rate: float,
    ) -> list[dict]:
        cascade_path = _cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        detector = _cv2.CascadeClassifier(cascade_path)

        fps      = max(sample_rate / 3.0, 0.2)
        duration = chunk_end - chunk_start
        events:  list[dict] = []
        face_was_visible: bool | None = None
        run_start = chunk_start

        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            cmd = [
                "ffmpeg", "-y", "-hide_banner", "-nostats",
                "-ss", f"{chunk_start:.3f}",
                "-i", str(video),
                "-t", f"{duration:.3f}",
                "-vf", f"fps={fps:.3f},scale=480:-2",
                "-f", "image2", "-q:v", "6",
                str(tmp_dir / "f%05d.jpg"),
            ]
            try:
                subprocess.run(
                    cmd, check=True,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            except subprocess.CalledProcessError:
                return []

            frames = sorted(tmp_dir.glob("f*.jpg"))
            step   = 1.0 / fps

            for i, fp in enumerate(frames):
                ts  = round(chunk_start + i * step, 3)
                img = _cv2.imread(str(fp), _cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue
                faces   = detector.detectMultiScale(img, scaleFactor=1.1, minNeighbors=4)
                visible = len(faces) > 0

                if face_was_visible is None:
                    face_was_visible = visible
                    run_start = ts
                elif visible != face_was_visible:
                    dur = ts - run_start
                    if face_was_visible and dur >= self.MIN_DURATION:
                        events.append(_event(run_start, "face_visible", dur, 0.75))
                    face_was_visible = visible
                    run_start = ts

            last_ts = chunk_start + len(frames) * step
            if face_was_visible and (last_ts - run_start) >= self.MIN_DURATION:
                events.append(_event(run_start, "face_visible",
                                      last_ts - run_start, 0.75))

        return events


# ── ChunkProcessor ─────────────────────────────────────────────────────────

class ChunkProcessor:
    def __init__(
        self,
        video: Path,
        duration: float,
        chunk_minutes: float,
        sample_rate: float,
        detect: set[str],
    ):
        self.video       = video
        self.duration    = duration
        self.chunk_sec   = chunk_minutes * 60.0
        self.sample_rate = sample_rate
        self.detect      = detect

        self._ff   = FfmpegPassDetector()
        self._zoom = ZoomDetector()         if "zoom"   in detect else None
        self._text = TextOverlayDetector()  if ("text"  in detect and _HAS_OCR) else None
        self._face = FaceDetector()         if ("face"  in detect and _HAS_CV2) else None

    def process(self) -> tuple[list[dict], list[FrameStat]]:
        chunks: list[tuple[float, float]] = []
        t = 0.0
        while t < self.duration:
            chunks.append((t, min(t + self.chunk_sec, self.duration)))
            t += self.chunk_sec

        all_events: list[dict]   = []
        all_stats:  list[FrameStat] = []

        for chunk_start, chunk_end in _progress(chunks, desc="analyzing"):
            events, stats = self._ff.run_and_detect(
                self.video, chunk_start, chunk_end, self.sample_rate, self.detect
            )
            all_events.extend(events)
            all_stats.extend(stats)

            scene_times = {e["timestamp"] for e in events if e["type"] == "scene_change"}

            if self._zoom:
                all_events.extend(self._zoom.run_chunk(
                    self.video, chunk_start, chunk_end,
                    self.sample_rate, scene_times,
                ))

            if self._text:
                all_events.extend(self._text.run_chunk(
                    self.video, chunk_start, chunk_end, stats
                ))

            if self._face:
                all_events.extend(self._face.run_chunk(
                    self.video, chunk_start, chunk_end, self.sample_rate
                ))

        return all_events, all_stats


# ── EventMerger ────────────────────────────────────────────────────────────

class EventMerger:
    MERGE_WINDOWS: dict[str, float] = {
        "zoom_in":        1.5,
        "zoom_out":       1.5,
        "screen_content": 3.0,
        "text_overlay":   1.5,
        "motion_high":    1.0,
        "face_visible":   2.0,
    }

    def merge(self, events: list[dict]) -> list[dict]:
        if not events:
            return []

        events = sorted(events, key=lambda e: e["timestamp"])

        result: list[dict] = []
        for e in events:
            etype  = e["type"]
            window = self.MERGE_WINDOWS.get(etype, 0.0)
            merged = False

            for prev in reversed(result):
                if prev["type"] != etype:
                    continue
                prev_end = prev["timestamp"] + max(prev["duration"], 0.1)
                if e["timestamp"] - prev_end <= window:
                    new_end = max(prev_end, e["timestamp"] + max(e["duration"], 0.0))
                    prev["duration"]   = round(new_end - prev["timestamp"], 3)
                    prev["confidence"] = round(max(prev["confidence"], e["confidence"]), 3)
                    for k, v in e["properties"].items():
                        if k not in prev["properties"]:
                            prev["properties"][k] = v
                    merged = True
                    break

            if not merged:
                result.append(e)

        result.sort(key=lambda e: e["timestamp"])
        for i, e in enumerate(result, 1):
            e["id"] = i

        return result


# ── ReportRenderer ─────────────────────────────────────────────────────────

class ReportRenderer:

    # -- JSON --

    def write_json(
        self,
        path: Path,
        events: list[dict],
        video_meta: dict,
        transcript_source: str,
        summary: dict,
    ) -> None:
        payload = {
            "video":             video_meta,
            "transcript_source": transcript_source,
            "summary":           summary,
            "events":            events,
        }
        path.write_text(json.dumps(payload, indent=2))
        print(f"saved: {path.name}  ({path.stat().st_size // 1024} KB)")

    # -- Markdown --

    def write_markdown(
        self,
        path: Path,
        events: list[dict],
        video_meta: dict,
        summary: dict,
    ) -> None:
        dur   = video_meta["duration"]
        vname = Path(video_meta["path"]).name
        w, h  = video_meta["resolution"]

        lines = [
            f"# Video Analysis: {vname}",
            "",
            f"**Duration:** {_fmt_time(dur)}  ",
            f"**Resolution:** {w}×{h}  ",
            f"**Events detected:** {summary.get('total_events', 0)}",
            "",
            "---",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|--------|-------|",
        ]

        by_type = summary.get("by_type", {})
        for etype, count in sorted(by_type.items(), key=lambda x: -x[1]):
            lines.append(f"| {etype.replace('_', ' ').title()} | {count} |")

        density = summary.get("density", {})
        for k, v in density.items():
            lines.append(f"| {k.replace('_', ' ').title()} | {v:.2f}/min |")

        for k, v in summary.get("speech_visual_alignment", {}).items():
            lines.append(f"| {k.replace('_', ' ').title()} | {v:.0%} |")

        lines += ["", "---", "", "## Event Timeline", ""]

        current_minute = -1
        for e in events:
            ts     = e["timestamp"]
            minute = int(ts // 60)

            if minute != current_minute:
                current_minute = minute
                m_end = min((minute + 1) * 60, dur)
                lines += [f"### {_fmt_time(minute * 60)} – {_fmt_time(m_end)}", ""]

            etype = e["type"]
            props = e["properties"]
            ctx   = e["transcript_context"]

            line = f"**[{_fmt_time(ts)}]** `{etype}`"

            if etype in ("zoom_in", "zoom_out"):
                sp = props.get("scale_peak")
                if sp:
                    line += f" — peak {sp}×"
            elif etype == "scene_change":
                kind  = props.get("kind", "cut")
                score = props.get("scd_score")
                line += f" ({kind}"
                if score:
                    line += f", score {score:.1f}"
                line += ")"
            elif etype == "text_overlay":
                text = props.get("text_detected", "")
                pos  = props.get("position", "")
                if text:
                    line += f' — "{text}"'
                if pos:
                    line += f" [{pos}]"

            dur_e = e["duration"]
            if dur_e > 0.0:
                line += f" — {dur_e:.1f}s"

            lines.append(line)

            if ctx:
                emph = "  ⚡ emphasis" if ctx.get("is_emphasis_word") else ""
                lines.append(f'> *"{ctx["sentence"]}"*{emph}')

            lines.append("")

        path.write_text("\n".join(lines))
        print(f"saved: {path.name}")

    # -- PNG --

    def write_timeline_png(
        self,
        path: Path,
        video: Path,
        events: list[dict],
        duration: float,
    ) -> None:
        sys.path.insert(0, str(HELPERS_DIR))
        from timeline_view import compute_envelope, load_font  # noqa: PLC0415

        CANVAS_W    = 3840
        FILMSTRIP_H = 120
        WAVE_H      = 140
        N_ROWS      = 4
        ROW_H       = 12
        EVENT_H     = N_ROWS * ROW_H
        LABEL_H     = 40
        PAD         = 50

        header_h    = 48
        filmstrip_y = header_h + 12
        wave_y      = filmstrip_y + FILMSTRIP_H + 16
        event_y     = wave_y + WAVE_H + 8
        legend_y    = event_y + EVENT_H + 6
        canvas_h    = legend_y + LABEL_H + 12

        canvas = Image.new("RGB", (CANVAS_W, canvas_h), BG)
        draw   = ImageDraw.Draw(canvas, "RGBA")

        hfont = load_font(20)
        lfont = load_font(13)
        sfont = load_font(11)

        draw.text(
            (PAD, 14),
            f"{video.name}   {_fmt_time(duration)}   {len(events)} events",
            fill=FG, font=hfont,
        )

        # Filmstrip — max 24 frames across full duration
        n_frames = max(min(24, int(duration / 60) + 2), 4)
        strip_w  = CANVAS_W - 2 * PAD

        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            step = duration / max(n_frames - 1, 1)
            imgs: list[Image.Image] = []

            for i in range(n_frames):
                t  = i * step
                fp = tmp_dir / f"f{i:03d}.jpg"
                cmd = [
                    "ffmpeg", "-y", "-hide_banner", "-nostats",
                    "-ss", f"{t:.3f}", "-i", str(video),
                    "-frames:v", "1", "-vf", "scale=200:-2",
                    "-q:v", "5", str(fp),
                ]
                try:
                    subprocess.run(
                        cmd, check=True,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    )
                    img = Image.open(fp).convert("RGB")
                    th  = FILMSTRIP_H
                    tw  = int(th * img.width / img.height)
                    imgs.append(img.resize((tw, th), Image.LANCZOS))
                except Exception:
                    imgs.append(Image.new("RGB", (int(FILMSTRIP_H * 16 / 9), FILMSTRIP_H),
                                          (35, 35, 45)))

        total_w = sum(im.width for im in imgs) + max(0, len(imgs) - 1) * 3
        if total_w > strip_w:
            sc = strip_w / total_w
            imgs = [im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
                    for im in imgs]

        x = PAD
        for im in imgs:
            canvas.paste(im, (x, filmstrip_y + (FILMSTRIP_H - im.height) // 2))
            x += im.width + 3

        strip_x0 = PAD
        strip_x1 = CANVAS_W - PAD
        span     = strip_x1 - strip_x0

        def t2x(t: float) -> int:
            return strip_x0 + int((t / max(duration, 1.0)) * span)

        # Waveform
        draw.rectangle([strip_x0, wave_y, strip_x1, wave_y + WAVE_H], fill=(26, 26, 32))
        env = compute_envelope(video, 0.0, duration, samples=span)
        mid  = wave_y + WAVE_H // 2
        ampl = WAVE_H // 2 - 6
        pts_t = [(strip_x0 + int(i * span / max(len(env) - 1, 1)),
                   mid - int(v * ampl)) for i, v in enumerate(env)]
        pts_b = [(x, mid + (mid - y)) for x, y in pts_t]
        if pts_t:
            draw.line(pts_t, fill=WAVE, width=1)
            draw.line(pts_b, fill=WAVE, width=1)
            draw.polygon(pts_t + list(reversed(pts_b)), fill=(*WAVE, 35))

        # Time ruler
        n_ticks = 10
        for i in range(n_ticks + 1):
            t  = duration * i / n_ticks
            xi = t2x(t)
            draw.line([(xi, wave_y + WAVE_H), (xi, wave_y + WAVE_H + 5)], fill=DIM)
            draw.text((xi - 18, wave_y + WAVE_H + 7), _fmt_time(t), fill=DIM, font=lfont)

        # Event lane
        draw.rectangle([strip_x0, event_y, strip_x1, event_y + EVENT_H],
                        fill=(22, 22, 30))

        for e in events:
            ts    = e["timestamp"]
            dur_e = max(e["duration"], 0.3)
            etype = e["type"]
            color = EVENT_COLORS.get(etype, DIM)
            row   = _EVENT_ROW.get(etype, 0)
            x0    = t2x(ts)
            x1    = max(t2x(ts + dur_e), x0 + 2)
            ry    = event_y + row * ROW_H
            ry1   = ry + ROW_H - 1

            if etype == "scene_change":
                draw.line([(x0, event_y), (x0, event_y + EVENT_H)],
                           fill=(*color, 220), width=2)
            else:
                draw.rectangle([x0, ry, x1, ry1], fill=(*color, 180))

        # Legend
        lx = strip_x0
        for etype, color in EVENT_COLORS.items():
            draw.rectangle([lx, legend_y, lx + 12, legend_y + 12], fill=color)
            draw.text((lx + 15, legend_y), etype.replace("_", " "),
                       fill=DIM, font=sfont)
            lx += 135

        path.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(path, "PNG", optimize=True)
        print(f"saved: {path.name}  ({path.stat().st_size // 1024} KB)")


# ── Helpers ────────────────────────────────────────────────────────────────

def _fmt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def _compute_summary(
    events: list[dict], duration: float, aligner: TranscriptAligner
) -> dict:
    by_type: dict[str, int] = {}
    for e in events:
        by_type[e["type"]] = by_type.get(e["type"], 0) + 1

    minutes       = max(duration / 60.0, 1.0)
    overlay_count = by_type.get("text_overlay", 0) + by_type.get("screen_content", 0)
    zoom_count    = by_type.get("zoom_in", 0)  + by_type.get("zoom_out", 0)

    return {
        "total_events": len(events),
        "by_type":      by_type,
        "density": {
            "overlays_per_minute": round(overlay_count / minutes, 2),
            "zooms_per_minute":    round(zoom_count    / minutes, 2),
            "cuts_per_minute":     round(by_type.get("scene_change", 0) / minutes, 2),
        },
        "speech_visual_alignment": aligner.alignment_stats(events),
    }


# ── Main ────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Analyze visual events in a video, aligned to transcript."
    )
    ap.add_argument("input", type=str,
                    help="Video path or YouTube URL")
    ap.add_argument("--transcript", type=Path, default=None,
                    help="Existing transcript.json (skips auto-transcription)")
    ap.add_argument("--output", type=Path, default=None,
                    help="Output directory (default: same dir as video)")
    ap.add_argument("--sample-rate", type=float, default=1.0,
                    help="Frames per second to sample (default: 1.0)")
    ap.add_argument("--detect", type=str, default="scene,motion,zoom,screen,text,face",
                    help="Comma-separated detectors (default: all)")
    ap.add_argument("--chunk-minutes", type=float, default=5.0,
                    help="Processing chunk size in minutes (default: 5)")
    args = ap.parse_args()

    detect = {d.strip().lower() for d in args.detect.split(",")}

    if "text" in detect and not _HAS_OCR:
        print("note: text detection skipped — install: brew install tesseract && pip install pytesseract")
        detect.discard("text")
    if "face" in detect and not _HAS_CV2:
        print("note: face detection skipped — install: pip install opencv-python-headless")
        detect.discard("face")

    # Resolve video
    if VideoDownloader.is_url(args.input):
        video      = VideoDownloader.download(args.input)
        output_dir = args.output or CACHE_DIR
    else:
        video = Path(args.input).resolve()
        if not video.exists():
            sys.exit(f"video not found: {video}")
        output_dir = (args.output or video.parent).resolve()

    output_dir.mkdir(parents=True, exist_ok=True)
    stem = video.stem

    # Probe
    print(f"\nprobing: {video.name}")
    video_meta = VideoProbe.probe(video)
    dur = video_meta["duration"]
    w, h = video_meta["resolution"]
    print(f"  {_fmt_time(dur)}  {w}×{h}  {video_meta['fps']:.2f}fps")

    # Transcript
    loader = TranscriptLoader()
    transcript_data, transcript_source = loader.resolve(
        video, args.transcript, output_dir
    )
    aligner = TranscriptAligner(
        (transcript_data or {}).get("words", [])
    )

    # Detect
    print(f"\ndetecting: {', '.join(sorted(detect))}")
    processor = ChunkProcessor(
        video         = video,
        duration      = dur,
        chunk_minutes = args.chunk_minutes,
        sample_rate   = args.sample_rate,
        detect        = detect,
    )
    raw_events, stats = processor.process()

    # Merge + align
    events = EventMerger().merge(raw_events)
    print(f"\nfound {len(events)} events")

    for e in events:
        e["transcript_context"] = aligner.context_at(e["timestamp"])

    # Summarize
    summary = _compute_summary(events, dur, aligner)

    # Write outputs
    print()
    renderer = ReportRenderer()
    renderer.write_json(
        output_dir / f"{stem}_analysis.json",
        events, video_meta, transcript_source, summary,
    )
    renderer.write_markdown(
        output_dir / f"{stem}_analysis.md",
        events, video_meta, summary,
    )
    renderer.write_timeline_png(
        output_dir / f"{stem}_timeline.png",
        video, events, dur,
    )

    print(f"\ndone — {output_dir}")


if __name__ == "__main__":
    main()
