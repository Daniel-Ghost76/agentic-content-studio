#!/usr/bin/env python3
"""
Usage: python3 validate_filler_words.py <path/to/transcript.json>
Pre-scans an ElevenLabs Scribe transcript JSON for filler words and long silences.

Filler word list (editing_rules.md / cut_edit_sub-agent.md):
  um, uh, ah, like (as filler), you know, so (at sentence start), basically

Silence thresholds (editing_rules.md):
  Remove >= 500ms gaps | Review 300-499ms | Preserve < 300ms
"""
import sys
import os
import json
import re

FILLER_EXACT = {"um", "uh", "ah", "basically"}
SILENCE_REMOVE_MS = 500
SILENCE_REVIEW_MS = 300


def load_words(path: str):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("words", [])


def fmt_ts(sec: float) -> str:
    m = int(sec) // 60
    s = int(sec) % 60
    ms = int((sec % 1) * 1000)
    return f"{m}:{s:02d}.{ms:03d}"


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_filler_words.py <transcript.json>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"Error: file not found: {path}")
        sys.exit(1)

    all_tokens = load_words(path)
    word_tokens = [w for w in all_tokens if w.get("type") == "word"]

    fillers = []
    silences = []

    prev_end = None
    prev_word_text = ""

    for i, token in enumerate(all_tokens):
        if token.get("type") == "spacing":
            continue

        start = token.get("start", 0)
        end = token.get("end", start)
        text = token.get("text", "").strip()
        text_lower = text.lower()

        # Silence detection: gap between end of previous word and start of this word
        if prev_end is not None:
            gap_ms = (start - prev_end) * 1000
            if gap_ms >= SILENCE_REVIEW_MS:
                action = "REMOVE" if gap_ms >= SILENCE_REMOVE_MS else "REVIEW"
                silences.append({
                    "after": fmt_ts(prev_end),
                    "gap_ms": int(gap_ms),
                    "action": action,
                })

        prev_end = end

        # Exact filler words
        if text_lower in FILLER_EXACT:
            fillers.append({
                "timestamp": fmt_ts(start),
                "word": text,
                "type": "filler",
            })
            prev_word_text = text_lower
            continue

        # "like" as filler — not preceded by looks/feels/seems/sounds/acts
        if text_lower == "like":
            if prev_word_text not in {"looks", "feels", "seems", "sounds", "acts", "just"}:
                fillers.append({
                    "timestamp": fmt_ts(start),
                    "word": text,
                    "type": "filler (likely)",
                })

        # "so" at sentence start — preceded by sentence-ending punctuation or nothing
        elif text_lower == "so":
            ends_sentence = bool(re.search(r"[.!?]$", prev_word_text)) or prev_word_text == ""
            if ends_sentence:
                fillers.append({
                    "timestamp": fmt_ts(start),
                    "word": text,
                    "type": "filler (sentence-start so)",
                })

        prev_word_text = text_lower

    # "you know" bigram scan
    words_only = [(w.get("text", "").strip().lower(), w.get("start", 0)) for w in all_tokens if w.get("type") == "word"]
    for i in range(len(words_only) - 1):
        if words_only[i][0] == "you" and words_only[i + 1][0] == "know":
            fillers.append({
                "timestamp": fmt_ts(words_only[i][1]),
                "word": "you know",
                "type": "filler",
            })

    # Sort by timestamp
    fillers.sort(key=lambda x: x["timestamp"])

    # Output report
    print(f"Pre-scan: {os.path.basename(path)}")
    print(f"Word tokens: {len(word_tokens)}")
    print()

    remove_silences = [s for s in silences if s["action"] == "REMOVE"]
    review_silences = [s for s in silences if s["action"] == "REVIEW"]

    print(f"FILLER WORDS — {len(fillers)} found")
    if fillers:
        print(f"  {'Timestamp':<16} {'Word':<12} Type")
        print("  " + "-" * 48)
        for f in fillers:
            print(f"  {f['timestamp']:<16} {f['word']:<12} {f['type']}")
    else:
        print("  None")

    print()
    print(f"SILENCES >= {SILENCE_REMOVE_MS}ms — {len(remove_silences)} to REMOVE, {len(review_silences)} to REVIEW")
    if silences:
        print(f"  {'After':<16} {'Gap (ms)':<12} Action")
        print("  " + "-" * 40)
        for s in silences:
            print(f"  {s['after']:<16} {s['gap_ms']:<12} {s['action']}")
    else:
        print("  None")


if __name__ == "__main__":
    main()
