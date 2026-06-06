# 02g — Expandable Checklist

**Sub-library:** `02_partial_overlays_hyperframes`  
**Status:** draft — seeded from eRS3CmvrOvA (Nate Herk)

## What It Is

A two-part overlay: a labeled category pill header anchored top-left, with a growing dark semi-transparent card beneath it that reveals checklist items one by one as Daniel speaks. Used when Daniel walks through "the things that exist" or "the options available" in a category.

## When To Use

- Daniel is listing 2–4 items that belong to one named category ("PLAIN TEXT FILES: Claude.md, Memory files")
- A checklist of existing tools/features that are being acknowledged before introducing something better
- Any "here's what already exists" moment where you want visual confirmation

## When Not To Use

- For a process that has order/sequence (use `02c_step_list` — numbered)
- For more than 4 items (too long for an overlay)
- For a single item — the checklist needs at least 2 items to justify the card

## What Good Looks Like

- **Header pill:** `~280–360px wide`, `52px tall`, `border-radius: 26px` — teal-filled, icon left, category label right
- **Card:** appears directly below header pill, `340–420px wide`, `border-radius: 12px`, `background: rgba(9,9,11,0.72)`, no border
- **Checklist items:** each `~40px tall`, flex row with `24px` teal checkmark `✓` on left, label text `20px` white on right
- Card height grows as items appear (animate height or use staggered reveal)
- Entire group: top-left, `80px` from edges
- Header fades in first. Card appears below it. Items stagger in 300ms apart.

## Reference

Observed at 10:09–10:22 in eRS3CmvrOvA — "PLAIN TEXT FILES" category pill + "Claude.md / Memory files" list building in, top-left position
