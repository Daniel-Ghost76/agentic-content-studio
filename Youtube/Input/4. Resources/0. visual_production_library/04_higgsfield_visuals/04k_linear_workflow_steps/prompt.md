# Higgsfield Capsule Prompt: Linear Workflow Steps

**Sub-library:** `04_higgsfield_visuals`  
**Capsule:** `04k_linear_workflow_steps`  
**Tool:** Higgsfield video generation API  
**Status:** draft — seeded from eRS3CmvrOvA

---

## Prompt Template

```
Workflow process diagram inside a browser/app window. Near-black background (#09090b) 
with a soft teal ambient glow behind the window.

Title above the window (outside the frame): "{workflow_title}" in teal uppercase 
text, ~26px, letter-spaced.

The window frame: dark browser chrome, rounded corners, macOS-style (optional 
traffic light dots top-left).

Inside the window: {step_count} process step boxes arranged in a horizontal row, 
connected by thin lines. Each box:
- Rounded square, ~120×120px, teal fill (#0D9488 or close)
- White icon inside (~40px): "{step_icons}" (one per box)
- Label below the box (outside the box, white, ~16px): "{step_labels}"
- The active/highlighted step (index {active_step}) is slightly brighter 
  and larger (~130×130px) with a faint glow

Thin connecting lines between boxes. No arrows.

Animation: boxes appear left to right, 300ms stagger. 
Connecting lines draw in left to right between each box.
Final: all elements settled.

Aspect ratio: 16:9. Duration: {duration_s} seconds.
```

---

## Variables

- `{workflow_title}` — title above the window (e.g. `"SUPER POWER SKILL"`, `"GSD PROCESS"`)
- `{step_count}` — number of steps (e.g. `3`, `4`, `5`)
- `{step_icons}` — comma-separated icon descriptions for each step box in order (e.g. `"checklist icon", "brain/lightning icon", "speech-bubble review icon"`)
- `{step_labels}` — comma-separated step labels in order (e.g. `"TESTS", "BRAINSTORMS", "REVIEW"`)
- `{active_step}` — 1-based index of the active/highlighted step (e.g. `3` for last), or `0` for none
- `{duration_s}` — clip duration in seconds (default: `5`, range: `4–7`)

---

## DALL-E Reference Images

**First frame prompt:**
```
Dark browser window on near-black background. "{workflow_title}" teal title above. 
First step box (teal square with icon) visible on the left. Others not drawn yet. 
Soft teal ambient glow. Premium, minimal, dark UI.
```

**Last frame prompt:**
```
Complete workflow diagram. {step_count} step boxes connected by horizontal lines. 
"{step_labels}" labels below each box. Active step ({active_step}) slightly brighter. 
Clean, settled, readable.
```

---

## Anti-list

- No arrows on connectors — thin lines only
- No more than 5 steps in one diagram
- Step labels must be single words or short 2-word phrases
- The active step is only slightly larger — do not exaggerate the size difference
- Do not use different colours for different steps — teal fill for all
