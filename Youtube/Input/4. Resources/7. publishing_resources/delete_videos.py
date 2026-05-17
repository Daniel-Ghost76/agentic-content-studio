#!/usr/bin/env python3
"""
Delete YouTube videos by ID.

Usage:
    python3 delete_videos.py <video_id> [<video_id> ...]
"""

import os
import sys

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


def get_authenticated_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)


def main():
    if len(sys.argv) < 2:
        print("Usage: delete_videos.py <video_id> [<video_id> ...]", file=sys.stderr)
        sys.exit(1)

    youtube = get_authenticated_service()

    for video_id in sys.argv[1:]:
        try:
            youtube.videos().delete(id=video_id).execute()
            print(f"DELETED={video_id}")
        except HttpError as e:
            print(f"ERROR deleting {video_id}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
