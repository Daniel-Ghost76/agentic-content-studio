# Higgsfield Capsule Prompt: Workflow Transformation

**Sub-library:** `04_higgsfield_visuals`  
**Capsule:** `04b_workflow_transformation`  
**Tool:** Higgsfield video generation API  
**Status:** draft

---

## Prompt Template

```
Abstract transformation visual — {transformation_concept}. 
Dark background, near-black. Motion travels {direction}: starts in a constrained, 
fragmented, or static state and resolves into an organised, flowing, or unified state 
by the final frame. Restrained colour: {color_tone}. Slow, deliberate motion. 
No text, no logos, no readable UI. Final frame is clean and resolved — 
the transformation is complete. Cinematic, premium.
Aspect ratio: 16:9. Duration: {duration_s} seconds.
```

---

## Variables

- `{transformation_concept}` — what is being transformed (e.g. `"scattered data becoming a coherent stream"`, `"manual work becoming automated flow"`, `"chaos becoming order"`)
- `{direction}` — motion direction (e.g. `"left to right"`, `"bottom to top"`, `"inward to outward"`)
- `{color_tone}` — single restrained tone (e.g. `"cool white-blue"`, `"warm gold"`, `"silver-grey"`)
- `{duration_s}` — clip duration in seconds (default: `6`, range: `4–8`)

---

## Generation Settings (Higgsfield API)

- Aspect ratio: `16:9`
- Resolution: `1920 × 1080`
- Final-frame requirement: the resolved/transformed state must be visible and held for at least the last 15% of the clip
- Start-frame: fragmented, scattered, or dim — contrast with the resolved final frame

---

## Anti-list

- No text, logos, or readable elements
- No explosive transitions — the transformation should feel gradual and inevitable
- No random looping — there must be a clear start state and end state
- No humanoid elements, faces, or hands
- Do not end the clip mid-transformation

---

## Notes On Reuse

Change `{transformation_concept}` and `{direction}` per video. The visual grammar (dark → resolving → clean final frame) stays constant and creates a recognisable language across episodes.
