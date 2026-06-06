# Higgsfield Capsule Prompt: Abstract Concept

**Sub-library:** `04_higgsfield_visuals`  
**Capsule:** `04c_abstract_concept`  
**Tool:** Higgsfield video generation API  
**Status:** draft

---

## Prompt Template

```
Atmospheric visual metaphor for: {concept}. 
Dark near-black environment. {atmosphere_description}. 
Slow, meditative motion — this is a feeling, not an action. 
Restrained colour: {color_tone}. No text, no logos, no readable UI, no dashboards. 
Final frame is still and holdable — the atmosphere is present but motion has settled.
Cinematic, considered. Not a tech demo — an emotion or idea made visible.
Aspect ratio: 16:9. Duration: {duration_s} seconds.
```

---

## Variables

- `{concept}` — the abstract idea to evoke (e.g. `"AI thinking"`, `"scale and reach"`, `"connection between systems"`, `"unseen intelligence"`)
- `{atmosphere_description}` — one sentence describing the specific visual atmosphere (e.g. `"slow-expanding luminous threads in deep space"`, `"soft geometric forms emerging from darkness"`, `"light refracting through an invisible structure"`)
- `{color_tone}` — single restrained tone (default: `"cool silver-white on near-black"`)
- `{duration_s}` — clip duration in seconds (default: `5`, range: `4–8`)

---

## Generation Settings (Higgsfield API)

- Aspect ratio: `16:9`
- Resolution: `1920 × 1080`
- Final-frame requirement: motion should be nearly still in the last 20% — holdable as a freeze frame
- Start-frame: darker, quieter — atmosphere builds through the clip

---

## Anti-list

- No action, explosions, or fast movement
- No text, logos, or product UI
- No generic sci-fi spacecraft, planets, or space backgrounds unless `{concept}` specifically calls for it
- No humanoid elements
- No saturated colour — keep the palette restrained and singular
- Do not generate anything that looks like a rendered product demo

---

## Notes On Reuse

This is the most flexible capsule in sub-library 04. `{atmosphere_description}` is the key differentiator per use — spend time on it. A precise atmospheric sentence produces a vastly better clip than a vague concept keyword.
