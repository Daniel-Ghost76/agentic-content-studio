# HyperFrames Capsule Prompt: Icon Pill

**Sub-library:** `02_partial_overlays_hyperframes`  
**Capsule:** `02f_icon_pill`  
**Aesthetic:** teal-fill pill / benefit callout  
**Status:** draft — seeded from eRS3CmvrOvA

---

## Visual Spec

- Canvas: `1920 × 1080px`, transparent background
- Pill: `{pill_width}px wide` (default 300), `60px tall`, `border-radius: 30px`
- Background: `rgba(16, 185, 129, 0.12)`
- Border: `1.5px solid rgba(16, 185, 129, 0.70)`
- Box shadow: `0 0 16px rgba(16,185,129,0.14)`
- Internal layout: `display: flex; align-items: center; padding: 0 16px 0 12px; gap: 12px`
- **Icon zone:** `44px × 44px` circle, `background: rgba(16,185,129,0.18)`, centered icon `24px`
- **Label:** `font-family: 'Space Grotesk'; font-size: 20px; font-weight: 600; color: #ffffff; letter-spacing: 0.03em; text-transform: uppercase`

## Position Variants

- `bottom-left` — single pill: `left: 80px; bottom: 80px`
- `bottom-center-pair` — two pills side by side: group centered, `bottom: 80px`, `gap: 20px`
- `bottom-left-stacked` — two pills stacked: `left: 80px; bottom: 80px`, column with `12px` gap
- `top-left` — single pill: `left: 80px; top: 80px`

## Variables

- `{pills}` — array of pill objects, each with:
  - `{label}` — display text (e.g. `"SAVE TIME"`, `"Fewer debugging cycles"`) — max 4 words
  - `{icon}` — icon name from HyperFrames icon set (e.g. `"clock"`, `"check-circle"`, `"dollar-sign"`, `"target"`, `"shield"`, `"zap"`)
  - `{pill_width}` — width in px (default: `300`, adjust to label length)
- `{position_variant}` — one of: `bottom-left`, `bottom-center-pair`, `bottom-left-stacked`, `top-left`
- `{hold_ms}` — display duration in ms (default: `3000`)

## Code Instruction

Write a HyperFrames HTML composition. Single overlay layer on 1920×1080 transparent canvas.

For each pill in `{pills}`, create a flex-row container matching the visual spec above. If `{position_variant}` is a pair/stacked, wrap all pills in a parent flex container (row or column) and center-position the group.

Animate on enter: `gsap.from(pills, { opacity: 0, y: 20, duration: 0.28, stagger: 0.08, ease: 'power3.out' })`.
After `{hold_ms}` ms: `gsap.to(pills, { opacity: 0, y: -8, duration: 0.20, stagger: 0.05, ease: 'power2.in' })`.

## Anti-list

- No glass blur — teal-tinted solid fill only
- No heavy drop shadows — glow only
- Label must not exceed 4 words
- Icons must be simple line icons — no filled complex illustrations
- Do not mix this style with the glass panel style of `02a_callout_card` in the same video section
