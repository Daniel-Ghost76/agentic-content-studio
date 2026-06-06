# HyperFrames Capsule Prompt: Step List

**Sub-library:** `02_partial_overlays_hyperframes`  
**Capsule:** `02c_step_list`  
**Aesthetic:** liquid glass / dark minimal  
**Status:** draft

---

## Visual Spec

- Canvas: `1920 × 1080px`, transparent background (composited over footage)
- Panel size: `380–480px wide`, height grows as steps build in
- Panel style: glass recipe from `_channel_design_system.md`
- Font: Geist from `_channel_design_system.md`
- Position: right side of frame, vertically centred or bottom-right (160px inset)
- Animation: panel appears first, then steps build in one at a time on cue (or auto-staggered at 80ms each)

## Variables

- `{title}` — optional small caps header above the list (e.g. "THE PROCESS", "3 STEPS") — leave empty to omit
- `{steps}` — array of step strings, 2–4 items max, each under 5 words (e.g. `["Connect your tools", "Write the prompt", "Review output"]`)
- `{position}` — `right-centre` or `bottom-right` (default: `right-centre`)
- `{stagger_ms}` — delay between each step appearing (default: `800` — driven by Daniel's speech pace; set to `80` for auto-cascade)
- `{hold_ms}` — hold after final step before exit (default: `2000`)

## Anti-list

- No more than 4 steps
- No step text longer than 5 words
- No paragraph sentences inside step items
- No icons — numbers only
- Do not show all steps at once — sequential reveal is mandatory
- No panel wider than 480px

## Code Instruction

Write a HyperFrames HTML composition. Single overlay layer, transparent 1920×1080 canvas. One glass panel at `{position}`, 160px from right and vertically centred (or bottom-right if specified).

Panel layout:
- Optional title: `12px`, `font-weight: 600`, `letter-spacing: 0.10em`, `text-transform: uppercase`, colour `#a1a1aa`, `margin-bottom: 12px`
- Step rows: each row is a flex container with a step number + step text
  - Step number: `13px`, `font-weight: 600`, colour from accent token (or `#a1a1aa` until accent is locked), `min-width: 20px`
  - Step text: `18px`, `font-weight: 500`, colour `#ffffff`
  - Row gap: `10px` between number and text, `14px` between rows

Panel padding: `20px 24px`. Apply glass recipe. Panel height must expand smoothly as each new step appears (use CSS transitions on height or animate max-height).

On enter: panel fades in + translateY(8px)→0 over `300ms ease-out`. Steps are all hidden initially. Each step fades in + translateX(8px)→0 over `250ms ease-out`, triggered either by `{stagger_ms}` interval or on a timed schedule.

After all steps are visible and `{hold_ms}` ms have passed, panel exits with `opacity: 0` over `200ms ease-in`.

Include Google Fonts Geist import. Export as transparent overlay clip.
