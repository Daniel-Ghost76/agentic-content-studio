"""
compress_gaps.py — Snap EDL cut edges to word boundaries and compress long
internal silences into tight sub-segments.

The LLM builds the content EDL (which takes/sentences to keep). This script
fixes the mechanical precision:

  1. Snaps every segment [start, end] to the nearest word boundary in the
     ElevenLabs Scribe transcript — eliminates mid-word cuts.

  2. Walks each kept segment word-by-word. Any gap between consecutive words
     >= max_gap_ms is a split point. The segment is divided there and each
     piece gets keep_gap_ms/2 of padding on both sides — compresses dead air
     without clipping speech.

  3. Updates total_duration_s in the output EDL.

Transcripts are loaded from <edl_dir>/transcripts/<source_name>.json — the
same location transcribe.py writes to.

Usage:
    python helpers/compress_gaps.py <edl.json>
    python helpers/compress_gaps.py <edl.json> --max-gap 400 --keep-gap 150
    python helpers/compress_gaps.py <edl.json> --in-place

Default thresholds (milliseconds):
    --max-gap  400   gaps >= 400ms are split and compressed
    --keep-gap 150   total silence kept across each split (75ms each side)

Output: <edl_stem>_compressed.json  (or overwrites input if --in-place)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Transcript loading
# ---------------------------------------------------------------------------

def load_words(transcript_path: Path) -> list[dict]:
    """Return word-type entries with valid start/end, sorted by start time."""
    data = json.loads(transcript_path.read_text())
    words = []
    for w in data.get("words", []):
        if w.get("type") != "word":
            continue
        s, e = w.get("start"), w.get("end")
        if s is None or e is None:
            continue
        text = (w.get("text") or "").strip()
        if not text:
            continue
        words.append({"text": text, "start": float(s), "end": float(e)})
    return sorted(words, key=lambda w: w["start"])


def words_in_range(
    words: list[dict], t_start: float, t_end: float, tol: float = 0.08
) -> list[dict]:
    """Words that overlap [t_start, t_end] with tol-second boundary tolerance."""
    return [
        w for w in words
        if w["end"] > t_start - tol and w["start"] < t_end + tol
    ]


# ---------------------------------------------------------------------------
# Boundary snapping
# ---------------------------------------------------------------------------

def snap_start(words: list[dict], t: float, tol: float = 0.08) -> float:
    """
    Return the start of the first word that begins at or after (t - tol).
    Falls back to the word with the closest start if none qualifies.
    """
    candidates = [w for w in words if w["start"] >= t - tol]
    if candidates:
        return candidates[0]["start"]
    return min(words, key=lambda w: abs(w["start"] - t))["start"]


def snap_end(words: list[dict], t: float, tol: float = 0.08) -> float:
    """
    Return the end of the last word that ends at or before (t + tol).
    Falls back to the word with the closest end if none qualifies.
    """
    candidates = [w for w in words if w["end"] <= t + tol]
    if candidates:
        return candidates[-1]["end"]
    return min(words, key=lambda w: abs(w["end"] - t))["end"]


# ---------------------------------------------------------------------------
# Gap compression
# ---------------------------------------------------------------------------

def split_on_gaps(
    words: list[dict],
    max_gap_s: float,
    pad_s: float,
) -> list[tuple[float, float]]:
    """
    Walk consecutive words. Where the inter-word gap >= max_gap_s, split.
    Each piece gets pad_s of silence before and after the speech boundary.

    Returns a list of (start, end) float pairs.
    """
    if not words:
        return []

    sub_segs: list[tuple[float, float]] = []
    seg_start = words[0]["start"] - pad_s

    for i in range(len(words) - 1):
        curr_end = words[i]["end"]
        next_start = words[i + 1]["start"]
        gap = next_start - curr_end

        if gap >= max_gap_s:
            seg_end = curr_end + pad_s
            sub_segs.append((seg_start, seg_end))
            seg_start = next_start - pad_s

    # Close the final piece
    seg_end = words[-1]["end"] + pad_s
    sub_segs.append((seg_start, seg_end))

    return sub_segs


# ---------------------------------------------------------------------------
# EDL processing
# ---------------------------------------------------------------------------

def process_edl(
    edl: dict,
    transcripts_dir: Path,
    max_gap_ms: int,
    keep_gap_ms: int,
) -> dict:
    max_gap_s = max_gap_ms / 1000.0
    pad_s = (keep_gap_ms / 2) / 1000.0  # half on each side of a split

    new_ranges: list[dict] = []
    orig_ranges = edl.get("ranges", [])
    orig_dur = sum(float(r["end"]) - float(r["start"]) for r in orig_ranges)

    transcript_cache: dict[str, list[dict]] = {}

    for r in orig_ranges:
        src_name = r["source"]
        orig_start = float(r["start"])
        orig_end = float(r["end"])

        # Load transcript (cached per source).
        # Try EDL source key first (e.g. "talking_head" -> transcripts/talking_head.json).
        # Fall back to the video stem from the sources path (e.g. the mp4 filename stem),
        # since transcribe.py names transcripts after the video file, not the EDL key.
        if src_name not in transcript_cache:
            tr_path = transcripts_dir / f"{src_name}.json"
            if not tr_path.exists():
                src_file = edl.get("sources", {}).get(src_name, "")
                if src_file:
                    stem = Path(src_file).stem
                    fallback = transcripts_dir / f"{stem}.json"
                    if fallback.exists():
                        tr_path = fallback
            if not tr_path.exists():
                print(f"  [warn] no transcript for '{src_name}' — keeping range as-is")
                transcript_cache[src_name] = []
            else:
                transcript_cache[src_name] = load_words(tr_path)

        all_words = transcript_cache[src_name]
        if not all_words:
            new_ranges.append(r)
            continue

        # Words that fall within (or near) this range
        scoped = words_in_range(all_words, orig_start, orig_end)
        if not scoped:
            print(
                f"  [warn] no words in {src_name} [{orig_start:.2f}-{orig_end:.2f}]"
                " — keeping range as-is"
            )
            new_ranges.append(r)
            continue

        # Snap outer boundaries to word edges
        snapped_start = snap_start(scoped, orig_start)
        snapped_end = snap_end(scoped, orig_end)

        # Re-scope words to snapped boundary
        scoped = words_in_range(all_words, snapped_start, snapped_end, tol=0.0)

        # Split on internal silence gaps
        sub_segs = split_on_gaps(scoped, max_gap_s, pad_s)

        # Clamp all sub-segment boundaries
        base = {k: v for k, v in r.items() if k not in ("start", "end")}
        for j, (s, e) in enumerate(sub_segs):
            s = max(0.0, s)
            e = max(s + 0.05, e)  # guard against zero-duration segments
            seg = dict(base)
            seg["start"] = round(s, 3)
            seg["end"] = round(e, 3)
            if len(sub_segs) > 1:
                label = r.get("beat") or r.get("note") or ""
                seg["note"] = f"{label} [{j + 1}/{len(sub_segs)}]".strip(" []")
            new_ranges.append(seg)

    new_dur = sum(float(r["end"]) - float(r["start"]) for r in new_ranges)
    removed = orig_dur - new_dur
    pct = removed / orig_dur * 100 if orig_dur > 0 else 0.0

    print(f"  original  : {orig_dur:.1f}s  ({len(orig_ranges)} ranges)")
    print(f"  compressed: {new_dur:.1f}s  ({len(new_ranges)} ranges)")
    print(f"  removed   : {removed:.1f}s  ({pct:.1f}%)")

    new_edl = dict(edl)
    new_edl["ranges"] = new_ranges
    new_edl["total_duration_s"] = round(new_dur, 3)
    return new_edl


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Snap EDL cut edges to word boundaries and compress silence gaps"
    )
    ap.add_argument("edl", type=Path, help="Path to edl.json")
    ap.add_argument(
        "--max-gap",
        type=int,
        default=400,
        metavar="MS",
        help="Gaps >= this many ms are split and compressed (default: 400)",
    )
    ap.add_argument(
        "--keep-gap",
        type=int,
        default=150,
        metavar="MS",
        help="Total silence kept across each split — 75ms each side (default: 150)",
    )
    ap.add_argument(
        "--in-place",
        action="store_true",
        help="Overwrite the input EDL instead of writing <stem>_compressed.json",
    )
    args = ap.parse_args()

    edl_path = args.edl.resolve()
    if not edl_path.exists():
        sys.exit(f"EDL not found: {edl_path}")

    edl = json.loads(edl_path.read_text())
    transcripts_dir = edl_path.parent / "transcripts"

    if not transcripts_dir.exists():
        sys.exit(
            f"transcripts dir not found: {transcripts_dir}\n"
            "Run transcribe.py first, or check the edit_dir path."
        )

    print(f"compress_gaps: {edl_path.name}")
    print(f"  max_gap={args.max_gap}ms  keep_gap={args.keep_gap}ms")

    new_edl = process_edl(edl, transcripts_dir, args.max_gap, args.keep_gap)

    if args.in_place:
        out_path = edl_path
    else:
        out_path = edl_path.with_stem(edl_path.stem + "_compressed")

    out_path.write_text(json.dumps(new_edl, indent=2))
    print(f"  written → {out_path.name}")


if __name__ == "__main__":
    main()
