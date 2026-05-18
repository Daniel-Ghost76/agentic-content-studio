#!/usr/bin/env python3
"""
Usage: python3 check_analytics_due.py
Reads upload_log.md and prints which Day 7 / Day 30 snapshots are due.

Upload log format (publishing_sub-agent.md Step 9):
| project_id | Date Uploaded | Title | Video ID | URL | Scheduled For |
Scheduled For format: YYYY-MM-DD HH:MM London

Snapshot files:
  Youtube/Output/9. Analytics/{project_id}/{project_id}_analytics_d07.md
  Youtube/Output/9. Analytics/{project_id}/{project_id}_analytics_d30.md

YouTube has a 2-3 day data delay — snapshots available after publish + N + 2 days.
"""
import sys
import os
import re
from datetime import date, timedelta

WORKSPACE_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
)
ANALYTICS_DIR = os.path.join(WORKSPACE_ROOT, "Youtube", "Output", "9. Analytics")
UPLOAD_LOG = os.path.join(ANALYTICS_DIR, "upload_log.md")
DATA_DELAY_DAYS = 2


def parse_date(s: str):
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None


def parse_upload_log(path: str):
    videos = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("|"):
                continue
            if "project_id" in line.lower() or re.match(r"\|[-\s|]+\|", line):
                continue
            cols = [c.strip() for c in line.strip("|").split("|")]
            if len(cols) < 6:
                continue
            project_id = cols[0]
            title = cols[2]
            video_id = cols[3]
            scheduled_for = cols[5]
            pub_date = parse_date(scheduled_for)
            if project_id and pub_date:
                videos.append({
                    "project_id": project_id,
                    "title": title,
                    "video_id": video_id,
                    "publish_date": pub_date,
                })
    return videos


def snapshot_path(project_id: str, snapshot: str) -> str:
    return os.path.join(ANALYTICS_DIR, project_id, f"{project_id}_analytics_{snapshot}.md")


def main():
    if not os.path.isfile(UPLOAD_LOG):
        print("No upload_log.md found.")
        print(f"Expected at: {UPLOAD_LOG}")
        print("Publish a video first with /publish.")
        sys.exit(0)

    videos = parse_upload_log(UPLOAD_LOG)
    if not videos:
        print("upload_log.md has no video rows. Nothing to check.")
        sys.exit(0)

    today = date.today()
    available_cutoff = today - timedelta(days=DATA_DELAY_DAYS)

    print(f"Analytics due-date check — today: {today}")
    print()
    col = "{:<32} {:<12} {:<22} {:<22} {}"
    print(col.format("Project ID", "Published", "D07", "D30", "Action"))
    print("-" * 100)

    any_to_fetch = False

    for v in videos:
        pid = v["project_id"]
        pub = v["publish_date"]

        d07_due = pub + timedelta(days=7)
        d30_due = pub + timedelta(days=30)

        d07_available = d07_due <= available_cutoff
        d30_available = d30_due <= available_cutoff

        d07_exists = os.path.isfile(snapshot_path(pid, "d07"))
        d30_exists = os.path.isfile(snapshot_path(pid, "d30"))

        def status(available, exists, due_date):
            if exists:
                return "done"
            if available:
                return "FETCH"
            return f"due {due_date}"

        d07_status = status(d07_available, d07_exists, d07_due)
        d30_status = status(d30_available, d30_exists, d30_due)

        actions = []
        if "FETCH" in d07_status:
            actions.append("fetch d07")
            any_to_fetch = True
        if "FETCH" in d30_status:
            actions.append("fetch d30")
            any_to_fetch = True
        action_str = ", ".join(actions) if actions else "—"

        print(col.format(pid[:31], str(pub), d07_status, d30_status, action_str))

    print()
    if any_to_fetch:
        print("Run fetch_analytics.py for each row marked FETCH.")
        print("Command:")
        print('  venv/bin/python3 fetch_analytics.py \\')
        print('    --project-id "<pid>" --video-id "<vid>" \\')
        print('    --title "<title>" --published "<YYYY-MM-DD>" \\')
        print('    --snapshot d07|d30 --output-dir "Youtube/Output/9. Analytics"')
    else:
        print("All snapshots current — nothing to fetch.")


if __name__ == "__main__":
    main()
