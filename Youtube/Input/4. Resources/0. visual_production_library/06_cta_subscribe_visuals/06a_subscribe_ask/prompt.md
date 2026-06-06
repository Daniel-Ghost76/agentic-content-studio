# HyperFrames Capsule Prompt: Subscribe Ask

**Sub-library:** `06_cta_subscribe_visuals`  
**Capsule:** `06a_subscribe_ask`  
**Aesthetic:** liquid glass / dark minimal  
**Status:** draft

---

## Visual Spec

- Canvas: `1920 × 1080px`, transparent (composited over footage)
- Panel: small glass pill, bottom-centre or bottom-right, `160px` from edges
- Size: max `360px wide`, height auto (~60–72px)
- Font: Geist from design system
- Animation: slides up from `+16px` + `opacity 0→1` over `300ms ease-out`, auto-exits after hold

## Variables

- `{channel_name}` — Daniel's channel name (e.g. `"@danieldanut"`)
- `{cta_text}` — the ask text (default: `"Subscribe for more"`) — max 4 words
- `{position}` — `bottom-centre` or `bottom-right` (default: `bottom-centre`)
- `{hold_ms}` — how long to display (default: `3500`)

## Anti-list

- No YouTube red button or logo — native YouTube handles that in the player
- No text longer than 4 words in `{cta_text}`
- No animations that call too much attention — this is a quiet ask
- No full-width banners
- No bell icon unless it looks completely native (test it)

## Code Instruction

Write a HyperFrames HTML composition. Transparent `1920 × 1080px` canvas.

Single glass pill at `{position}`, `160px` from the bottom edge. Pill layout (horizontal flex, gap `10px`, `align-items: centre`):
1. Optional small circle icon (12px diameter, `rgba(255,255,255,0.4)` fill) as a minimal visual indicator
2. `{channel_name}`: `15px`, `font-weight: 600`, `#ffffff`
3. Thin vertical divider: `1px solid rgba(255,255,255,0.15)`, `height: 14px`
4. `{cta_text}`: `14px`, `font-weight: 400`, `#a1a1aa`

Pill padding: `12px 18px`, `border-radius: 100px`. Apply glass recipe from design system (reduced blur `blur(12px)` since this sits on footage).

Entrance: `translateY(16px) opacity(0)` → rest over `300ms ease-out`. After `{hold_ms}` ms, `opacity(1) → opacity(0)` over `250ms ease-in`.

Include Google Fonts Geist import.
