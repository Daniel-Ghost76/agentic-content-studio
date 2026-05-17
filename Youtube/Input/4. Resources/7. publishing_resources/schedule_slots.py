#!/usr/bin/env python3
"""
Calculate YouTube schedule slots at 4:00 PM Europe/London.

Slot assignment:
  Videos 1–3  →  next 3 Fridays
  Videos 4+   →  consecutive Tuesdays after the last Friday

Usage:
    python3 schedule_slots.py <num_videos>

Output:
    One ISO 8601 datetime per line, e.g.:
    2026-05-15T16:00:00+01:00
    2026-05-22T16:00:00+01:00
    2026-05-29T16:00:00+01:00
    2026-06-02T16:00:00+01:00
"""

import sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo


def get_slots(n: int) -> list[str]:
    tz = ZoneInfo("Europe/London")
    today = date.today()

    # Next 3 Fridays — never include today even if today is Friday
    fridays: list[date] = []
    d = today + timedelta(days=1)
    while len(fridays) < 3:
        if d.weekday() == 4:  # Friday
            fridays.append(d)
        d += timedelta(days=1)

    # Tuesdays strictly after the last Friday, for videos 4+
    tuesdays: list[date] = []
    need = max(n - 3, 0)
    d = fridays[-1] + timedelta(days=1)
    while len(tuesdays) < need:
        if d.weekday() == 1:  # Tuesday
            tuesdays.append(d)
        d += timedelta(days=1)

    slots = fridays[:min(n, 3)] + tuesdays[:need]
    return [
        datetime(s.year, s.month, s.day, 16, 0, 0, tzinfo=tz).isoformat()
        for s in slots[:n]
    ]


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    for slot in get_slots(n):
        print(slot)
