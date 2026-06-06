# HyperFrames Capsule Prompt: Comment Prompt

**Sub-library:** `06_cta_subscribe_visuals`  
**Capsule:** `06c_comment_prompt`  
**Aesthetic:** liquid glass / dark minimal  
**Status:** draft

---

## Visual Spec

- Canvas: `1920 × 1080px`, transparent (composited over footage)
- Card: glass panel, centred horizontally, bottom third of frame (`top: 70%`)
- Size: max `640px wide`, height auto
- Font: Geist from design system
- Animation: slide up from `+16px` + `opacity 0→1` over `350ms ease-out`

## Variables

- `{question}` — Daniel's question to the audience — max 10 words, 1–2 lines
- `{cta_label}` — sub-label below (default: `"Comment below ↓"`)
- `{hold_ms}` — how long to display (default: `4000`)

## Anti-list

- No decorative speech bubble graphics
- No question mark as a giant decorative element
- No text longer than 10 words in `{question}`
- `{cta_label}` max 4 words
- No full-width panel

## Code Instruction

Write a HyperFrames HTML composition. Transparent `1920 × 1080px` canvas.

Glass card centred horizontally, positioned at `top: 70%` of the canvas. Card layout (vertical stack, gap `8px`):
1. `{question}`: `32px`, `font-weight: 600`, `#ffffff`, `line-height: 1.35`, `text-align: centre`, max `600px wide`
2. `{cta_label}`: `13px`, `font-weight: 500`, `letter-spacing: 0.08em`, `text-transform: uppercase`, `#a1a1aa`, `text-align: centre`

Card padding: `24px 32px`. Apply glass recipe from design system.

Entrance: `translateY(16px) opacity(0)` → rest over `350ms ease-out`. After `{hold_ms}` ms, `opacity(1) → opacity(0)` over `250ms ease-in`.

Include Google Fonts Geist import.
