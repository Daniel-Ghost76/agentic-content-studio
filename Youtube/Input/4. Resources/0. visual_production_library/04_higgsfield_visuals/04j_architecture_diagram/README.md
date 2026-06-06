# 04j — Architecture Diagram

**Sub-library:** `04_higgsfield_visuals`  
**Status:** draft — seeded from eRS3CmvrOvA (Nate Herk)

## What It Is

A Higgsfield clip showing a horizontal node-link architecture diagram — icon circles or icon squares connected by dashed or solid lines, each labeled beneath. Used to explain how a system works: what connects to what, what goes where. The "how this thing actually works under the hood" visual.

## When To Use

- Explaining the technical structure of a tool or system ("a skill = a markdown file that connects to Claude's hooks, edits, offers, and design")
- Any "here's how it's wired together" moment
- Showing the relationship between 3–5 components in a pipeline

## When Not To Use

- When the relationship is a linear sequence (use `04k_linear_workflow_steps`)
- When there are more than 5 nodes — too complex for one diagram clip
- For abstract concepts with no component structure (use `04c_abstract_concept`)

## What Good Looks Like

- Background: near-black, teal gradient glow in one corner or across the base
- Outer frame: teal-glow rounded rectangle (matches `04e_section_intro_circle` frame style)
- Nodes: icon circles (teal fill or teal outline) with labels below, sized ~100–140px
- Connections: dashed lines between nodes, white or light teal
- Layout: horizontal left-to-right flow or hub-and-spoke (one central node, others radiating)
- Optional: a label pill at the top-center naming the diagram (`04f` header style)
- Animation: nodes appear sequentially, then connections draw in
- Duration: 4–6 seconds

## Reference

`eRS3CmvrOvA/screenshots/frame_0151000ms.jpg` — "SKILL" icon circle → dashed line → "Markdown" document → dashed line → "Claude" box (Hooks / Edits / Offers / Design grid inside). Teal glow frame.
