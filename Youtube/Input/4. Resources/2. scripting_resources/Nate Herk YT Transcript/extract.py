#!/usr/bin/env python3
"""
Nate Herk transcript extraction script.
Calls Ollama (qwen2.5:32b) for each video — zero Claude tokens, zero extra cost.
Progress saved after every video — crash-safe and fully resumable.

Run: python3 extract.py
"""

import json
import re
import sys
import time
import requests
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
TRANSCRIPT_FILE = "/Users/danieldanut/Desktop/Nate Herk YT Transcript/Nate Herk YT Transcript.txt"
ANALYSIS_DIR    = Path("/Users/danieldanut/Desktop/Nate Herk YT Transcript/analysis")
PROGRESS_DIR    = ANALYSIS_DIR / "progress"
PROGRESS_FILE   = PROGRESS_DIR / "progress.json"
OLLAMA_URL      = "http://localhost:11434/api/generate"
MODEL           = "qwen2.5:7b"
NUM_CTX         = 8192
CHUNK_CHARS     = 22000  # ~5500 tokens — leaves room for prompt overhead
BATCH_SIZE      = 16

EXTRACTION_PROMPT = """\
You are extracting structured data from a YouTube transcript. Be precise and quote verbatim.

VIDEO: {title}
DATE: {date}

TRANSCRIPT:
{transcript_chunk}

Extract the following. For each item, quote EXACTLY from the transcript (word for word). If something is not present in this section, write "NOT FOUND".

1. HOOK (first 15 seconds / first ~50 words): Quote the exact opening words.
2. HOOK TYPE: Label as one of: Result-First / Contrarian / Time-Bound / Problem-Statement / Curiosity-Gap / Demonstration / Personal-Moment
3. CREDENTIAL DROP: Any mention of Nate's income, agency, experience, or background. Quote verbatim + note position in video (early/mid/late).
4. SIGNATURE PHRASES: List every instance of: "you guys", "here we go", "what's really cool", "let me hit you with", "literally insane", "let's not waste any time", "honestly", "crazy", "insane", "wild". Quote each in context (5-10 word surrounding snippet).
5. TRANSITIONS: Quote any phrase used to move between sections (e.g. intro→tutorial, step→step, body→CTA).
6. CTA / OUTRO: Quote the subscribe ask, community plug, or closing line verbatim.
7. VOCABULARY: List 5-10 distinctive words/phrases that feel specific to Nate's voice.
8. ANALOGIES: Quote any "think of it like", "imagine", "it's basically X but Y" comparisons verbatim.
9. CURIOSITY GAPS: Quote any open loops, teasers, or withheld payoffs ("I'll come back to this", "stay till the end", "here's where it gets interesting").
10. SPECIFICITY: List all dollar amounts, percentages, subscriber counts, time references, and named tools mentioned.
11. VULNERABILITY: Any admissions of mistakes, uncertainty, or failure. Quote verbatim. If none, write "NONE FOUND".
12. SCRIPT TYPE: Classify as TIGHT / LOOSE / OFF-THE-DOME based on sentence completeness and filler density.
13. ENERGY NOTES: Where does pace seem to accelerate or slow? Note topic at those moments.
14. AUDIENCE LANGUAGE: Quote any direct address phrases ("you guys", "those of you", "OGs", "if you've been with me").
15. FRAMEWORKS: Any numbered lists, step processes, or named frameworks. Quote the opening line of each.

Output ONLY valid JSON with keys: hook, hook_type, credential_drop, signature_phrases, transitions, cta, vocabulary, analogies, curiosity_gaps, specificity, vulnerability, script_type, energy_notes, audience_language, frameworks.
Do NOT include any explanation, markdown, or code fences. Start with {{ and end with }}.
"""

# ── Parse transcript ──────────────────────────────────────────────────────────
def parse_videos(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    videos = []
    # Title line: "N. Some Title (DD/MM/YY)"  — date is always the last parenthetical
    header_re = re.compile(r'^(\d+)\.\s+(.+)\s+\((\d{2}/\d{2}/\d{2})\)\s*$')

    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\n')
        m = header_re.match(line)
        if m:
            num   = int(m.group(1))
            title = m.group(2).strip()
            date  = m.group(3)
            # Transcript is the next non-empty line
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            transcript = lines[j].strip() if j < len(lines) else ''
            videos.append({
                'num':        num,
                'title':      title,
                'date':       date,
                'transcript': transcript,
                'word_count': len(transcript.split()),
            })
            i = j + 1
        else:
            i += 1

    return videos

# ── Chunk long transcripts ────────────────────────────────────────────────────
def chunk_text(text, chunk_size=CHUNK_CHARS):
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end < len(text):
            # Break on sentence boundary
            bp = text.rfind('. ', start, end)
            if bp == -1:
                bp = text.rfind(' ', start, end)
            if bp > start:
                end = bp + 1
        chunks.append(text[start:end].strip())
        start = end
    return chunks

# ── Ollama API call ───────────────────────────────────────────────────────────
def call_ollama(prompt, retries=3):
    payload = {
        "model":   MODEL,
        "prompt":  prompt,
        "stream":  False,
        "options": {"num_ctx": NUM_CTX, "temperature": 0.1},
    }
    for attempt in range(retries):
        try:
            resp = requests.post(OLLAMA_URL, json=payload, timeout=360)
            resp.raise_for_status()
            return resp.json().get('response', '')
        except Exception as e:
            wait = 15 * (attempt + 1)
            print(f"    [attempt {attempt+1}/{retries}] Error: {e} — retrying in {wait}s")
            if attempt < retries - 1:
                time.sleep(wait)
    return None

# ── Parse JSON from model response ───────────────────────────────────────────
def parse_json(text):
    if not text:
        return {"parse_error": True, "raw": ""}
    # Direct parse
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass
    # Find the outermost JSON object
    m = re.search(r'\{.*\}', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass
    return {"parse_error": True, "raw": text[:500]}

# ── Merge multi-chunk results ─────────────────────────────────────────────────
LIST_KEYS = [
    'signature_phrases', 'transitions', 'vocabulary', 'analogies',
    'curiosity_gaps', 'specificity', 'audience_language', 'frameworks',
]
FIRST_CHUNK_KEYS = ['hook', 'hook_type', 'credential_drop', 'script_type',
                    'energy_notes', 'vulnerability']

def merge_chunks(chunk_results):
    if len(chunk_results) == 1:
        return chunk_results[0]['data']

    first = chunk_results[0]['data'] or {}
    last  = chunk_results[-1]['data'] or {}
    merged = {}

    for key in FIRST_CHUNK_KEYS:
        merged[key] = first.get(key, 'NOT FOUND')
    merged['cta'] = last.get('cta', 'NOT FOUND')

    for key in LIST_KEYS:
        combined = []
        for cr in chunk_results:
            val = (cr['data'] or {}).get(key, [])
            if isinstance(val, list):
                combined.extend(val)
            elif isinstance(val, str) and val not in ('NOT FOUND', 'NONE FOUND', ''):
                combined.append(val)
        merged[key] = combined or 'NOT FOUND'

    return merged

# ── Process one video ─────────────────────────────────────────────────────────
def process_video(video):
    chunks = chunk_text(video['transcript'])
    results = []
    for idx, chunk in enumerate(chunks):
        label = f" [chunk {idx+1}/{len(chunks)}]" if len(chunks) > 1 else ""
        print(f"    Calling Ollama{label} ({len(chunk):,} chars)...")
        prompt = EXTRACTION_PROMPT.format(
            title=video['title'] + label,
            date=video['date'],
            transcript_chunk=chunk,
        )
        raw  = call_ollama(prompt)
        data = parse_json(raw)
        results.append({'chunk': idx + 1, 'total_chunks': len(chunks), 'data': data})
    return results

# ── Save per-video result ─────────────────────────────────────────────────────
def save_video_result(video, chunk_results, merged):
    path = PROGRESS_DIR / f"video_{video['num']:03d}.json"
    payload = {
        "num":       video['num'],
        "title":     video['title'],
        "date":      video['date'],
        "word_count": video['word_count'],
        "char_count": len(video['transcript']),
        "chunks":    len(chunk_results),
        "extracted": merged,
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

# ── Progress tracking ─────────────────────────────────────────────────────────
def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"completed": [], "failed": []}

def save_progress(p):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(p, f, indent=2)

# ── Generate batch markdown files ─────────────────────────────────────────────
def generate_batch_files(videos):
    print("\n── Generating batch markdown files ──")
    all_results = []
    for v in videos:
        fp = PROGRESS_DIR / f"video_{v['num']:03d}.json"
        if fp.exists():
            with open(fp) as f:
                all_results.append(json.load(f))
        else:
            all_results.append({
                "num": v['num'], "title": v['title'], "date": v['date'],
                "word_count": v['word_count'], "chunks": 0, "extracted": None,
            })

    fields = [
        ('hook',              'Hook'),
        ('hook_type',         'Hook Type'),
        ('credential_drop',   'Credential Drop'),
        ('signature_phrases', 'Signature Phrases'),
        ('transitions',       'Transitions'),
        ('cta',               'CTA / Outro'),
        ('vocabulary',        'Vocabulary'),
        ('analogies',         'Analogies'),
        ('curiosity_gaps',    'Curiosity Gaps'),
        ('specificity',       'Specificity'),
        ('vulnerability',     'Vulnerability'),
        ('script_type',       'Script Type'),
        ('energy_notes',      'Energy Notes'),
        ('audience_language', 'Audience Language'),
        ('frameworks',        'Frameworks'),
    ]

    batch_num = 1
    for i in range(0, len(all_results), BATCH_SIZE):
        batch      = all_results[i:i + BATCH_SIZE]
        start_v    = batch[0]['num']
        end_v      = batch[-1]['num']
        batch_file = ANALYSIS_DIR / f"batch_{batch_num:02d}_videos_{start_v:03d}-{end_v:03d}.md"

        lines = [f"# Batch {batch_num:02d}: Videos {start_v}–{end_v}\n\n"]
        for r in batch:
            lines.append(f"## Video {r['num']}: {r['title']} ({r['date']})\n")
            lines.append(f"**Word count:** {r.get('word_count', '?')} | **Chunks:** {r.get('chunks', '?')}\n\n")
            extracted = r.get('extracted') or {}
            if not extracted:
                lines.append("_No extraction data._\n\n---\n\n")
                continue
            for key, label in fields:
                val = extracted.get(key, 'NOT FOUND')
                if isinstance(val, list):
                    lines.append(f"**{label}:**\n")
                    for item in val:
                        lines.append(f"- {item}\n")
                else:
                    lines.append(f"**{label}:** {val}\n")
                lines.append("\n")
            lines.append("---\n\n")

        with open(batch_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"  Written: {batch_file.name}")
        batch_num += 1

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    ANALYSIS_DIR.mkdir(exist_ok=True)
    PROGRESS_DIR.mkdir(exist_ok=True)

    print("Parsing transcript file...")
    videos = parse_videos(TRANSCRIPT_FILE)
    print(f"Found {len(videos)} videos.\n")

    if len(videos) == 0:
        print("ERROR: No videos found. Check transcript file path.")
        sys.exit(1)

    progress  = load_progress()
    completed = set(progress['completed'])
    failed    = set(progress['failed'])
    remaining = [v for v in videos if v['num'] not in completed]

    print(f"Completed: {len(completed)} | Failed: {len(failed)} | Remaining: {len(remaining)}\n")

    start_time = time.time()

    for idx, video in enumerate(remaining):
        num   = video['num']
        chars = len(video['transcript'])
        n_chunks = max(1, (chars + CHUNK_CHARS - 1) // CHUNK_CHARS)
        elapsed  = time.time() - start_time
        done_so_far = idx
        if done_so_far > 0:
            avg_per = elapsed / done_so_far
            eta_secs = avg_per * (len(remaining) - done_so_far)
            eta_str = f"  ETA: {eta_secs/3600:.1f}h"
        else:
            eta_str = ""

        print(f"[{idx+1}/{len(remaining)}] Video {num}: {video['title'][:55]}...")
        print(f"  {chars:,} chars | {n_chunks} chunk(s){eta_str}")

        try:
            chunk_results = process_video(video)
            merged        = merge_chunks(chunk_results)
            save_video_result(video, chunk_results, merged)
            completed.add(num)
            failed.discard(num)
            progress['completed'] = sorted(completed)
            progress['failed']    = sorted(failed)
            save_progress(progress)
            print(f"  ✓ video_{num:03d}.json saved")
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed.add(num)
            progress['failed'] = sorted(failed)
            save_progress(progress)

    total_time = time.time() - start_time
    print(f"\n── Extraction complete ({total_time/3600:.1f}h) ──")
    print(f"Completed: {len(completed)} | Failed: {len(failed)}")
    if failed:
        print(f"Failed video numbers: {sorted(failed)}")

    print("\nGenerating batch markdown files...")
    generate_batch_files(videos)
    print("\nAll done. Next: run the synthesis step in Claude Code.")

if __name__ == '__main__':
    main()
