# HyperFrames Capsule Prompt: Callout Card

**Sub-library:** `02_partial_overlays_hyperframes`  
**Capsule:** `02a_callout_card`  
**Aesthetic:** liquid glass / dark minimal  
**Status:** draft

---

## Visual Spec

- Canvas: `1920 × 1080px`, transparent background (composited over footage)
- Panel size: `320–420px wide`, height auto based on content (~80–100px)
- Panel style: glass recipe from `_channel_design_system.md`
- Font: Geist from `_channel_design_system.md`
- Position: bottom-left or bottom-right of frame (160px from edges, safe zone)
- Animation: entrance `300ms ease-out` slide from edge + opacity 0→1, exit `200ms ease-in` fade

## Variables

- `{label}` — small caps label above the value (e.g. "TOOL", "CONCEPT", "STAGE")
- `{value}` — main display text (e.g. "Claude Code", "Stage 4 — Editing") — max 6 words
- `{position}` — `bottom-left` or `bottom-right` (default: `bottom-right`)
- `{entrance_from}` — `left`, `right`, or `bottom` (default matches position side)
- `{hold_ms}` — how long panel stays visible in ms (default: `2500`)

## Anti-list

- No panel wider than 480px
- No value text longer than 6 words
- No blocking the centre of frame (face cam zone)
- No drop shadows heavier than `0 8px 32px rgba(0,0,0,0.40)`
- No border radius larger than 16px
- No colour backgrounds — glass only
- No icons or logos inside the panel

## Code Instruction

Write a HyperFrames HTML composition. The scene is a single overlay layer on a transparent 1920×1080 canvas. Create one glass panel positioned in the `{position}` corner, inset 160px from the frame edges.

The panel contains two text elements stacked vertically with 8px gap:
1. A label line: `13px`, `font-weight: 500`, `letter-spacing: 0.08em`, `text-transform: uppercase`, colour `#a1a1aa`
2. A value line: `36px`, `font-weight: 600`, colour `#ffffff`

Font: `Space Grotesk` (HyperFrames auto-resolves this — no import needed).

Panel padding: `16px 20px`. Apply the glass recipe from the design system (blur, fill, border, shadow). For footage overlays use the stronger variant: `rgba(255,255,255,0.10)` fill + `blur(12px)`.

On enter: use `gsap.from()` — panel starts `translateX(±40px)` (direction from `{entrance_from}`) and `opacity: 0`, animates to rest position over `300ms ease-out` (`power3.out`). After `{hold_ms}` ms, `gsap.to()` fades out over `200ms ease-in` (`power2.in`) with `overwrite: 'auto'`.

The composition should export as a transparent overlay clip.
