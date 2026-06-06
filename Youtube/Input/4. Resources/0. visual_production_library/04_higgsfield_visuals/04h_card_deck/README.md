# 04h — Card Deck

**Sub-library:** `04_higgsfield_visuals`  
**Status:** draft — seeded from eRS3CmvrOvA (Nate Herk)

## What It Is

A Higgsfield clip of stacked glass cards in 3D perspective — the front card is fully readable and contains a numbered item, icon, and body text. Behind it, 3–4 ghost cards recede in a perspective stack suggesting more items follow. Used to list requirements, prerequisites, or features with a premium, premium visual weight.

## When To Use

- Listing prerequisites or requirements (e.g. "here's what you need before running this")
- Presenting 3–5 items that have equal visual weight and deserve individual focus
- Any "before you run this, check these" or "here's what to have ready" moment

## When Not To Use

- For a process with sequence/order (use `04k_linear_workflow_steps`)
- For abstract concepts (use `04c_abstract_concept`)
- When items are longer than 1–2 short lines — cards get too dense

## What Good Looks Like

- Front card: `~500–600px wide`, `~420px tall`, rounded corners (~28px), semi-transparent dark glass with teal accent at top edge
  - Numbered circle top-left: `52px` diameter, circle outline, number inside
  - Icon circle centre: `~160px` diameter, teal circle background, icon inside (Anthropic robot, Claude logo, etc.)
  - Body text below icon: left-aligned, `18–20px`, white, with a teal play-arrow `▶` prefix for each line
- Ghost cards: 3–4 cards behind the front card, each shifted right and slightly scaled down, opacity decreasing (50% → 30% → 15%), same shape and border
- Background: near-black, faint teal ambient glow at bottom-left corner
- Animation: front card has a very subtle scale-in (0.97→1.0), ghost cards drift into position
- Duration: 4–6 seconds per card, or used as a static hold

## Reference

`eRS3CmvrOvA/screenshots/frame_0440000ms.jpg` — Card 1: Anthropic pixel robot icon, "Claude code version 2.1.86 or later". 3 ghost cards receding right.
