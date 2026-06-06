# Higgsfield Capsule Prompt: Architecture Diagram

**Sub-library:** `04_higgsfield_visuals`  
**Capsule:** `04j_architecture_diagram`  
**Tool:** Higgsfield video generation API  
**Status:** draft — seeded from eRS3CmvrOvA

---

## Prompt Template

```
Technical architecture diagram on near-black background (#09090b). 
A soft teal gradient glow runs along the bottom edge of the frame.

A thin teal-glow rounded rectangle frame (matches the outer frame style from a 
section intro) contains the diagram.

Optional: a label pill at the top-center of the frame reading "{diagram_title}" 
(teal-filled pill, white text, if {diagram_title} is specified).

Inside the frame, a horizontal node-link diagram:
{node_descriptions}

Nodes are connected by dashed lines ({connection_style}) running horizontally between them.
Each node has a label below it.

If the final node contains sub-components (a 2×2 grid of items), render it as a 
rounded rectangle box with a title and the items listed in a 2-column grid inside.

Animation: nodes appear from left to right with a 300ms stagger, then dashed-line 
connections draw in sequentially. Everything settles by 60% of clip duration, 
remaining time holds static.

Aspect ratio: 16:9. Duration: {duration_s} seconds.
```

---

## Variables

- `{diagram_title}` — optional top label (e.g. `"SKILL"`) or `"none"`
- `{node_descriptions}` — comma-separated node descriptions in order, each: `"[icon_type] labeled '[label]'"`. E.g.: `"teal circle with gear+brain icon labeled 'SKILL'", "blue document icon labeled 'Markdown'", "rounded rectangle box labeled 'Claude' containing 2×2 grid: Hooks, Edits, Offers, Design"`
- `{connection_style}` — `"dashed white"` or `"solid teal"` (default: `"dashed white"`)
- `{duration_s}` — clip duration in seconds (default: `5`, range: `4–7`)

---

## DALL-E Reference Images

**First frame prompt:**
```
Dark technical diagram on near-black background inside a teal glow rounded frame. 
First node (teal circle with icon labeled "SKILL") visible on the left. 
Remaining nodes not yet drawn. Teal ambient glow at bottom. Premium, dark UI aesthetic.
```

**Last frame prompt:**
```
Complete architecture diagram. All nodes and connections visible. 
Left to right: SKILL circle → dashed line → Markdown document → dashed line → 
Claude box with Hooks/Edits/Offers/Design grid inside. Clean, readable, settled.
```

---

## Anti-list

- No more than 5 nodes — diagram gets unreadable beyond that
- No coloured connector lines other than white or teal
- No arrows (dashed lines only, no arrowheads) unless the flow is strictly one-directional
- All labels must be short (1–2 words max)
- No busy backgrounds — teal glow at base only
