# Higgsfield Capsule Prompt: AI Tech HUD

**Sub-library:** `04_higgsfield_visuals`  
**Capsule:** `04a_ai_tech_hud`  
**Tool:** Higgsfield video generation API  
**Status:** draft

---

## Prompt Template

```
{concept_hint} — abstract technology visual. Dark near-black background (#09090b). 
Thin luminous data-flow lines moving slowly across the frame, subtle atmospheric 
depth haze, minimal particle drift. No text, no logos, no readable UI, no dashboards. 
Single restrained colour tone: {color_tone}. 
Cinematic, premium, slow motion. Final frame holds clean with motion mostly settled.
Aspect ratio: 16:9. Duration: {duration_s} seconds.
```

---

## Variables

- `{concept_hint}` — one short phrase describing the AI/tech idea (e.g. `"AI agent network"`, `"data pipeline"`, `"autonomous system"`) — guides the generative direction without being too literal
- `{color_tone}` — accent colour direction (e.g. `"cool blue-white"`, `"warm amber"`, `"neutral silver"`) — keep restrained, single-tone
- `{duration_s}` — clip duration in seconds (default: `5`, range: `3–8`)

---

## Generation Settings (Higgsfield API)

- Aspect ratio: `16:9`
- Resolution: `1920 × 1080`
- Final-frame requirement: motion should slow and settle in the last 20% of the clip so the editor can cut out cleanly
- Start-frame: no specific requirement — let Higgsfield establish from black

---

## Anti-list

- No text, numbers, or typographic elements generated in the clip
- No logos, brand marks, or recognisable product UI
- No neon colour explosions or glitch effects
- No busy dashboards with many tiny elements
- No animated faces, hands, or humanoid elements
- No looping that looks mechanical — motion should feel organic

---

## Notes On Reuse

This capsule produces b-roll. Change `{concept_hint}` for each video — the base visual style (dark, data-flow, restrained tone) stays consistent across episodes.
