# 04k — Linear Workflow Steps

**Sub-library:** `04_higgsfield_visuals`  
**Status:** draft — seeded from eRS3CmvrOvA (Nate Herk)

## What It Is

A Higgsfield clip showing a horizontal left-to-right sequence of 3–5 steps connected by lines, displayed inside a browser or app window frame with a section title above. Used to show the ordered stages of a workflow or process — each step is a teal icon square with a label below.

## When To Use

- Explaining a sequential process: "it does X, then Y, then Z"
- Showing the stages Claude executes internally (plan → test → brainstorm → review)
- Any ordered pipeline that needs to be made visible as a flow

## When Not To Use

- For non-sequential components (use `04j_architecture_diagram`)
- For more than 5 steps — too many for one visual
- For abstract concepts (use `04c_abstract_concept`)

## What Good Looks Like

- Section title: teal text above the window frame (`24–28px`, uppercase, spaced)
- Window frame: browser/app window chrome (dark, rounded corners, traffic light dots if applicable)
- Inside window: 3–5 step boxes in a horizontal row, connected by thin lines
  - Each step box: `~120×120px` rounded square, teal fill, icon inside (white, ~40px), label below in white
  - Active/current step: slightly brighter fill and a slightly larger size or glow
- Connections: thin horizontal lines between boxes
- Background behind window: near-black with ambient teal glow
- Animation: steps appear left to right with 300ms stagger, connections draw in between
- Duration: 4–6 seconds

## Reference

`eRS3CmvrOvA/screenshots/frame_0195000ms.jpg` — "SUPER POWER SKILL" title above browser window with TESTS → BRAINSTORMS → REVIEW three-step workflow. Third step ("REVIEW") is highlighted/active.
