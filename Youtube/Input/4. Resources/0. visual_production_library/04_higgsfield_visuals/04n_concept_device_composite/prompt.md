# Higgsfield Capsule Prompt: Concept Device Composite

**Sub-library:** `04_higgsfield_visuals`  
**Capsule:** `04n_concept_device_composite`  
**Tool:** Higgsfield video generation API  
**Status:** draft — seeded from eRS3CmvrOvA

---

## Prompt Template

```
Bold concept statement with product device. Near-black background (#09090b).

Top half of frame: large bold uppercase white text "{headline_word_1} {headline_word_2}" 
(~88px, font-weight 800, letter-spacing 0.05em). 
The second word "{headline_word_2}" may appear slightly bolder or have a very subtle 
teal tint to differentiate it.

Bottom half of frame: an iPad or tablet in landscape orientation, 
screen showing {screen_content_description} — a dark-mode interface with 
visible code, files, or documentation layout. The device is centred horizontally.

Very faint ambient glow beneath the tablet (teal or neutral).
Minimal to no motion — this is a near-static title card.

Aspect ratio: 16:9. Duration: {duration_s} seconds.
```

---

## Variables

- `{headline_word_1}` — first word of the bold headline (e.g. `"AUTOMATE"`)
- `{headline_word_2}` — second word (e.g. `"BUSINESS"`, `"FASTER"`, `"SMARTER"`)
- `{screen_content_description}` — what the tablet screen shows (e.g. `"VS Code file explorer with skill folders and a SKILLSPEC.txt file open"`)
- `{duration_s}` — clip duration in seconds (default: `5`, range: `4–6`)

---

## DALL-E Reference Images

**First frame prompt:**
```
Large bold uppercase white text "{headline_word_1} {headline_word_2}" at the top 
of a near-black frame. Below it, an iPad landscape with a dark-mode code editor 
showing folders and a text file. No border, no glow frame. Very minimal, high-impact. 
Premium product visual.
```

**Last frame prompt:**
```
Same composition, fully settled. Text crisp. iPad screen content visible and readable 
at screen level. Clean holdable frame.
```

---

## Hybrid Approach Note

The headline text can be composited in HyperFrames for exact font control:
1. Higgsfield: generate the near-black background + iPad frame with blank/dark screen
2. HyperFrames: composite the bold headline text + composite real screenshot into iPad screen via perspective transform

---

## Anti-list

- Headline must not exceed 2 words — simplicity is the impact
- Device must be landscape iPad, not portrait phone
- No teal glow frame/border around the composition
- No icons or additional decorative elements — text + device only
