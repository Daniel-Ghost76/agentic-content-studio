# 02e — Version Badge

**Sub-library:** `02_partial_overlays_hyperframes`  
**Status:** draft — seeded from eRS3CmvrOvA (Nate Herk)

## What It Is

A two-layer annotation overlay: a large product or version label in bold white text (no background panel) floating above a smaller teal-outline command pill. Used when a version number or product name needs to land visually alongside the command that uses it.

## When To Use

- Daniel mentions a specific version requirement + the command to invoke it ("Opus 4.7… /ultrareview")
- A product launch name + slash command pair needs to appear simultaneously
- Any "version X just dropped and here's how to use it" moment

## When Not To Use

- When there is no paired command — use `02f_icon_pill` for standalone labels
- When the top text is longer than 3 words — too heavy for a floating label
- When the command is the only relevant thing — use `02d_install_command_bar` alone

## What Good Looks Like

- Top element: plain bold white text, 64–80px, no background, no panel — floats freely
- Bottom element: ~600–700px wide pill, teal glow outline, command text in monospace 26px
- Gap between top text and pill: ~16px
- Entire group: bottom-center, ~120px from bottom edge
- Top text entrance: fade in 0→1, 200ms, slight scale 0.95→1.0
- Pill entrance: same timing, stagger 80ms after top text
- Hold both together, exit together

## Reference

Observed at 6:39 in eRS3CmvrOvA — "Opus 4.7" floating above "/ultrareview" pill
