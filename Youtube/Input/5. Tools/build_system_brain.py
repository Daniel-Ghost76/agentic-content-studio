#!/usr/bin/env python3
"""
build_system_brain.py — merge the workspace's prose knowledge (CLAUDE.md + every
stage SOP/Skill/Rules) into ONE structured PDF for drag-and-drop into NotebookLM.

Why a single PDF: NotebookLM caps free notebooks at 50 sources and only ingests
PDF/Docs/Slides/URL/YouTube/audio — not .py/.json/.md. Merging the prose into one
clean, text-extractable PDF sidesteps both limits. Code, configs, and media are
deliberately excluded — NotebookLM can't reason about them and they only dilute
retrieval. Regenerate this whenever the SOPs/Skills/Rules change; the PDF is a
frozen snapshot, not a live mirror.

stdlib only. Renders via Chrome headless. Output: Youtube/Quick Access/system_brain.pdf
"""
import datetime
import html
import os
import re
import subprocess
import sys

ROOT = "/Users/danieldanut/Agentic Workspace"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT_PDF = os.path.join(ROOT, "Youtube/Quick Access/system_brain.pdf")
TMP_HTML = os.path.join(ROOT, "Youtube/Quick Access/.system_brain.tmp.html")

CATEGORIES = [("SOP", "Youtube/Input/1. SOPs"),
              ("Skill", "Youtube/Input/2. Skills"),
              ("Rules", "Youtube/Input/3. Rules")]


def stage_key(stage_folder):
    m = re.match(r"\s*(\d+)", stage_folder)
    return (int(m.group(1)) if m else 999, stage_folder)


def collect():
    """Return ordered list of (section_title, rel_path, text)."""
    items = [("Workspace Charter — CLAUDE.md", ".claude/CLAUDE.md")]

    # stage -> {category -> [rel_paths]}
    stages = {}
    for cat, base in CATEGORIES:
        base_abs = os.path.join(ROOT, base)
        for dirpath, _, files in os.walk(base_abs):
            for fn in sorted(files):
                if fn.startswith(".") or not fn.endswith(".md"):
                    continue
                rel = os.path.relpath(os.path.join(dirpath, fn), ROOT)
                parts = rel.split(os.sep)
                # parts: Youtube, Input, '<n>. SOPs', '<stage folder>', ...file
                if len(parts) < 5:
                    continue  # skip stray files not inside a stage folder
                stage_folder = parts[3]
                stages.setdefault(stage_folder, {}).setdefault(cat, []).append((fn, rel))

    ordered = items[:]
    for stage_folder in sorted(stages, key=stage_key):
        for cat, _ in CATEGORIES:
            for fn, rel in sorted(stages[stage_folder].get(cat, [])):
                title = f"{stage_folder} — {cat}: {fn}"
                ordered.append((title, rel))

    result = []
    for title, rel in ordered:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            result.append((title, rel, f.read()))
    return result


# ---- minimal, dependable markdown -> HTML ----
def inline(s):
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", s)  # keep link text, drop URL
    return s


def md_to_html(md):
    lines = md.split("\n")
    out, i, n = [], 0, len(md and lines)
    para = []

    def flush():
        if para:
            txt = " ".join(para).strip()
            if txt:
                out.append("<p>" + inline(txt) + "</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        # fenced code
        if line.lstrip().startswith("```"):
            flush()
            i += 1
            buf = []
            while i < len(lines) and not lines[i].lstrip().startswith("```"):
                buf.append(html.escape(lines[i]))
                i += 1
            i += 1
            out.append("<pre><code>" + "\n".join(buf) + "</code></pre>")
            continue
        # table
        if "|" in line and i + 1 < len(lines) and re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]*$", lines[i + 1]):
            flush()
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            out.append("<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in header) + "</tr></thead><tbody>")
            i += 2
            while i < len(lines) and "|" in lines[i]:
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
                i += 1
            out.append("</tbody></table>")
            continue
        # heading
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush()
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2).strip())}</h{lvl}>")
            i += 1
            continue
        # hr
        if re.match(r"^\s*([-*_])\1\1+\s*$", line):
            flush()
            out.append("<hr>")
            i += 1
            continue
        # unordered list
        if re.match(r"^\s*[-*]\s+", line):
            flush()
            out.append("<ul>")
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                item = re.sub(r"^\s*[-*]\s+", "", lines[i])
                out.append("<li>" + inline(item) + "</li>")
                i += 1
            out.append("</ul>")
            continue
        # ordered list
        if re.match(r"^\s*\d+\.\s+", line):
            flush()
            out.append("<ol>")
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                item = re.sub(r"^\s*\d+\.\s+", "", lines[i])
                out.append("<li>" + inline(item) + "</li>")
                i += 1
            out.append("</ol>")
            continue
        # blank
        if not line.strip():
            flush()
            i += 1
            continue
        para.append(line.strip())
        i += 1
    flush()
    return "\n".join(out)


CSS = """
body{font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;font-size:12px;line-height:1.5;color:#111;max-width:820px;margin:0 auto;padding:24px;}
h1{font-size:24px;border-bottom:2px solid #333;padding-bottom:6px;}
h2{font-size:18px;margin-top:22px;}
h3{font-size:15px;}
code{background:#f2f2f2;padding:1px 4px;border-radius:3px;font-size:11px;}
pre{background:#f6f8fa;padding:10px;border-radius:6px;overflow:auto;}
pre code{background:none;padding:0;}
table{border-collapse:collapse;width:100%;margin:10px 0;}
th,td{border:1px solid #ccc;padding:4px 8px;text-align:left;font-size:11px;}
th{background:#f0f0f0;}
hr{border:none;border-top:1px solid #ddd;margin:16px 0;}
.section{page-break-before:always;border-top:3px solid #333;margin-top:32px;padding-top:8px;}
.section .src{color:#888;font-size:10px;font-family:monospace;margin:0 0 8px;}
.cover{page-break-after:always;}
.toc li{font-size:11px;margin:2px 0;}
.note{background:#fff8e1;border:1px solid #f0d000;padding:10px;border-radius:6px;font-size:11px;}
"""


def build():
    sections = collect()
    today = datetime.date.today().isoformat()
    parts = [f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"]
    # cover + TOC
    parts.append("<div class='cover'>")
    parts.append("<h1>YouTube Content System — Brain</h1>")
    parts.append(f"<p class='note'><strong>Generated {today}.</strong> This is a frozen snapshot of the workspace's "
                 "operating docs (CLAUDE.md + every stage SOP, Skill, and Rules file). It deliberately excludes all "
                 "code, configs, and media — NotebookLM can't reason about those. Regenerate after the source docs "
                 "change: <code>python3 \"Youtube/Input/5. Tools/build_system_brain.py\"</code></p>")
    parts.append(f"<p>{len(sections)} documents merged.</p>")
    parts.append("<h2>Contents</h2><ol class='toc'>")
    for title, _, _ in sections:
        parts.append(f"<li>{html.escape(title)}</li>")
    parts.append("</ol></div>")
    # sections
    for title, rel, text in sections:
        parts.append(f"<div class='section'><h2>{html.escape(title)}</h2><p class='src'>{html.escape(rel)}</p>")
        parts.append(md_to_html(text))
        parts.append("</div>")
    parts.append("</body></html>")

    with open(TMP_HTML, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))

    try:
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={OUT_PDF}", f"file://{TMP_HTML}"],
                       check=True, capture_output=True, timeout=120)
    except subprocess.TimeoutExpired:
        # old headless can hang after writing the PDF; the file is already complete
        subprocess.run(["pkill", "-f", f"print-to-pdf={OUT_PDF}"], capture_output=True)
    finally:
        if os.path.exists(TMP_HTML):
            os.remove(TMP_HTML)
    if not os.path.exists(OUT_PDF) or os.path.getsize(OUT_PDF) < 10000:
        sys.exit("ERROR: PDF was not written correctly.")
    size = os.path.getsize(OUT_PDF)
    print(f"OK: {OUT_PDF}  ({len(sections)} docs, {size//1024} KB)")


if __name__ == "__main__":
    if not os.path.exists(CHROME):
        sys.exit("ERROR: Chrome not found at expected path.")
    build()
