#!/usr/bin/env python3
"""
Usage: python3 extract_srt_chapters.py <path/to/file.srt>
Parses an SRT file and outputs chapter timestamps for the YAML description field.

Rules (scripting_rules.md):
- Every chapter >= 60 seconds from the previous
- Max 5 chapters for videos <= 12 min
- Format: M:SS - Chapter Name (no leading zeros on minutes)
- First chapter always at 0:00
"""
import sys
import re
import os


def parse_srt(path: str):
    """Return list of (start_sec, text) for each SRT entry."""
    with open(path, encoding="utf-8") as f:
        content = f.read()

    entries = []
    blocks = re.split(r"\n\s*\n", content.strip())

    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue
        tc_match = re.match(
            r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})",
            lines[1],
        )
        if not tc_match:
            continue
        h = int(tc_match.group(1))
        m = int(tc_match.group(2))
        s = int(tc_match.group(3))
        ms = int(tc_match.group(4))
        start_sec = h * 3600 + m * 60 + s + ms / 1000
        text = " ".join(lines[2:]).strip()
        if text:
            entries.append((start_sec, text))

    return entries


def seconds_to_timestamp(sec: float) -> str:
    """Format seconds as M:SS with no leading zero on minutes."""
    total_sec = int(sec)
    minutes = total_sec // 60
    seconds = total_sec % 60
    return f"{minutes}:{seconds:02d}"


def clean_label(text: str, max_words: int = 5) -> str:
    """Strip filler words from the start, take first max_words, title-case."""
    fillers = {"um", "uh", "ah", "so", "and", "but", "like", "well", "right",
               "alright", "okay", "i'm", "i", "we", "you", "the"}
    words = text.split()
    while words and words[0].lower().rstrip(".,!?") in fillers:
        words = words[1:]
    if not words:
        words = text.split()
    label = " ".join(words[:max_words]).strip(".,!?")
    return label.title()


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_srt_chapters.py <path/to/file.srt>")
        sys.exit(1)

    srt_path = sys.argv[1]
    if not os.path.isfile(srt_path):
        print(f"Error: file not found: {srt_path}")
        sys.exit(1)

    entries = parse_srt(srt_path)
    if not entries:
        print("Error: no valid SRT entries found.")
        sys.exit(1)

    total_duration = entries[-1][0] if entries else 0
    max_chapters = 5 if total_duration <= 720 else 8

    # Find natural pauses (gap between consecutive starts > 2s)
    PAUSE_THRESHOLD = 2.0
    MIN_CHAPTER_GAP = 60.0

    candidates = [(0.0, entries[0][1])]

    for i in range(1, len(entries)):
        prev_start = entries[i - 1][0]
        curr_start, curr_text = entries[i]
        if curr_start - prev_start >= PAUSE_THRESHOLD:
            candidates.append((curr_start, curr_text))

    # Filter: each chapter must be >= 60s from the previous
    chapters = [candidates[0]]
    for t, text in candidates[1:]:
        if t - chapters[-1][0] >= MIN_CHAPTER_GAP:
            chapters.append((t, text))
        if len(chapters) >= max_chapters:
            break

    print("Timestamps for YAML description:")
    print()
    for start_sec, text in chapters:
        ts = seconds_to_timestamp(start_sec)
        label = clean_label(text)
        print(f"{ts} – {label}")
    print()
    print(f"({len(chapters)} chapters from {seconds_to_timestamp(total_duration)} video)")
    print("Verify chapter names match actual section content before saving to YAML.")


if __name__ == "__main__":
    main()
