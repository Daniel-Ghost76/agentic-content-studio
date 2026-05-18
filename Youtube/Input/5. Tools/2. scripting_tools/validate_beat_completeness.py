#!/usr/bin/env python3
"""
Usage: python3 validate_beat_completeness.py <path/to/draft.txt>
       cat draft.txt | python3 validate_beat_completeness.py

Checks every beat/section block in a script draft for:
  - A visual cue (*[Screen:...]*  or similar annotation)
  - A word-count target (~Xw)
  - Non-empty body text (the Point)

Exit code 0 = all pass. Exit code 1 = issues found.
"""
import sys
import re
import os


SECTION_PATTERN = re.compile(
    r"^##\s+(HOOK|PROMISE|CREDENTIAL|BODY|BEAT\s+\d+|WRAP|CTA|[A-Z][A-Z\s]+\d*).*$",
    re.MULTILINE | re.IGNORECASE,
)


def check_beat(header: str, body: str):
    issues = []

    # Visual cue check
    has_visual = bool(
        re.search(r"\*\[Screen:", body)
        or re.search(r"\*\[Visual:", body)
        or re.search(r"\*\[Cut to", body, re.IGNORECASE)
        or re.search(r"\*\[Show", body, re.IGNORECASE)
        or re.search(r"on.?screen", body, re.IGNORECASE)
        or re.search(r"TH\b|LIVE\b", body)
    )
    if not has_visual:
        issues.append("no visual cue (*[Screen:...]*  or TH/LIVE tag)")

    # Word-count target check
    has_word_count = bool(
        re.search(r"~\d+\s*w\b", body, re.IGNORECASE)
        or re.search(r"\b\d+\s*words?\b", body, re.IGNORECASE)
        or re.search(r"\(~?\d+w\)", body, re.IGNORECASE)
    )
    if not has_word_count:
        issues.append("no word-count target (~Xw)")

    # Non-empty body
    stripped = re.sub(r"\*\[.*?\]\*", "", body).strip()
    stripped = re.sub(r"\*\*.*?\*\*", "", stripped).strip()
    if len(stripped) < 30:
        issues.append("body appears empty — add the Point text")

    return issues


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if not os.path.isfile(path):
            print(f"Error: file not found: {path}")
            sys.exit(1)
        with open(path, encoding="utf-8") as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    matches = list(SECTION_PATTERN.finditer(content))

    if not matches:
        print("No section headers found (expected ## HOOK, ## BEAT 1, ## WRAP, etc.).")
        print("PASS — nothing to validate.")
        sys.exit(0)

    beats = []
    for i, m in enumerate(matches):
        header = m.group(0).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        body = content[start:end]
        beats.append((header, body))

    all_pass = True
    for header, body in beats:
        issues = check_beat(header, body)
        if issues:
            all_pass = False
            print(f"FAIL  {header}")
            for issue in issues:
                print(f"      - {issue}")
        else:
            print(f"PASS  {header}")

    print()
    if all_pass:
        print("All beats complete. Safe to generate Draft 2.")
        sys.exit(0)
    else:
        print("Fix the above before generating Draft 2.")
        sys.exit(1)


if __name__ == "__main__":
    main()
