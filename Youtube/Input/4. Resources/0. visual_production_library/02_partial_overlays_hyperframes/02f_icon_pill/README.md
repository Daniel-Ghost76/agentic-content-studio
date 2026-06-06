# 02f — Icon Pill

**Sub-library:** `02_partial_overlays_hyperframes`  
**Status:** draft — seeded from eRS3CmvrOvA (Nate Herk)

## What It Is

A compact teal-filled rounded pill with a circular icon on the left and a short benefit label on the right. Used to surface a single outcome or feature point directly on face cam footage. Can appear solo or in a pair (two pills side by side or stacked).

## When To Use

- Daniel names a concrete benefit: "saves time", "removes mistakes", "fewer debugging cycles"
- A feature or outcome needs a visual anchor during a spoken list
- Appearing in pairs: two simultaneous benefits shown bottom-center

## When Not To Use

- For a terminal command (use `02d_install_command_bar`)
- For a numbered process (use `02c_step_list`)
- For a metric with a number hero (use `02b_stat_metric_card`)
- When text exceeds 4 words — shrink wording or switch capsule

## What Good Looks Like

- Pill: `~260–320px wide`, `60px tall`, `border-radius: 30px`
- Background: `rgba(16, 185, 129, 0.15)` + `border: 1.5px solid rgba(16,185,129,0.70)`
- Left: circular icon zone `44px` dia, teal icon (clock, checkmark, money, target, etc.)
- Right: label text `20–22px`, `font-weight: 600`, `color: #ffffff`, `letter-spacing: 0.02em`, uppercase or title case
- Position: `bottom-left` (single pill), or `bottom-center` pair side-by-side with 20px gap
- Variant B (top-left): single pill anchored top-left, 80px from edges
- Entrance: `translateY(20px)` → rest + `opacity 0→1`, `280ms ease-out`
- Multiple pills stagger 80ms apart

## Reference

Observed at 0:12 ("SAVE TIME" + "SAVE MONEY" bottom-center pair), 4:15 ("Fewer debugging cycles" top-left), 5:23 ("Quality gates" + "Scope reduction detection" stacked bottom-left) in eRS3CmvrOvA
