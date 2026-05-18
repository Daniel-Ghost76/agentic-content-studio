#!/usr/bin/env python3
"""
Usage: python3 validate_publish_pairs.py
Scans Youtube/Output/7. Publishing/ for canonical publish pairs.

A valid pair requires both files at the root of a project subfolder
(NOT inside a published/ subfolder):
  {project_id}_publish.mp4
  {project_id}_metadata.yaml

Exit code 0 = at least one pair is ready. Exit code 1 = none ready.
"""
import os
import sys

WORKSPACE_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
)
PUBLISHING_DIR = os.path.join(WORKSPACE_ROOT, "Youtube", "Output", "7. Publishing")


def main():
    if not os.path.isdir(PUBLISHING_DIR):
        print(f"Error: Publishing folder not found: {PUBLISHING_DIR}")
        sys.exit(1)

    ready = []
    incomplete = []
    already_published = []

    try:
        entries = sorted(os.scandir(PUBLISHING_DIR), key=lambda e: e.name)
    except OSError as e:
        print(f"Error reading Publishing folder: {e}")
        sys.exit(1)

    for entry in entries:
        if not entry.is_dir():
            continue
        project_id = entry.name
        folder = entry.path

        published_dir = os.path.join(folder, "published")

        expected_mp4 = f"{project_id}_publish.mp4"
        expected_yaml = f"{project_id}_metadata.yaml"

        # Check if already published (both files in published/ subfolder)
        in_pub_mp4 = os.path.isfile(os.path.join(published_dir, expected_mp4))
        in_pub_yaml = os.path.isfile(os.path.join(published_dir, expected_yaml))
        if in_pub_mp4 and in_pub_yaml:
            already_published.append(project_id)
            continue

        # Check root of project folder
        root_files = {f.name for f in os.scandir(folder) if f.is_file()}
        has_mp4 = expected_mp4 in root_files
        has_yaml = expected_yaml in root_files

        if has_mp4 and has_yaml:
            ready.append(project_id)
        else:
            missing = []
            if not has_mp4:
                missing.append(expected_mp4)
            if not has_yaml:
                missing.append(expected_yaml)
            if missing:
                incomplete.append((project_id, missing))

    print("Publishing folder scan:")
    print()

    if ready:
        print(f"READY ({len(ready)}):")
        for pid in ready:
            print(f"  OK  {pid}")
    else:
        print("READY: none")

    print()

    if incomplete:
        print(f"INCOMPLETE ({len(incomplete)}):")
        for pid, missing in incomplete:
            print(f"  --  {pid}  missing: {', '.join(missing)}")
    else:
        print("INCOMPLETE: none")

    if already_published:
        print()
        print(f"ALREADY PUBLISHED ({len(already_published)}) — skipped:")
        for pid in already_published:
            print(f"      {pid}")

    print()

    if not ready:
        print("No videos ready to publish.")
        sys.exit(1)
    else:
        print(f"{len(ready)} video(s) ready for upload.")
        sys.exit(0)


if __name__ == "__main__":
    main()
