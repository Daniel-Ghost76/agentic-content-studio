# HyperFrames Capsule Prompt: Workflow Map

**Sub-library:** `03_full_screen_overlays`  
**Capsule:** `03b_workflow_map`  
**Aesthetic:** liquid glass / dark minimal  
**Status:** draft

---

## Visual Spec

- Canvas: `1920 × 1080px`, solid `#09090b` background
- Layout area: centred, max `1400px wide × 600px tall`
- Nodes: glass pill / rounded rect, `border-radius: 10px`
- Arrows: `1px` line, colour `rgba(255,255,255,0.25)`, animated draw-on
- Font: Geist from `_channel_design_system.md`
- Animation: title appears first, then nodes + arrows build in left-to-right (or top-to-bottom), one node at a time, 400ms per step

## Variables

- `{title}` — optional diagram title shown top-left or top-centre (e.g. `"The Agent Pipeline"`) — leave empty to omit
- `{direction}` — `horizontal` (left-to-right) or `vertical` (top-to-bottom) (default: `horizontal`)
- `{nodes}` — array of node objects: `[{label: "Input", sublabel: "optional"}, ...]` — 3–6 nodes max
- `{arrows}` — array of connection pairs: `[[0,1], [1,2], ...]` — index references to nodes array
- `{step_delay_ms}` — delay between each node appearing (default: `500`)
- `{hold_ms}` — hold after final node appears (default: `2000`)

## Anti-list

- No more than 6 nodes
- No node labels longer than 3 words
- No diagonal arrows — horizontal or vertical only
- No colour fills on nodes — glass only
- No decorative icons inside nodes
- No font sizes below 14px

## Code Instruction

Write a HyperFrames HTML composition. Full `1920 × 1080px` frame, `background: #09090b`.

If `{title}` provided, render it top-centre: `16px`, `font-weight: 600`, `letter-spacing: 0.08em`, `text-transform: uppercase`, colour `#a1a1aa`, fade in first over `250ms`.

Render nodes as glass pills in `{direction}` layout, evenly spaced across the content area. Each node: glass recipe + label text `18px font-weight: 600 #ffffff` + optional sublabel `13px #a1a1aa`. Nodes start `opacity: 0` and `translateX(-8px)` (horizontal) or `translateY(-8px)` (vertical), animating to rest over `300ms ease-out`.

Arrows are SVG lines between node centres. Each arrow path draws on using `stroke-dashoffset` animation over `250ms` timed to appear just before the destination node enters.

Nodes and arrows appear sequentially: node 0 fades in, then arrow 0→1 draws, then node 1 fades in, and so on. Gap between steps: `{step_delay_ms}`.

After all nodes visible + `{hold_ms}` ms, fade entire composition out over `300ms ease-in`.

Include Google Fonts Geist import.
