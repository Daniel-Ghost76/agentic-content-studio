#!/usr/bin/env python3
"""Render a War Room day JSON as HTML for the Apple Notes mirror."""
import json
import sys

d = json.load(open(sys.argv[1]))

def mark(b):
    return '✅' if b else ('⬜' if b is None else '❌')

s = d.get('score') or {}
parts = ["<h1>⚔️ War Room — Today</h1>"]
parts.append(f"<p><b>{d['date']}</b></p>")
parts.append(f"<p><b>Focus:</b> {d.get('focus', '')}</p>")
parts.append(f"<p>Rating {s.get('rating') or 0}% · {s.get('hours') or 0}h</p>")
parts.append('<h2>Priorities</h2><ul>')
for p in d['priorities']:
    actual = f" ({p['actual']})" if p.get('actual') is not None else ''
    parts.append(f"<li>{mark(p['done'])} {p['text']}{actual}</li>")
parts.append('</ul><h2>Schedule</h2><ul>')
tasks = {p['id']: p['text'] for p in d['priorities']}
for sl in d['slots']:
    if sl.get('taskId'):
        parts.append(f"<li>{sl['time']} {mark(sl.get('done'))} {tasks.get(sl['taskId'], '')}</li>")
    elif sl.get('routine'):
        parts.append(f"<li>{sl['time']} · {sl['routine']}</li>")
parts.append('</ul><p><i>Read-only mirror — tick in the War Room app.</i></p>')
print(''.join(parts))
