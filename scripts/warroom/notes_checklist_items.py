#!/usr/bin/env python3
"""Emit plain-text lines for the morning Notes checklist (typed via UI scripting).

Output format (sections separated for the AppleScript):
  line 1: date · focus header
  then PRIORITIES section marker, items
  then SCHEDULE section marker, items
No emoji — keystroke typing chokes on them.
"""
import datetime
import json
import sys

d = json.load(open(sys.argv[1]))
date = datetime.date.fromisoformat(d['date'])

print(f"{date.strftime('%A %-d %B')} - Focus: {d.get('focus', '')}")
print('::PRIORITIES::')
for p in d['priorities']:
    print(p['text'])
print('::SCHEDULE::')

tasks = {p['id']: p['text'] for p in d['priorities']}

def endtime(t):
    h, m = map(int, t.split(':'))
    m += 30
    return f"{h + m // 60:02d}:{m % 60:02d}"

runs = []
for sl in d['slots']:
    tid = sl.get('taskId')
    if not tid:
        continue
    if runs and runs[-1]['tid'] == tid and runs[-1]['end'] == sl['time']:
        runs[-1]['end'] = endtime(sl['time'])
    else:
        runs.append({'tid': tid, 'start': sl['time'], 'end': endtime(sl['time'])})
for r in runs:
    label = tasks.get(r['tid'], r['tid'])
    short = label if len(label) <= 52 else label[:49] + '...'
    print(f"{r['start']}-{r['end']} {short}")
