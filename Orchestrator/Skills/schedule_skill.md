# Schedule Skill

**Owner:** All orchestrators (Astra, Vera, Clodella, Codex)
**Tool:** `mcp__claude_ai_Google_Calendar` (claude.ai MCP)
**Calendar:** `daniel@ministryflow.co` (primary)
**Timezone:** `Europe/London`

---

## Weekly Schedule — Canonical Structure

### Every Day
| Block | Time | Recurring Event ID |
|-------|------|--------------------|
| Brush Teeth + Drink Water | 03:45–04:00 | `3l8ddrae2i7k0pglle22p9h2be` |

### Mon–Sat
| Block | Time | Recurring Event ID |
|-------|------|--------------------|
| Dinner | 18:00–18:45 | `sp8j9sml3hmthk1o2mbdi88rl8` |
| Downtime — Read / Devotional | 18:45–19:45 | `cac40sefm195rkh59cnq2jnl4c` |
| Sleep | 19:45–03:45 | `1de0ugn4fh9754gvnavbdv7v3p` |

### Monday–Friday
| Block | Time | Recurring Event ID |
|-------|------|--------------------|
| Scripting 📝 | 04:00–09:00 | `0e87rja3qk97mig4vpmr7b0hrt` |
| Breakfast | 09:00–09:30 | `1ppgnkce5k7huojrn6i6106kq5` |
| Gym | 10:00–12:00 | `4oje6orbh8vjn5mmr8328sl5p4` |
| Recording | 12:00–14:00 | `4mg133s5n5r2tvueshcea0stq4` |
| Lunch | 14:00–14:30 | `nkiglnpg8cbcmf6oirb5d1hefg` |
| Editing | 14:30–16:30 | `ki5v9rrcb62mgmgovv8vf4d5mo` |
| Build / Agentic Workflows | 16:30–18:00 | `63i93a8d7gqubfs1p90ldo990g` |

### Saturday
| Block | Time | Recurring Event ID |
|-------|------|--------------------|
| Breakfast | 09:00–09:30 | `1ppgnkce5k7huojrn6i6106kq5` |
| Gym | 10:00–12:00 | `p2nqrimaodp1i1kvkm8nrj58mo` |
| Laundry / Clean | 12:00–12:30 | `4b0cjom2v9d5366epcse8ln4ig` |
| Outreach | 12:30–14:30 | `5h553g8i1l20cco5np8eabt9ig` |
| Lunch | 14:30–15:00 | `a1ibpr0vi3hg31qe65bp8u4qgc` |

### Sunday
| Block | Time | Recurring Event ID |
|-------|------|--------------------|
| Call with Irma | 13:00–14:00 | `2kqjffqrj5833u4h0msheu6ohm` |
| Call with Ana | 14:00–15:00 | `e727mfqmfa9g8kglrrl8km2s4g` |
| Church | 16:00–21:00 | `5cn8ht7os6srh1oh4ajn1hk23c` |
| Dinner | 21:00–21:30 | `rlpt3ss926e4qmh4b3qc6b7sss` |
| Sleep | 21:30–03:45 | `8a3uh7r1u3isejv5at9hmicqls` |

### Weekly / Biweekly Meetings
| Meeting | When | Recurring Event ID |
|---------|------|--------------------|
| Call with Francis (biweekly) | Thu 16:00–17:00 | `ne0ppgbip7tbnqbekhh73nsdf0` |

---

## Rules

**Do not book over:**
- 04:00–09:00 (Deep Work) — highest-priority protected block
- Sleep — 19:45–03:45 Mon–Sat; 21:30–03:45 Sunday
- Church (Sun 16:00–21:00)
- Any existing recurring meeting (Irma, Ana, Francis)

**Safe windows for one-off calls/tasks:**
- Mon–Fri: 09:30–10:00 (post-breakfast, pre-gym)
- Sat: 13:30–18:00 (post-Outreach/Lunch, pre-Dinner)
- Sun: 14:00–16:00 (post-Ana, pre-Church) — but Ana ends at 15:00 so 15:00–16:00 is the clean window

**Phase context:**
- Phase 1 (until ~2026-07-08): Recording block = foundation AI explainer videos daily
- Phase 2 (~2026-07-08+): Recording block = buyer-facing content + pro-bono build documentation
- Saturday Outreach block activates fully in Phase 2 (warm outreach, pro-bono sourcing)

---

## How to Use This Skill

### Read current schedule
```
mcp__claude_ai_Google_Calendar__list_events(
    startTime='YYYY-MM-DDT00:00:00',
    endTime='YYYY-MM-DDT23:59:59',
    timeZone='Europe/London'
)
```

### Add a one-off event
```
mcp__claude_ai_Google_Calendar__create_event(
    summary='Event name',
    startTime='YYYY-MM-DDTHH:MM:00',
    endTime='YYYY-MM-DDTHH:MM:00',
    timeZone='Europe/London'
)
```

### Update a recurring block (e.g. shift recording time)
Use the recurring event ID from the table above. Do NOT update a single instance ID — update the base series ID so all future occurrences shift.
```
mcp__claude_ai_Google_Calendar__update_event(
    eventId='[recurring_event_id]',
    startTime='YYYY-MM-DDTHH:MM:00',
    endTime='YYYY-MM-DDTHH:MM:00',
    timeZone='Europe/London'
)
```

### Delete a recurring series
```
mcp__claude_ai_Google_Calendar__delete_event(
    eventId='[recurring_event_id]',
    notificationLevel='NONE'
)
```

### Add a new indefinite weekly recurring event
```
mcp__claude_ai_Google_Calendar__create_event(
    summary='Block name',
    startTime='YYYY-MM-DDTHH:MM:00',  # use next occurrence date
    endTime='YYYY-MM-DDTHH:MM:00',
    timeZone='Europe/London',
    recurrenceData=['RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR']  # adjust BYDAY
)
```

---

## Last Rebuilt
2026-06-08 — Sunday stripped to bare minimum (Irma/Ana calls, Church 16:00–21:00, Dinner, Sleep). Weekday Publish+Distribute+Plan and Buffer/Admin removed; replaced with Build / Agentic Workflows 16:30–18:00. Downtime now Mon–Sat only.
