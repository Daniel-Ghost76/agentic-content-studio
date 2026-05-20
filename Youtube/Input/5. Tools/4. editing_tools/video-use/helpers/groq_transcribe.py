"""Transcribe a video with Groq Whisper large-v3.

Extracts mono 16kHz audio via ffmpeg, chunks into <=15 min segments to stay
within Groq's file size limits, transcribes each chunk, merges with time
offsets, and writes output in ElevenLabs Scribe-compatible format so
pack_transcripts.py works unchanged.

Usage:
    python helpers/groq_transcribe.py <video_path>
    python helpers/groq_transcribe.py <video_path> --edit-dir /custom/edit
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import re

import requests


GROQ_URL = "https://api.groq.com/openai/v1/audio/transcriptions"
CHUNK_MINUTES = 15


def load_api_key() -> str:
    candidates = [
        Path.home() / ".claude" / ".env",
        Path(__file__).resolve().parent.parent / ".env",
        Path(".env"),
    ]
    for candidate in candidates:
        if candidate.exists():
            for line in candidate.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == "GROQ_API_KEY":
                    val = v.strip().strip('"').strip("'")
                    if val:
                        return val
    v = os.environ.get("GROQ_API_KEY", "")
    if not v:
        sys.exit("GROQ_API_KEY not found in ~/.claude/.env or environment")
    return v


def get_duration(video_path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())


def extract_chunk(video_path: Path, dest: Path, start: float, duration: float) -> None:
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start),
        "-i", str(video_path),
        "-t", str(duration),
        "-vn", "-ac", "1", "-ar", "16000",
        "-c:a", "libmp3lame", "-b:a", "16k",
        str(dest),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def transcribe_chunk(audio_path: Path, api_key: str, time_offset: float) -> list[dict]:
    while True:
        with open(audio_path, "rb") as f:
            resp = requests.post(
                GROQ_URL,
                headers={"Authorization": f"Bearer {api_key}"},
                files={"file": (audio_path.name, f, "audio/mpeg")},
                data={
                    "model": "whisper-large-v3",
                    "response_format": "verbose_json",
                    "timestamp_granularities[]": "word",
                    "language": "en",
                },
                timeout=300,
            )

        if resp.status_code == 429:
            # Parse wait time from error message e.g. "try again in 5m21.5s"
            match = re.search(r"try again in (\d+m\s*)?(\d+(?:\.\d+)?s)?", resp.text)
            wait = 60.0
            if match:
                mins = float((match.group(1) or "0m").rstrip("m")) * 60
                secs = float((match.group(2) or "0s").rstrip("s"))
                wait = mins + secs + 5  # +5s buffer
            print(f"    rate limit — waiting {wait:.0f}s...", flush=True)
            time.sleep(wait)
            continue

        if resp.status_code != 200:
            raise RuntimeError(f"Groq returned {resp.status_code}: {resp.text[:500]}")
        break

    words = []
    for w in resp.json().get("words", []):
        start = round(w.get("start", 0.0) + time_offset, 3)
        end = round(w.get("end", w.get("start", 0.0)) + time_offset, 3)
        words.append({
            "text": w.get("word", "").strip(),
            "start": start,
            "end": end,
            "type": "word",
            "speaker_id": None,
        })
    return words


def main() -> None:
    ap = argparse.ArgumentParser(description="Transcribe a video with Groq Whisper large-v3")
    ap.add_argument("video", type=Path)
    ap.add_argument("--edit-dir", type=Path, default=None)
    args = ap.parse_args()

    video = args.video.resolve()
    if not video.exists():
        sys.exit(f"video not found: {video}")

    edit_dir = (args.edit_dir or (video.parent / "edit")).resolve()
    transcripts_dir = edit_dir / "transcripts"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    out_path = transcripts_dir / f"{video.stem}.json"

    if out_path.exists():
        print(f"cached: {out_path.name}")
        return

    api_key = load_api_key()

    print(f"  probing {video.name}", flush=True)
    total_duration = get_duration(video)
    chunk_seconds = CHUNK_MINUTES * 60
    num_chunks = -(-int(total_duration) // int(chunk_seconds))  # ceiling division

    print(f"  {total_duration/60:.1f} min total → {num_chunks} chunk(s) of {CHUNK_MINUTES} min", flush=True)

    all_words: list[dict] = []
    t0 = time.time()
    chunks_dir = transcripts_dir / f"{video.stem}_chunks"
    chunks_dir.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        for i in range(num_chunks):
            chunk_cache = chunks_dir / f"chunk_{i:03d}.json"
            if chunk_cache.exists():
                words = json.loads(chunk_cache.read_text())
                all_words.extend(words)
                print(f"  chunk {i+1}/{num_chunks}: cached ({len(words)} words)", flush=True)
                continue

            start = i * chunk_seconds
            duration = min(chunk_seconds, total_duration - start)
            chunk_path = Path(tmp) / f"chunk_{i:03d}.mp3"

            print(f"  chunk {i+1}/{num_chunks}: {start/60:.1f}–{(start+duration)/60:.1f} min", flush=True)
            extract_chunk(video, chunk_path, start, duration)
            size_mb = chunk_path.stat().st_size / (1024 * 1024)
            print(f"    {size_mb:.1f} MB — transcribing...", flush=True)

            words = transcribe_chunk(chunk_path, api_key, time_offset=start)
            chunk_cache.write_text(json.dumps(words))
            all_words.extend(words)
            print(f"    {len(words)} words", flush=True)

    payload = {
        "language_code": "en",
        "language_probability": 1.0,
        "text": " ".join(w["text"] for w in all_words if w["text"]),
        "words": all_words,
        "transcription_id": f"groq_{video.stem}",
    }

    out_path.write_text(json.dumps(payload, indent=2))
    dt = time.time() - t0
    kb = out_path.stat().st_size / 1024
    print(f"  saved: {out_path.name} ({kb:.0f} KB) in {dt:.0f}s")
    print(f"  total words: {len(all_words)}")


if __name__ == "__main__":
    main()
