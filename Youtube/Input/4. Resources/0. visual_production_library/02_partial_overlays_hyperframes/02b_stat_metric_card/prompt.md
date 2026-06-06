# HyperFrames Capsule Prompt: Stat / Metric Card

**Sub-library:** `02_partial_overlays_hyperframes`  
**Capsule:** `02b_stat_metric_card`  
**Aesthetic:** liquid glass / dark minimal  
**Status:** draft

---

## Visual Spec

- Canvas: `1920 × 1080px`, transparent background (composited over footage)
- Panel size: `300–440px wide`, height auto (~110–130px)
- Panel style: glass recipe from `_channel_design_system.md`
- Font: Geist from `_channel_design_system.md`
- Position: bottom-right, bottom-left, or top-right (160px from edges)
- Animation: number counts up from 0 over `600ms ease-out` after panel entrance; panel enters `300ms ease-out` translateY(12px) + opacity 0→1

## Variables

- `{number}` — the numeric value to display (e.g. `4`, `87`, `2.3`)
- `{unit}` — optional unit after the number (e.g. `hrs`, `%`, `×`, `k`) — leave empty if none
- `{prefix}` — optional prefix before the number (e.g. `$`, `~`, `+`) — leave empty if none
- `{label}` — context label below the number (e.g. "hours saved per week", "accuracy rate") — max 5 words
- `{position}` — `bottom-right`, `bottom-left`, or `top-right` (default: `bottom-right`)
- `{hold_ms}` — how long panel stays visible after count-up completes (default: `2000`)
- `{count_up}` — `true` or `false` — if false, number slams in with a brief scale(1.05)→scale(1) pulse instead

## Anti-list

- No more than one number per panel
- No label text longer than 5 words
- No decorative icons or progress bars
- No colour backgrounds — glass only
- Do not show the number before the panel entrance animation starts
- No decimal animation unless `{number}` itself contains a decimal

## Code Instruction

Write a HyperFrames HTML composition. Single overlay layer, transparent 1920×1080 canvas. One glass panel at `{position}`, 160px from frame edges.

Panel layout (vertical stack, 6px gap):
1. Number line: `{prefix}{number}{unit}` — `72px`, `font-weight: 700`, `letter-spacing: -0.02em`, colour `#ffffff`
2. Label line: `14px`, `font-weight: 500`, `letter-spacing: 0.06em`, `text-transform: uppercase`, colour `#a1a1aa`

Panel padding: `20px 24px`. Apply glass recipe from design system.

On enter: panel slides up from `translateY(12px)` + `opacity: 0` over `300ms ease-out`. If `{count_up}` is true, after panel is visible the number animates from `0` to `{number}` over `600ms ease-out` using `requestAnimationFrame`. If false, number appears with `scale(1.05)→scale(1)` pulse over `150ms`.

After count-up plus `{hold_ms}` ms hold, panel fades out over `200ms ease-in`.

Include Google Fonts Geist import. Export as transparent overlay clip.
