# HyperFrames Capsule Prompt: Expandable Checklist

**Sub-library:** `02_partial_overlays_hyperframes`  
**Capsule:** `02g_expandable_checklist`  
**Aesthetic:** teal header pill + dark expanding card  
**Status:** draft — seeded from eRS3CmvrOvA

---

## Visual Spec

- Canvas: `1920 × 1080px`, transparent background
- Position: `top: 60px; left: 60px`

**Header pill:**
- Width: auto (fits `{category}` text), `min-width: 240px`, height: `52px`, `border-radius: 26px`
- Background: `rgba(16, 185, 129, 0.90)` (solid teal)
- Left icon: `32px`, white, icon name from `{category_icon}`
- Label: `font-size: 18px; font-weight: 700; color: #ffffff; letter-spacing: 0.06em; text-transform: uppercase`
- Internal padding: `0 20px 0 14px`, icon-label gap `10px`

**Expanding card:**
- Appears `8px` below the header pill
- Width: `380px` (or matches pill width + 40px)
- Background: `rgba(9, 9, 11, 0.75)`
- Border-radius: `0 0 14px 14px` (flat top to sit flush under pill, rounded bottom)
- Padding: `12px 16px`
- Height: starts at 0, expands as items appear

**Checklist items** (one per `{items}` entry):
- Row: `height: 40px; display: flex; align-items: center; gap: 14px`
- Checkmark: `24px × 24px` circle, `background: rgba(16,185,129,0.15)`, `border: 1.5px solid rgba(16,185,129,0.5)`, inner `✓` in teal `16px`
- Text: `font-size: 20px; font-weight: 500; color: #ffffff`

## Variables

- `{category}` — category label in header pill (e.g. `"Plain Text Files"`, `"Quality Gates"`, `"Requirements"`)
- `{category_icon}` — icon name (e.g. `"file-text"`, `"shield"`, `"list"`, `"check-square"`)
- `{items}` — array of 2–4 strings, each a checklist label (e.g. `["Claude.md", "Memory files"]`)
- `{item_delay_ms}` — ms between each item appearing (default: `400`)
- `{hold_ms}` — hold after last item appears before exit (default: `2500`)

## Code Instruction

Write a HyperFrames HTML composition. Single overlay layer on 1920×1080 transparent canvas.

Render the header pill first. Animate: `gsap.from(pill, { opacity:0, x:-20, duration: 0.25, ease:'power2.out' })`.

Below the pill, render the card container. Set `overflow: hidden; height: 0` initially. For each item in `{items}`:
1. Pre-render the item row but `opacity: 0; transform: translateX(-12px)`
2. After `(index * {item_delay_ms})` ms from card appear: `gsap.to(card, { height: targetHeight, duration: 0.3, ease:'power2.out' })` then `gsap.to(item, { opacity:1, x:0, duration:0.22, ease:'power2.out' })`

After all items shown and `{hold_ms}` ms: fade entire group out `opacity 0, duration 0.25`.

## Anti-list

- No border on the card itself — background only
- Do not show all items simultaneously — must stagger reveal
- No numbered labels — checkmarks only in this capsule (use `02c_step_list` for numbered steps)
- Maximum 4 items
