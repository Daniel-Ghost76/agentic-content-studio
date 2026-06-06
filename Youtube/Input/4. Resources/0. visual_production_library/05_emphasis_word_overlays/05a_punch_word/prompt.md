# HyperFrames Capsule Prompt: Punch Word

**Sub-library:** `05_emphasis_word_overlays`  
**Capsule:** `05a_punch_word`  
**Aesthetic:** liquid glass / dark minimal  
**Status:** draft

---

## Visual Spec

- Canvas: `1920 × 1080px`, transparent background (composited over footage or chapter break)
- Text position: horizontally centred, vertically centred or `45%` from top
- Font: Geist, `font-weight: 800`, `100–140px`, `letter-spacing: -0.03em`
- Colour: `#ffffff` default; accent override available
- Animation: slam entrance `120ms ease-out` from `scale(1.08) opacity(0)` to rest; hold; exit `150ms ease-in` fade

## Variables

- `{word}` — the single word to display (uppercase enforced in CSS)
- `{color}` — text colour (default: `#ffffff`; can be accent colour once locked)
- `{position_y}` — vertical position: `centre` or `high` (45% from top) (default: `centre`)
- `{hold_ms}` — how long the word holds after slamming in (default: `1500`)

## Anti-list

- One word only — no spaces
- No background panel, no glass, no border — raw text only
- No drop shadow heavier than `0 2px 20px rgba(0,0,0,0.6)`
- No animation longer than 150ms entrance (loses the punch)
- Do not use for multi-word phrases — that is `05b_two_word_contrast` or `05c_quote_highlight`

## Code Instruction

Write a HyperFrames HTML composition. Transparent `1920 × 1080px` canvas. Single text element: `{word}` in uppercase. Font: Geist `800` weight, `120px`, `letter-spacing: -0.03em`, `line-height: 1`, colour `{color}`.

Position: absolutely centred (or `top: 45%` if `{position_y}` is `high`), `transform: translateX(-50%)`.

Entrance: `scale(1.08) opacity(0)` → `scale(1) opacity(1)` over `120ms ease-out`. This must feel like a slam — fast in, immediate hold.

Optional: a very subtle text-shadow `0 0 40px rgba(255,255,255,0.15)` to give the word a faint presence against dark footage.

After `{hold_ms}` ms, fade to `opacity: 0` over `150ms ease-in`.

Include Google Fonts Geist import.
