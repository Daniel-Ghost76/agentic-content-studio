#!/usr/bin/env python3
"""
pipeline_status.py — Report which videos are currently in production and where each one is blocked.

A project is "in production" if it has a script PDF or an mp4 in the editing folder,
and has not yet been published (no files in the published/ subfolder of Stage 7).

Usage:
    python3 pipeline_status.py           # print to stdout
    python3 pipeline_status.py --send    # also send to Telegram via bot API
"""

import os
import re
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[3]
OUTPUT = WORKSPACE / "Youtube" / "Output"

STAGE_DIRS = {
    "ideation":      OUTPUT / "1. Ideation",
    "scripts":       OUTPUT / "2. Scripts",
    "preproduction": OUTPUT / "3. Pre-production Materials",
    "editing":       OUTPUT / "4. Editing",
    "visuals":       OUTPUT / "5. Visuals",
    "review":        OUTPUT / "6. Review  ",
    "publishing":    OUTPUT / "7. Publishing",
    "distribution":  OUTPUT / "8. Distribution",
    "analytics":     OUTPUT / "9. Analytics",
}

DANIEL_TELEGRAM_ID = "6174417525"


def real_files(folder):
    """Return list of real files in folder, ignoring .DS_Store."""
    if not folder.exists():
        return []
    return [f for f in folder.iterdir() if f.is_file() and f.name != ".DS_Store"]


def has_file(folder, pattern):
    if not folder.exists():
        return False
    return bool(list(folder.glob(pattern)))


def all_projects():
    d = STAGE_DIRS["ideation"]
    if not d.exists():
        return []
    return sorted(p.name for p in d.iterdir() if p.is_dir() and not p.name.startswith("."))


def is_published(pid):
    pub = STAGE_DIRS["publishing"] / pid / "published"
    return bool(real_files(pub))


def has_script(pid):
    return has_file(STAGE_DIRS["scripts"] / pid, f"{pid}_script.pdf")


def has_recording(pid):
    return has_file(STAGE_DIRS["editing"] / pid, "*.mp4")


def is_in_production(pid):
    if is_published(pid):
        return False
    return has_script(pid) or has_recording(pid)


def stage_status(pid):
    e = STAGE_DIRS["editing"] / pid
    v = STAGE_DIRS["visuals"] / pid
    r = STAGE_DIRS["review"] / pid
    return {
        "script":        has_script(pid),
        "preproduction": bool(real_files(STAGE_DIRS["preproduction"] / pid)),
        "recording":     has_recording(pid),
        "cut":           has_file(e, f"{pid}_cut.mp4"),
        "visuals":       has_file(v, f"{pid}_overlaid.mp4"),
        "review":        has_file(r, f"{pid}_metadata.yaml") and has_file(r, f"{pid}_review.mp4"),
    }


def blocker(pid, done):
    if not done["script"]:
        return "Scripted — no, not yet. Run /script in Claude Code to start it."
    if not done["recording"]:
        return "Script is ready — waiting on you to record it."
    if not done["cut"]:
        return "Recording's in. Needs a cut edit — run /cut-edit in Claude Code."
    if not done["visuals"]:
        return "Cut is done. Waiting on visuals and overlays — that's Codex."
    if not done["review"]:
        return "Visuals are in. Needs review — run /review in Claude Code."
    return "Review done. Ready to publish — run /publish in Claude Code or ask me."


def readable_title(pid):
    stripped = re.sub(r'^\d+[-_]', '', pid)
    return stripped.replace("-", " ").replace("_", " ").title()


def build_message(in_production_list, ideation_count):
    lines = ["Morning, Master Daniel. Here's where things stand:\n"]

    for pid, done in in_production_list:
        title = readable_title(pid)
        lines.append(f"{title} — {blocker(pid, done)}")

    if ideation_count:
        lines.append(f"\n{ideation_count} idea{'s' if ideation_count != 1 else ''} sitting in ideation whenever you're ready to move one forward.")

    return "\n".join(lines)


def send_telegram(message):
    env_path = Path.home() / ".claude" / ".env"
    token = None
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("TELEGRAM_BOT_TOKEN="):
                token = line.split("=", 1)[1].strip().strip('"').strip("'")
                break

    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not found in ~/.claude/.env", file=sys.stderr)
        sys.exit(1)

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": DANIEL_TELEGRAM_ID, "text": message}).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=data)) as resp:
        result = json.loads(resp.read())
        if not result.get("ok"):
            print(f"Telegram API error: {result}", file=sys.stderr)
            sys.exit(1)


def main():
    do_send = "--send" in sys.argv

    projects = all_projects()
    in_production = []
    ideation_only_count = 0

    for pid in projects:
        if is_published(pid):
            continue
        if is_in_production(pid):
            in_production.append((pid, stage_status(pid)))
        else:
            ideation_only_count += 1

    if not in_production:
        message = "Morning, Master Daniel. Nothing is actively in production right now — everything's either published or still at the idea stage."
    else:
        message = build_message(in_production, ideation_only_count)

    print(message)

    if do_send:
        send_telegram(message)
        print("\n[sent to Telegram]")


if __name__ == "__main__":
    main()
