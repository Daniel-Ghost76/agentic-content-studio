# Higgsfield Capsule Prompt: Icon Node Flow

**Sub-library:** `04_higgsfield_visuals`  
**Capsule:** `04l_icon_node_flow`  
**Tool:** Higgsfield video generation API  
**Status:** draft — seeded from eRS3CmvrOvA

---

## Prompt Template

```
Abstract process flow diagram. Near-black background (#09090b) with deep teal 
gradient ambient glow at the bottom-left and bottom-right corners.

{node_count} large circles arranged horizontally across the frame, equally spaced. 
Each circle:
- Diameter: ~200px
- Style: teal glowing ring outline (not filled), glow intensity rgba(16,185,129,0.7)
- Inside the ring: a clean icon, ~80px, teal color: "{node_icons}" (one per circle, in order)
- Below the circle (outside): white label, ~22px, "{node_labels}" (one per circle)

Between each pair of adjacent circles: a simple thin arrow (→), white, pointing 
left to right. Arrow centered vertically between the two circles.

The circles gently pulse with the teal glow (subtle breathing animation ~0.95–1.0 scale, 
1.5s period). Arrows fade in after the circles appear.

No window frame. No titles. Pure diagram on dark background.
Aspect ratio: 16:9. Duration: {duration_s} seconds.
```

---

## Variables

- `{node_count}` — number of circles (e.g. `3`)
- `{node_icons}` — comma-separated icon descriptions in order (e.g. `"analytics bar chart with person icon"`, `"circular clock/timeline icon"`, `"document with magnifying glass"`)
- `{node_labels}` — comma-separated labels below each circle (e.g. `"Returns a compact index"`, `"Pull a timeline"`, `"Fetch full details"`)
- `{duration_s}` — clip duration in seconds (default: `5`, range: `4–7`)

---

## DALL-E Reference Images

**First frame prompt:**
```
Dark background with deep teal ambient glow at corners. Three large teal-glow 
ring circles spaced horizontally. First circle contains an analytics/chart icon 
with label "Returns a compact index". Other circles faint/appearing. 
Minimal, abstract, premium dark tech aesthetic.
```

**Last frame prompt:**
```
All three circles fully visible with teal glow rings. White arrows connecting 
them left to right. Labels below each. Circles gently glowing. Clean holdable frame.
```

---

## Anti-list

- Circles must be ring outlines (not solid fills) — the icon must be visible inside
- No window frames or browser chrome in this capsule
- No more than 4 nodes — 3 is the sweet spot
- Arrow should be thin and simple — not a large flashy directional indicator
- Label text must be 1–4 words maximum per node
