#!/usr/bin/env python3
"""
Fetch YouTube Analytics for a single video and save a Markdown snapshot.

Usage:
    python3 fetch_analytics.py \
        --project-id <NN_slug> \
        --video-id <ID> \
        --title "<Title>" \
        --published <YYYY-MM-DD> \
        --snapshot d07|d30 \
        --output-dir <path>

    --project-id  Canonical project ID, e.g. 02_codex_mobile
    --video-id    YouTube video ID (e.g. I_8GpWlf6oc)
    --title       Video title (used in the snapshot header)
    --published   Date the video went live on YouTube (YYYY-MM-DD)
    --snapshot    d07 = 7-day snapshot, d30 = 30-day snapshot
    --output-dir  Folder to save the .md file (default: Youtube/Output/9. Analytics/)

Saves: {output-dir}/{project-id}/{project-id}_analytics_{snapshot}.md
"""

import argparse
import os
import sys
from datetime import date, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, "credentials.json")
TOKEN_FILE = os.path.join(SCRIPT_DIR, "token.json")

WORKSPACE_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
DEFAULT_OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, "Youtube", "Output", "9. Analytics")


def get_authenticated_services():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None

    if not creds or not creds.valid:
        if not os.path.exists(CREDENTIALS_FILE):
            print(f"ERROR: credentials.json not found at {CREDENTIALS_FILE}", file=sys.stderr)
            sys.exit(1)
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    youtube = build("youtube", "v3", credentials=creds)
    yt_analytics = build("youtubeAnalytics", "v2", credentials=creds)
    return youtube, yt_analytics


def get_video_title_from_api(youtube, video_id):
    try:
        resp = youtube.videos().list(part="snippet", id=video_id).execute()
        items = resp.get("items", [])
        if items:
            return items[0]["snippet"]["title"]
    except HttpError:
        pass
    return None


def fetch_video_metrics(yt_analytics, video_id, start_date, end_date):
    try:
        resp = yt_analytics.reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics=(
                "views,"
                "estimatedMinutesWatched,"
                "averageViewDuration,"
                "averageViewPercentage,"
                "likes,"
                "comments,"
                "subscribersGained,"
                "impressions,"
                "impressionClickThroughRate"
            ),
            filters=f"video=={video_id}",
        ).execute()
    except HttpError as e:
        print(f"ERROR fetching metrics: {e}", file=sys.stderr)
        sys.exit(1)

    rows = resp.get("rows")
    if not rows:
        return None

    headers = [col["name"] for col in resp["columnHeaders"]]
    row = rows[0]
    return dict(zip(headers, row))


def fetch_top_traffic_source(yt_analytics, video_id, start_date, end_date):
    try:
        resp = yt_analytics.reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            dimensions="insightTrafficSourceType",
            metrics="views",
            filters=f"video=={video_id}",
            sort="-views",
            maxResults=1,
        ).execute()
    except HttpError:
        return "N/A"

    rows = resp.get("rows")
    if not rows:
        return "N/A"

    source_map = {
        "YT_SEARCH": "YouTube search",
        "SUGGESTED_VIDEO": "Suggested videos",
        "BROWSE_FEATURES": "Browse / homepage",
        "EXTERNAL": "External (social/web)",
        "NOTIFICATION": "Notifications",
        "PLAYLIST": "Playlist",
        "CHANNEL": "Channel page",
        "OTHER": "Other",
    }
    raw = rows[0][0]
    return source_map.get(raw, raw)


def format_snapshot(project_id, video_id, title, published, snapshot_label, metrics, top_source, end_date):
    days = 7 if snapshot_label == "d07" else 30
    label = f"Day {days}"

    views = int(metrics.get("views", 0))
    watch_min = int(metrics.get("estimatedMinutesWatched", 0))
    avg_dur_pct = metrics.get("averageViewPercentage", 0)
    likes = int(metrics.get("likes", 0))
    comments = int(metrics.get("comments", 0))
    subs = int(metrics.get("subscribersGained", 0))
    impressions = int(metrics.get("impressions", 0))
    ctr = metrics.get("impressionClickThroughRate", 0) * 100

    lines = [
        f"# {label} — \"{title}\"",
        "",
        f"Project ID: {project_id}",
        f"Video ID:   {video_id}",
        f"Published:  {published}",
        f"Snapshot:   {end_date}",
        "",
        "| Metric                  | Value              |",
        "|-------------------------|--------------------|",
        f"| Views                   | {views:,}             |",
        f"| Impressions             | {impressions:,}       |",
        f"| CTR                     | {ctr:.1f}%            |",
        f"| Avg view duration %     | {avg_dur_pct:.1f}%    |",
        f"| Watch time (min)        | {watch_min:,}         |",
        f"| Likes                   | {likes:,}             |",
        f"| Comments                | {comments:,}          |",
        f"| Subscribers gained      | {subs:,}              |",
        f"| Top traffic source      | {top_source}          |",
    ]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube Analytics snapshot for a video.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--video-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--published", required=True, help="YYYY-MM-DD publish date")
    parser.add_argument("--snapshot", required=True, choices=["d07", "d30"])
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    days = 7 if args.snapshot == "d07" else 30
    published = date.fromisoformat(args.published)
    end_date = min(published + timedelta(days=days), date.today() - timedelta(days=2))
    start_date = published.isoformat()
    end_date_str = end_date.isoformat()

    if end_date <= published:
        print(
            f"ERROR: YouTube Analytics data is not yet available for this window "
            f"(published {published}, need data through {published + timedelta(days=days)}).",
            file=sys.stderr,
        )
        sys.exit(1)

    project_output_dir = os.path.join(args.output_dir, args.project_id)
    output_path = os.path.join(project_output_dir, f"{args.project_id}_analytics_{args.snapshot}.md")
    if os.path.exists(output_path):
        print(f"Snapshot already exists: {output_path}")
        sys.exit(0)

    print(f"Fetching {args.snapshot} analytics for {args.video_id} ({start_date} → {end_date_str})...")

    youtube, yt_analytics = get_authenticated_services()

    metrics = fetch_video_metrics(yt_analytics, args.video_id, start_date, end_date_str)
    if metrics is None:
        print(
            f"WARNING: No analytics data returned for {args.video_id}. "
            "Data may not be available yet (YouTube Analytics has a 2-3 day delay).",
            file=sys.stderr,
        )
        sys.exit(1)

    top_source = fetch_top_traffic_source(yt_analytics, args.video_id, start_date, end_date_str)
    content = format_snapshot(
        args.project_id, args.video_id, args.title, args.published, args.snapshot, metrics, top_source, end_date_str
    )

    os.makedirs(project_output_dir, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(content)

    print(f"SNAPSHOT_SAVED={output_path}")
    print(content)


if __name__ == "__main__":
    main()
