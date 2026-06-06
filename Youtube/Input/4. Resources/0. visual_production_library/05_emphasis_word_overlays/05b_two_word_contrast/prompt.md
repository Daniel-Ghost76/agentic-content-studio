# HyperFrames Capsule Prompt: Two-Word Contrast

**Sub-library:** `05_emphasis_word_overlays`  
**Capsule:** `05b_two_word_contrast`  
**Aesthetic:** liquid glass / dark minimal  
**Status:** draft

---

## Visual Spec

- Canvas: `1920 × 1080px`, transparent background
- Layout: two phrases with a separator between them, centred on frame
- Font: Geist, `font-weight: 700`, `64–80px`, `letter-spacing: -0.02em`
- Word A colour: `#52525b` (dim, secondary — the old/bad state)
- Separator: `→` or `/`, `#3f3f46`, `font-weight: 400`, `48px`
- Word B colour: `#ffffff` (bright — the new/good state) or accent once locked
- Animation: Word A fades in first, then separator, then Word B — staggered 300ms apart

## Variables

- `{word_a}` — first phrase (old/before state) — max 3 words, uppercase
- `{word_b}` — second phrase (new/after state) — max 3 words, uppercase
- `{separator}` — `arrow` (`→`) or `slash` (`/`) (default: `arrow`)
- `{layout}` — `horizontal` (side by side) or `vertical` (stacked) (default: `horizontal`)
- `{hold_ms}` — hold after Word B appears (default: `2000`)

## Anti-list

- No more than 3 words per phrase
- No background panel or glass — raw text only (same family as `05a_punch_word`)
- No simultaneous reveal — sequential order is mandatory
- No equal visual weight between Word A and Word B — A must read as secondary

## Code Instruction

Write a HyperFrames HTML composition. Transparent `1920 × 1080px` canvas.

If `{layout}` is `horizontal`: three inline elements on one row — `{word_a}`, separator, `{word_b}` — with `32px` gap between each. Entire group centred on frame with flexbox.

If `{layout}` is `vertical`: `{word_a}` and `{word_b}` stacked vertically with separator between, centred.

All three elements start `opacity: 0`. Timeline:
- `0ms`: Word A fades in over `250ms ease-out` (`opacity 0→0.45`)
- `300ms`: Separator fades in over `200ms ease-out` (`opacity 0→0.3`)
- `600ms`: Word B fades in over `300ms ease-out` + `scale(0.97)→scale(1)` (`opacity 0→1`)

After all visible + `{hold_ms}` ms, everything fades out over `200ms ease-in`.

Include Google Fonts Geist import.
