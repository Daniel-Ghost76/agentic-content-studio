#!/usr/bin/env python3
"""
thumbnail_scraper.py

Downloads YouTube thumbnails for a list of channel handles using yt-dlp.
Saves images and a manifest to the reference_thumbnails library.

Usage:
    python3 thumbnail_scraper.py @nateherk @liamottley @nicksaraev
    python3 thumbnail_scraper.py @nateherk --max 20
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

OUTPUT_ROOT = (
    Path(__file__).parents[2]
    / "4. Resources"
    / "6. review_resources"
    / "reference_thumbnails"
)


def check_ytdlp() -> None:
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        sys.exit("[ERROR] yt-dlp not found. Install with: brew install yt-dlp")


def fetch_channel_info(handle: str, max_videos: int) -> list[dict]:
    handle_clean = handle.lstrip("@")
    url = f"https://www.youtube.com/@{handle_clean}/videos"
    print(f"\n=== @{handle_clean} ===")
    print(f"Fetching video list from {url} ...")

    result = subprocess.run(
        [
            "yt-dlp",
            "--flat-playlist",
            "-J",
            "--playlist-end",
            str(max_videos),
            url,
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        print(f"[WARN] yt-dlp returned non-zero for @{handle_clean}: {result.stderr[:200]}")
        return []

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Could not parse yt-dlp JSON for @{handle_clean}: {e}")
        return []

    entries = data.get("entries") or []
    videos = []
    for entry in entries:
        if not entry:
            continue
        video_id = entry.get("id") or entry.get("url", "").split("v=")[-1]
        if not video_id:
            continue
        videos.append(
            {
                "video_id": video_id,
                "title": entry.get("title", ""),
                "published_at": entry.get("upload_date", ""),
                "view_count": entry.get("view_count") or 0,
                "thumbnail_url": f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg",
                "channel_title": entry.get("channel") or entry.get("uploader") or handle_clean,
            }
        )
    return videos


def download_thumbnails(videos: list[dict], out_dir: Path) -> int:
    import urllib.request

    downloaded = 0
    for v in videos:
        dest = out_dir / f"{v['video_id']}.jpg"
        if dest.exists():
            print(f"  [SKIP] {dest.name}")
            continue
        url = v["thumbnail_url"]
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
            # maxresdefault can return a 404-style placeholder for some videos
            # fall back to hqdefault if file is very small (under 5KB)
            if len(data) < 5000:
                fallback = f"https://i.ytimg.com/vi/{v['video_id']}/hqdefault.jpg"
                req2 = urllib.request.Request(fallback, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req2, timeout=15) as resp2:
                    data = resp2.read()
                v["thumbnail_url"] = fallback
            dest.write_bytes(data)
            print(f"  [OK]   {dest.name}  — {v['title'][:60]}")
            downloaded += 1
        except Exception as e:
            print(f"  [FAIL] {v['video_id']} — {e}")
    return downloaded


def scrape_channel(handle: str, max_videos: int) -> None:
    handle_clean = handle.lstrip("@")
    videos = fetch_channel_info(handle, max_videos)
    if not videos:
        print(f"[WARN] No videos found for @{handle_clean}. Skipping.")
        return

    out_dir = OUTPUT_ROOT / handle_clean
    out_dir.mkdir(parents=True, exist_ok=True)

    downloaded = download_thumbnails(videos, out_dir)

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(videos, indent=2, ensure_ascii=False))
    print(f"Manifest saved → {manifest_path}")
    print(f"Downloaded {downloaded} new thumbnails ({len(videos)} total entries).")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download YouTube channel thumbnails for the reference library."
    )
    parser.add_argument("handles", nargs="+", help="Channel handles, e.g. @nateherk @liamottley")
    parser.add_argument("--max", type=int, default=17, help="Max recent videos per channel (default: 17)")
    args = parser.parse_args()

    check_ytdlp()
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    for handle in args.handles:
        scrape_channel(handle, args.max)

    print("\nDone. Reference library at:")
    print(f"  {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()
