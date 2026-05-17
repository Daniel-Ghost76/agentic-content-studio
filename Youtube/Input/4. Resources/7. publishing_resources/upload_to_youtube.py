#!/usr/bin/env python3
"""
Upload a single video to YouTube using the YouTube Data API v3.

Usage:
    python3 upload_to_youtube.py --video <path> --metadata <path.yaml> --schedule-at <ISO8601>

    --schedule-at  RFC 3339 datetime to schedule the video, e.g. 2026-05-15T16:00:00+01:00
                   The video is uploaded as private and auto-publishes at that time.

Outputs on success:
    VIDEO_ID=<id>
    VIDEO_URL=https://www.youtube.com/watch?v=<id>
    SCHEDULED_AT=<datetime>   (only when --schedule-at was used)

Credentials:
    Place credentials.json (OAuth2 Desktop client) at:
    Youtube/Resources/publishing/credentials.json
    On first run a browser opens for Google sign-in; token.json is saved for future runs.
"""

import argparse
import os
import sys
import time
import yaml

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = [
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, "credentials.json")
TOKEN_FILE = os.path.join(SCRIPT_DIR, "token.json")

RETRIABLE_STATUS_CODES = {500, 502, 503, 504}
MAX_RETRIES = 10


def validate_canonical_pair(video_path, metadata_path):
    video_dir = os.path.dirname(os.path.abspath(video_path))
    project_id = os.path.basename(video_dir)
    expected_video = f"{project_id}_publish.mp4"
    expected_metadata = f"{project_id}_metadata.yaml"

    if os.path.basename(video_path) != expected_video:
        print(
            f"ERROR: expected canonical video filename {expected_video}, got {os.path.basename(video_path)}",
            file=sys.stderr,
        )
        sys.exit(1)

    if os.path.basename(metadata_path) != expected_metadata:
        print(
            f"ERROR: expected canonical metadata filename {expected_metadata}, got {os.path.basename(metadata_path)}",
            file=sys.stderr,
        )
        sys.exit(1)

    if os.path.dirname(os.path.abspath(metadata_path)) != video_dir:
        print("ERROR: video and metadata must be in the same project folder.", file=sys.stderr)
        sys.exit(1)

    return project_id


def get_authenticated_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(
                    f"ERROR: credentials.json not found at {CREDENTIALS_FILE}\n"
                    "Setup:\n"
                    "  1. Go to console.cloud.google.com → create a project\n"
                    "  2. Enable YouTube Data API v3\n"
                    "  3. Create OAuth 2.0 credentials → Desktop app\n"
                    f"  4. Download and save as {CREDENTIALS_FILE}",
                    file=sys.stderr,
                )
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def load_metadata(yaml_path):
    with open(yaml_path, "r") as f:
        meta = yaml.safe_load(f)

    for key in ("title", "description"):
        if not meta.get(key):
            print(f"ERROR: metadata missing required field: '{key}'", file=sys.stderr)
            sys.exit(1)

    return {
        "title": meta["title"],
        "description": meta["description"],
        "tags": meta.get("tags", []),
        "category_id": str(meta.get("category_id", "28")),
        "privacy": meta.get("privacy", "public"),
        "made_for_kids": meta.get("made_for_kids", False),
        "thumbnail": meta.get("thumbnail"),
    }


def upload_video(youtube, video_path, metadata, schedule_at=None):
    if schedule_at:
        status_body = {
            "privacyStatus": "private",
            "publishAt": schedule_at,
            "selfDeclaredMadeForKids": metadata["made_for_kids"],
        }
    else:
        status_body = {
            "privacyStatus": metadata["privacy"],
            "selfDeclaredMadeForKids": metadata["made_for_kids"],
        }

    body = {
        "snippet": {
            "title": metadata["title"],
            "description": metadata["description"],
            "tags": metadata["tags"],
            "categoryId": metadata["category_id"],
        },
        "status": status_body,
    }

    media = MediaFileUpload(
        video_path,
        chunksize=10 * 1024 * 1024,  # 10 MB chunks
        resumable=True,
    )

    request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=media,
    )

    print(f"Uploading: {os.path.basename(video_path)}")
    response = None
    retry = 0

    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                pct = int(status.progress() * 100)
                print(f"  {pct}% uploaded...", end="\r", flush=True)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                retry += 1
                if retry > MAX_RETRIES:
                    print(f"\nERROR: Upload failed after {MAX_RETRIES} retries.", file=sys.stderr)
                    sys.exit(1)
                wait = 2 ** retry
                print(f"\n  HTTP {e.resp.status} — retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"\nERROR: {e}", file=sys.stderr)
                sys.exit(1)

    print()
    return response["id"]


def set_thumbnail(youtube, video_id, thumbnail_path):
    media = MediaFileUpload(thumbnail_path, resumable=True)
    youtube.thumbnails().set(videoId=video_id, media_body=media).execute()
    print(f"  Thumbnail set: {os.path.basename(thumbnail_path)}")


def main():
    parser = argparse.ArgumentParser(description="Upload a video to YouTube.")
    parser.add_argument("--video", required=True, help="Path to {project_id}_publish.mp4")
    parser.add_argument("--metadata", required=True, help="Path to {project_id}_metadata.yaml")
    parser.add_argument(
        "--schedule-at",
        dest="schedule_at",
        required=True,
        help="RFC 3339 datetime to schedule (e.g. 2026-05-15T16:00:00+01:00). "
             "Uploads as private and auto-publishes at this time.",
    )
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"ERROR: video file not found: {args.video}", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.metadata):
        print(f"ERROR: metadata file not found: {args.metadata}", file=sys.stderr)
        sys.exit(1)

    project_id = validate_canonical_pair(args.video, args.metadata)
    metadata = load_metadata(args.metadata)
    youtube = get_authenticated_service()

    video_id = upload_video(youtube, args.video, metadata, schedule_at=args.schedule_at)

    print(f"Upload complete!")
    print(f"PROJECT_ID={project_id}")
    print(f"VIDEO_ID={video_id}")
    print(f"VIDEO_URL=https://www.youtube.com/watch?v={video_id}")

    if args.schedule_at:
        print(f"SCHEDULED_AT={args.schedule_at}")

    if metadata["thumbnail"]:
        thumb_dir = os.path.dirname(args.video)
        thumb_path = os.path.join(thumb_dir, metadata["thumbnail"])
        if os.path.exists(thumb_path):
            set_thumbnail(youtube, video_id, thumb_path)
        else:
            print(f"  WARNING: thumbnail not found at {thumb_path}, skipping.")


if __name__ == "__main__":
    main()
