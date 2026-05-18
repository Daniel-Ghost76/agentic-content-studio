#!/usr/bin/env python3
"""
Usage: python3 assemble_monthly_rollup.py --month YYYY-MM
Reads all snapshot MD files for the given month and assembles the monthly rollup.

Skips if the rollup file already exists (Rule R7: generate once, last week of month).
Uses the best available snapshot per video (d30 preferred over d07).

Underperformer flags (analytics_rules.md):
  CTR < 4%  |  avg view duration < 40%
"""
import sys
import os
import re
import argparse
from datetime import date

WORKSPACE_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
)
ANALYTICS_DIR = os.path.join(WORKSPACE_ROOT, "Youtube", "Output", "9. Analytics")
UPLOAD_LOG = os.path.join(ANALYTICS_DIR, "upload_log.md")

UNDERPERFORM_CTR = 4.0
UNDERPERFORM_DURATION = 40.0


def parse_date_from_str(s: str):
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
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
            project_id, title, video_id, scheduled_for = cols[0], cols[2], cols[3], cols[5]
            pub_date = parse_date_from_str(scheduled_for)
            if project_id and pub_date:
                videos.append({
                    "project_id": project_id,
                    "title": title,
                    "video_id": video_id,
                    "publish_date": pub_date,
                })
    return videos


def extract_metric(text: str, *patterns):
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return None


def to_float(s):
    if s is None:
        return None
    cleaned = re.sub(r"[,%+]", "", s)
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_snapshot(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        text = f.read()

    views = to_float(extract_metric(text,
        r"\|\s*Views\s*\|\s*([\d,]+)\s*\|",
        r"Views[:\s]+([\d,]+)"))
    ctr = to_float(extract_metric(text,
        r"\|\s*CTR\s*\|\s*([\d.]+)",
        r"CTR[:\s]+([\d.]+)%?"))
    avg_dur = to_float(extract_metric(text,
        r"\|\s*Avg view duration %\s*\|\s*([\d.]+)",
        r"[Aa]vg\s+view\s+duration\s+%[:\s]+([\d.]+)"))
    watch = to_float(extract_metric(text,
        r"\|\s*Watch time[^|]*\|\s*([\d,]+)",
        r"[Ww]atch\s+time[:\s]+([\d,]+)"))
    likes = to_float(extract_metric(text,
        r"\|\s*Likes\s*\|\s*([\d,]+)",
        r"Likes[:\s]+([\d,]+)"))
    comments = to_float(extract_metric(text,
        r"\|\s*Comments\s*\|\s*([\d,]+)",
        r"Comments[:\s]+([\d,]+)"))
    subs = to_float(extract_metric(text,
        r"\|\s*Subscribers gained\s*\|\s*([+\-]?[\d,]+)",
        r"[Ss]ubs(?:cribers?)?\s+gained[:\s]+([+\-]?[\d,]+)"))

    return {
        "views": views,
        "ctr": ctr,
        "avg_duration": avg_dur,
        "watch_time_min": watch,
        "likes": likes,
        "comments": comments,
        "subscribers": subs,
    }


def fmt(n, suffix="", sign=False):
    if n is None:
        return "N/A"
    if sign and n >= 0:
        prefix = "+"
    else:
        prefix = ""
    if n == int(n):
        return f"{prefix}{int(n):,}{suffix}"
    return f"{prefix}{n:,.1f}{suffix}"


def rank_section(rows, key, suffix="", higher_is_better=True):
    ranked = [(r["title"], r["metrics"].get(key), r["snapshot"]) for r in rows if r["metrics"].get(key) is not None]
    ranked.sort(key=lambda x: x[1], reverse=higher_is_better)
    if not ranked:
        return "  No data available"
    lines = []
    for i, (title, val, snap) in enumerate(ranked, 1):
        snap_str = f" ({snap})" if snap else ""
        lines.append(f"{i}. \"{title}\" — {fmt(val, suffix)}{snap_str}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", required=True, help="YYYY-MM")
    args = parser.parse_args()

    month_str = args.month
    try:
        year, month = int(month_str[:4]), int(month_str[5:7])
    except (ValueError, IndexError):
        print("Error: --month must be YYYY-MM (e.g. 2026-05)")
        sys.exit(1)

    output_path = os.path.join(ANALYTICS_DIR, f"{month_str}-monthly.md")

    if os.path.isfile(output_path):
        print(f"Rollup already exists (Rule R7 — generate once): {output_path}")
        sys.exit(0)

    if not os.path.isfile(UPLOAD_LOG):
        print("No upload_log.md found. Publish videos first.")
        sys.exit(1)

    all_videos = parse_upload_log(UPLOAD_LOG)
    month_videos = [v for v in all_videos if v["publish_date"].startswith(month_str)]

    if not month_videos:
        print(f"No videos published in {month_str} — nothing to assemble.")
        sys.exit(0)

    month_name = date(year, month, 1).strftime("%B %Y")
    rows = []

    for v in month_videos:
        pid = v["project_id"]
        d30 = os.path.join(ANALYTICS_DIR, pid, f"{pid}_analytics_d30.md")
        d07 = os.path.join(ANALYTICS_DIR, pid, f"{pid}_analytics_d07.md")

        if os.path.isfile(d30):
            snap_path, snap_label = d30, "d30"
        elif os.path.isfile(d07):
            snap_path, snap_label = d07, "d07"
        else:
            snap_path, snap_label = None, None

        metrics = parse_snapshot(snap_path) if snap_path else {}
        rows.append({**v, "metrics": metrics, "snapshot": snap_label})

    no_data = [r for r in rows if r["snapshot"] is None]

    def safe_sum(key):
        vals = [r["metrics"][key] for r in rows if r["metrics"].get(key) is not None]
        return sum(vals) if vals else None

    total_views = safe_sum("views")
    total_watch = safe_sum("watch_time_min")
    total_subs = safe_sum("subscribers")

    underperformers = []
    for r in rows:
        m = r["metrics"]
        reasons = []
        if m.get("ctr") is not None and m["ctr"] < UNDERPERFORM_CTR:
            reasons.append(f"CTR {m['ctr']:.1f}% < 4%")
        if m.get("avg_duration") is not None and m["avg_duration"] < UNDERPERFORM_DURATION:
            reasons.append(f"avg duration {m['avg_duration']:.0f}% < 40%")
        if reasons:
            underperformers.append(f"  - \"{r['title']}\": {', '.join(reasons)}")

    md_lines = [
        f"# {month_name} — Monthly Channel Summary",
        "",
        f"Videos published this month: {len(month_videos)}",
        f"Total views: {fmt(total_views)}",
        f"Total watch time: {fmt(total_watch, ' min')}",
        f"Net subscribers: {fmt(total_subs, sign=True)}",
        "",
        "## Video Rankings",
        "",
        "### By avg view duration %",
        rank_section(rows, "avg_duration", "%"),
        "",
        "### By CTR",
        rank_section(rows, "ctr", "%"),
        "",
        "### By subscribers gained",
        rank_section(rows, "subscribers", " subs", higher_is_better=True),
    ]

    if underperformers:
        md_lines += ["", "## Underperformers (flag for Ideation review)", ""]
        md_lines += underperformers
    else:
        md_lines += ["", "## Underperformers", "", "None — all videos within acceptable ranges."]

    if no_data:
        md_lines += ["", "## Missing Snapshots", ""]
        for r in no_data:
            md_lines.append(f"  - \"{r['title']}\" ({r['project_id']}) — no snapshot fetched yet")

    md_lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"Monthly rollup saved: {output_path}")


if __name__ == "__main__":
    main()
