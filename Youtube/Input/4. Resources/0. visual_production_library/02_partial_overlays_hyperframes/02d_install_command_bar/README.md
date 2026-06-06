# 02d — Install Command Bar

**Sub-library:** `02_partial_overlays_hyperframes`  
**Status:** draft — seeded from eRS3CmvrOvA (Nate Herk)

## What It Is

A near-full-width pill anchored at the very bottom of the face cam frame displaying a terminal install command in monospace white text. Appears exactly when Daniel says "run this command" or "install it with" — the spoken command lands visually on screen.

## When To Use

- Daniel mentions a terminal command, plugin install, or slash command the viewer should copy
- Any "here's the exact command" moment — install, run, configure
- Works under face cam or over screen recordings when command is short enough

## When Not To Use

- For a concept label or benefit (use `02f_icon_pill`)
- For a list of steps (use `02c_step_list`)
- For a metric or number (use `02b_stat_metric_card`)
- When the command is longer than ~60 characters — break into two lines or use a screen recording

## What Good Looks Like

- Pill shape, ~1100px wide, ~72px tall, horizontally centered, 60px from bottom edge
- White monospace text, ~28–32px, centered in the pill
- Teal glow outline: `1.5px solid rgba(16, 185, 129, 0.8)`, box-shadow teal ambient glow
- Background: `rgba(9, 9, 11, 0.85)` — near-black, slightly transparent
- Entrance: fade in + scale from 0.96→1.0 over 250ms
- Hold: stays on screen for full duration of spoken command (~3–5s)
- Exit: fade out 180ms after command is complete

## Reference

Observed at 2:07, 9:00, 11:39 in eRS3CmvrOvA — "plugin install", "/context-mode:ctx-stats", "/plugin marketplace add"
