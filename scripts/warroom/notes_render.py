#!/usr/bin/env python3
"""Render a War Room day JSON as clean HTML for the Quick Note mirror."""
import datetime
import json
import sys

d = json.load(open(sys.argv[1]))

def box(b):
    return '☑' if b else '☐'

date = datetime.date.fromisoformat(d['date'])
s = d.get('score') or {}
parts = ["<h1>⚔️ War Room — Today</h1>"]
parts.append(f"<p>{date.strftime('%A %-d %B')} · {s.get('rating') or 0}% · {s.get('hours') or 0}h focused</p>")
parts.append(f"<p><b>Focus:</b> {d.get('focus', '')}</p>")
parts.append('<p>—————————</p>')

parts.append('<p><b>PRIORITIES</b></p>')
for p in d['priorities']:
    actual = f" ({p['actual']})" if p.get('actual') is not None else ''
    parts.append(f"<p>{box(p['done'])} {p['text']}{actual}</p>")

parts.append('<p>—————————</p>')
parts.append('<p><b>SCHEDULE</b></p>')
tasks = {p['id']: p['text'] for p in d['priorities']}

def endtime(t):
    h, m = map(int, t.split(':'))
    m += 30
    return f"{h + m // 60:02d}:{m % 60:02d}"

# group consecutive slots with the same taskId into one range line
runs = []
for sl in d['slots']:
    tid = sl.get('taskId')
    if not tid:
        continue
    if runs and runs[-1]['tid'] == tid and runs[-1]['end'] == sl['time']:
        runs[-1]['end'] = endtime(sl['time'])
        runs[-1]['all_done'] &= bool(sl.get('done'))
    else:
        runs.append({'tid': tid, 'start': sl['time'], 'end': endtime(sl['time']),
                     'all_done': bool(sl.get('done'))})
for r in runs:
    label = tasks.get(r['tid'], r['tid'])
    short = label if len(label) <= 58 else label[:55] + '…'
    parts.append(f"<p>{box(r['all_done'])} {r['start']}–{r['end']}  {short}</p>")

print(''.join(parts))
