#!/usr/bin/env python3
"""
Usage: python3 scaffold_project.py <project_id>
Creates all 9 Output stage folders for a given project_id if they don't exist.
Run this immediately after Draft 1 is written.
"""
import sys
import os

WORKSPACE_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
)

STAGES = [
    "1. Ideation",
    "2. Scripts",
    "3. Pre-production Materials",
    "4. Editing",
    "5. Visuals",
    "6. Review  ",
    "7. Publishing",
    "8. Distribution",
    "9. Analytics",
]


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scaffold_project.py <project_id>")
        sys.exit(1)

    project_id = sys.argv[1].strip()
    output_root = os.path.join(WORKSPACE_ROOT, "Youtube", "Output")

    print(f"Scaffolding output folders for: {project_id}")
    print()

    for stage in STAGES:
        path = os.path.join(output_root, stage, project_id)
        if os.path.isdir(path):
            print(f"  EXISTS   {stage}/{project_id}")
        else:
            os.makedirs(path)
            print(f"  CREATED  {stage}/{project_id}")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
