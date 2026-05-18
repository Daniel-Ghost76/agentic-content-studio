#!/usr/bin/env python3
"""
Usage: python3 extract_tools_from_transcript.py <transcript.json or .txt>
Scans a transcript for known tool/software names and prints a list.
Handles ElevenLabs Scribe JSON format and plain text.
"""
import sys
import os
import json
import re

# Canonical tool name list (scripting_rules.md vocabulary + CLAUDE.md)
# Ordered so longer/more specific matches come first to avoid partial matches
TOOL_NAMES = [
    # Multi-word first
    "Claude Code",
    "Google Sheets",
    "Google Docs",
    "Google Drive",
    "Apps Script",
    "YouTube Studio",
    "YouTube Data API",
    "Final Cut Pro",
    "DaVinci Resolve",
    "Premiere Pro",
    "You Know",  # not a tool — excluded below via allowlist logic
    # Single-word / short
    "ChatGPT",
    "Claude",
    "Gemini",
    "Grok",
    "DeepSeek",
    "Perplexity",
    "Copilot",
    "Anthropic",
    "OpenAI",
    "n8n",
    "Make",
    "Zapier",
    "Activepieces",
    "ElevenLabs",
    "Scribe",
    "Remotion",
    "HyperFrames",
    "Manim",
    "CapCut",
    "ffmpeg",
    "yt-dlp",
    "YTDLP",
    "Python",
    "JavaScript",
    "TypeScript",
    "GitHub",
    "Cursor",
    "Codex",
    "Hermes",
    "Skool",
    "Telegram",
    "Slack",
    "Notion",
    "YouTube",
]

# Items in TOOL_NAMES that are NOT tools and should be excluded
NOT_TOOLS = {"You Know"}


def build_patterns():
    patterns = []
    for name in TOOL_NAMES:
        if name in NOT_TOOLS:
            continue
        escaped = re.escape(name)
        pat = re.compile(r"(?<![A-Za-z0-9])" + escaped + r"(?![A-Za-z0-9])", re.IGNORECASE)
        patterns.append((name, pat))
    return patterns


def extract_text(path: str) -> str:
    _, ext = os.path.splitext(path.lower())
    if ext == ".json":
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if "words" in data:
            return " ".join(
                w["text"] for w in data["words"] if w.get("type") == "word"
            )
        if "text" in data:
            return data["text"]
        return json.dumps(data)
    else:
        with open(path, encoding="utf-8") as f:
            return f.read()


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_tools_from_transcript.py <transcript.json or .txt>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"Error: file not found: {path}")
        sys.exit(1)

    text = extract_text(path)
    patterns = build_patterns()

    found = []
    for name, pattern in patterns:
        if pattern.search(text):
            found.append(name)

    if not found:
        print("No known tools found in transcript.")
    else:
        print("Tools mentioned in transcript:")
        for tool in found:
            print(f"  {tool}")
        print()
        print("Use this list for the TOOLS USED section in the YAML description.")


if __name__ == "__main__":
    main()
