# Higgsfield Capsule Prompt: Chapter Menu

**Sub-library:** `04_higgsfield_visuals`  
**Capsule:** `04f_chapter_menu`  
**Tool:** Higgsfield video generation API  
**Status:** draft — seeded from eRS3CmvrOvA

---

## Prompt Template

```
Dark macOS-style application window on near-black background. The window has a 
dark title bar with three traffic-light dots (red, yellow, green) on the left 
and navigation/toolbar icons on the right.

Inside the window: a numbered menu of {item_count} skills/topics arranged in a 
{layout} grid. Each item is a rounded rectangle row containing a large bold number 
on the left and a skill name on the right.

Active item (number {active_index}): bright solid teal fill (#0D9488), white text, 
full opacity, slightly glowing — "{active_label}".
All other items: dark fill (rgba(30,30,35,0.8)), text dimmed to ~30% opacity, 
names partially blurred or unreadable — {inactive_labels}.

Below the window frame: a macOS-style dock with 4–5 blurred app icons is faintly 
visible at the bottom edge of the frame.

Background behind the window: near-black with a subtle ambient light gradient at 
the bottom center.

Static composition with minimal ambient light movement.
Aspect ratio: 16:9. Duration: {duration_s} seconds.
```

---

## Variables

- `{item_count}` — total number of items in the menu (e.g. `6`)
- `{layout}` — `"2-column"` or `"single-column"` (use 2-column for 5+ items)
- `{active_index}` — 1-based index of the highlighted item (e.g. `2`)
- `{active_label}` — the visible highlighted skill name (e.g. `"SUPER POWERS"`)
- `{inactive_labels}` — comma-separated list of the other labels (intentionally dimmed/blurred, Higgsfield may render them unreadably) — e.g. `"SKILL CREATOR, GSD, REVIEW, CONTEXT MODE, CLAUDE MEM"`
- `{duration_s}` — clip duration in seconds (default: `4`, range: `3–6`)

---

## DALL-E Reference Images

**First frame prompt:**
```
Dark macOS app window with a numbered list menu inside. Two-column grid of 
rounded rectangle items. One item ({active_label}) has a bright teal fill and 
white bold text. The others are dark and dimmed. Traffic light buttons top-left. 
Near-black background. Premium, clean.
```

**Last frame prompt:**
```
Same composition. Fully settled, no motion. Active item clearly highlighted.
```

---

## Anti-list

- Inactive items must remain unreadable — they serve as visual texture, not readable content
- No animations inside the window (no scrolling, no hover states)
- Do not show more than 1 active (highlighted) item
- No bright or colourful dock icons — keep dock icons very desaturated / blurred
