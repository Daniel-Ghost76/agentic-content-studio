#!/usr/bin/env python3
"""
Usage: python3 validate_yaml.py <path/to/{project_id}_metadata.yaml>
Validates a YouTube metadata YAML file before upload.

Rules (publishing_rules.md + scripting_rules.md):
  - title: required, <= 100 chars
  - description: required, <= 5000 chars, first 150 chars must not open with forbidden phrases
  - category_id: must be "28"
  - made_for_kids: must be false (boolean)
  - tags field: must NOT be present
  - privacy field: must NOT be present

Exit code 0 = PASS. Exit code 1 = FAIL.
"""
import sys
import os
import re

try:
    import yaml as _yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

FORBIDDEN_OPENERS = [
    "in this video",
    "in this tutorial",
    "welcome to",
    "hey guys",
    "hello everyone",
    "today we",
    "today i",
]


def _parse_fallback(text: str) -> dict:
    """
    Minimal YAML parser for the specific metadata.yaml structure used in this pipeline.
    Handles: scalar strings (quoted or unquoted), block scalars (|), and booleans.
    Not a general YAML parser — only covers what this project produces.
    """
    data = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        # Skip blank lines and comments
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        # Top-level key: value
        m = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.*)', line)
        if not m:
            i += 1
            continue
        key = m.group(1)
        rest = m.group(2).strip()
        if rest == "|":
            # Block scalar — collect indented lines
            i += 1
            block_lines = []
            while i < len(lines) and (lines[i].startswith("  ") or lines[i].strip() == ""):
                block_lines.append(lines[i][2:] if lines[i].startswith("  ") else "")
                i += 1
            data[key] = "\n".join(block_lines).rstrip()
        elif rest in ("true", "false"):
            data[key] = rest == "true"
        elif rest.startswith('"') and rest.endswith('"'):
            data[key] = rest[1:-1]
        elif rest.startswith("'") and rest.endswith("'"):
            data[key] = rest[1:-1]
        else:
            data[key] = rest
            i += 1
            continue
        # Don't double-increment for block scalar case
        if rest != "|":
            i += 1
    return data


def _load(path: str):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if _HAS_YAML:
        try:
            data = _yaml.safe_load(text)
            if isinstance(data, dict):
                return data, None
        except Exception as e:
            return None, f"YAML parse error: {e}"
    return _parse_fallback(text), None


def validate(path: str):
    data, err = _load(path)
    if err:
        return [err]
    if not isinstance(data, dict):
        return ["File did not parse as a YAML mapping — check formatting"]

    issues = []

    # title
    title = data.get("title")
    if not title:
        issues.append("title: missing")
    elif len(str(title)) > 100:
        issues.append(f"title: {len(str(title))} chars — must be <= 100")

    # description
    desc = data.get("description")
    if not desc:
        issues.append("description: missing")
    else:
        desc_str = str(desc)
        if len(desc_str) > 5000:
            issues.append(f"description: {len(desc_str)} chars — must be <= 5000")
        first_150 = desc_str[:150].lower().strip()
        for opener in FORBIDDEN_OPENERS:
            if first_150.startswith(opener):
                issues.append(f"description: opens with forbidden phrase '{opener}'")
                break

    # category_id
    cat = data.get("category_id")
    if cat is None:
        issues.append("category_id: missing (must be '28')")
    elif str(cat) != "28":
        issues.append(f"category_id: '{cat}' — must be '28'")

    # made_for_kids
    mfk = data.get("made_for_kids")
    if mfk is None:
        issues.append("made_for_kids: missing (must be false)")
    elif mfk is not False:
        issues.append(f"made_for_kids: '{mfk}' — must be boolean false")

    # forbidden fields
    if "tags" in data:
        issues.append("tags: field must be omitted entirely (Rule R13 — never include tags)")
    if "privacy" in data:
        issues.append("privacy: field must be omitted (publishing script handles scheduling)")

    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_yaml.py <metadata.yaml>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"Error: file not found: {path}")
        sys.exit(1)

    print(f"Validating: {os.path.basename(path)}")
    print()

    issues = validate(path)

    if not issues:
        print("PASS — all checks passed, ready for upload")
        sys.exit(0)
    else:
        print(f"FAIL — {len(issues)} issue(s) to fix before uploading:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)


if __name__ == "__main__":
    main()
