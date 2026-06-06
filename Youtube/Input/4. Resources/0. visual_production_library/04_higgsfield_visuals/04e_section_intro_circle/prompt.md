# Higgsfield Capsule Prompt: Section Intro Circle

**Sub-library:** `04_higgsfield_visuals`  
**Capsule:** `04e_section_intro_circle`  
**Tool:** Higgsfield video generation API  
**Status:** draft — seeded from eRS3CmvrOvA

---

## Prompt Template

```
Section chapter card. Near-black background (#09090b) with a very faint, soft teal 
radial glow behind the central element.

A rounded rectangle frame occupies most of the frame — approximately 1400×750px centred, 
thin teal-glowing border (1.5px, rgba(16,185,129,0.65)), no fill inside (transparent/dark).

In the exact centre of the frame: a large solid teal circle (~260px diameter, 
fill #10B981), containing the text "{section_name}" in white, bold, ~32px, centred.

Optional: a small icon or logo element below or above the text inside the circle — 
"{icon_description}" — if specified; otherwise text only.

The circle scales in gently from 0.85 to 1.0 over the clip duration. 
The rectangle border fades in from 0 to full opacity over the first half of the clip.

Background: dark, minimal, premium. No other elements.
Aspect ratio: 16:9. Duration: {duration_s} seconds.
```

---

## Variables

- `{section_name}` — the skill or topic name (e.g. `"SKILL CREATOR"`, `"SUPERPOWERS"`, `"GSD"`, `"Context Mode"`) — max 3 words
- `{icon_description}` — optional: short description of an icon to include inside or near the circle (e.g. `"small Anthropic asterisk logo"`, `"small gear icon"`) — or `"none"`
- `{duration_s}` — clip duration in seconds (default: `3`, range: `2.5–4`)

---

## DALL-E Reference Images

**First frame prompt:**
```
Dark minimalist chapter card on near-black background. Large solid teal circle 
centred inside a thin-bordered teal glowing rectangle frame. Circle contains white 
bold text "{section_name}". Circle starts slightly smaller than final size. 
Frame border is faint. Premium, clean, dark UI aesthetic.
```

**Last frame prompt:**
```
Same composition, fully settled. Circle at full size, teal border at full glow intensity. 
Text sharp and readable. No motion. Clean holdable frame.
```

---

## Generation Settings

- Aspect ratio: `16:9`
- Resolution: `1920 × 1080`
- Motion: circle scale-in, border glow fade-in — all slow and deliberate

---

## Anti-list

- No busy background — single radial glow only
- No text outside the circle
- No multiple circles or frames — one of each
- Do not loop — settle and hold
