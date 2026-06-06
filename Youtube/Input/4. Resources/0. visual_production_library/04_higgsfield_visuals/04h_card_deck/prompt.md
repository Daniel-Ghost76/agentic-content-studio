# Higgsfield Capsule Prompt: Card Deck

**Sub-library:** `04_higgsfield_visuals`  
**Capsule:** `04h_card_deck`  
**Tool:** Higgsfield video generation API  
**Status:** draft — seeded from eRS3CmvrOvA

---

## Prompt Template

```
Premium glass card stack in 3D perspective. Near-black background (#09090b) with a 
faint teal ambient glow at bottom-left.

Front card (fully visible, centred-left in frame): approximately 550×430px, dark glass 
with a thin teal glow border. Content:
- Top-left: a numbered circle "{item_number}" (52px, thin circle outline, white number inside)
- Centre: a circular icon zone (~160px diameter, solid teal circle), containing 
  "{icon_description}" — a clean icon or logo
- Below icon: left-aligned text "{body_lines}" — each line prefixed with a small teal 
  right-facing triangle "▶", white text, 18px

Behind the front card: 3 ghost cards, each shifted ~60px right and ~40px down from 
the card in front, scaled 0.92, 0.85, 0.78, with opacity 45%, 28%, 15%. 
Same card shape and border, no readable content inside the ghost cards.

Very subtle scale-in animation on the front card (0.97→1.0 over the clip duration).
Ghost cards fade in slightly as the clip progresses.

Aspect ratio: 16:9. Duration: {duration_s} seconds.
```

---

## Variables

- `{item_number}` — the card's position number (e.g. `"1"`, `"2"`, `"3"`)
- `{icon_description}` — description of the icon in the teal circle (e.g. `"orange-red pixel art robot (Claude Code icon)"`, `"gear icon"`, `"checkmark shield"`)
- `{body_lines}` — 1–3 lines of body text (e.g. `["Claude Code version 2.1.86 or later", "Signed in with a Claude account"]`)
- `{duration_s}` — clip duration in seconds (default: `5`, range: `4–7`)

---

## DALL-E Reference Images

**First frame prompt:**
```
Dark glass card with teal glow border, centred-left on near-black background. 
Numbered circle "1" top-left. Large teal circle icon in centre of card with 
"{icon_description}" inside. Two text lines below with teal arrow prefixes. 
Three ghost cards receding to the right in perspective. Premium, minimal.
```

**Last frame prompt:**
```
Same card deck, fully settled. Front card at full scale. Ghost cards at final 
opacity positions. Clean, holdable frame.
```

---

## Anti-list

- Ghost cards must have zero readable content — shape and border only
- Front card icon must be centred in the teal circle — no off-centre icons
- Body text lines must each start with ▶ prefix — no plain bullet points
- Maximum 3 lines of body text on front card
- Do not animate cards sliding in — they appear and subtly settle
