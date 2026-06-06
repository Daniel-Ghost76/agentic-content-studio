# Thumbnail Design Skill

## Before You Start

Read the reference library and pattern analysis first:

```
Youtube/Input/4. Resources/6. review_resources/reference_thumbnails/pattern_analysis.md
Youtube/Input/4. Resources/6. review_resources/thumbnail_style_guide.md
```

The pattern analysis is the source of truth. The sections below encode its conclusions.

---

## Step 1 — Read the Video

Pull the core topic, hook, and one concrete outcome from the transcript or script:

- What is the one thing the viewer will get?
- Is there a number, tool, or dollar amount that anchors it?
- What is the emotional payoff: curiosity, aspiration, vindication, FOMO?

---

## Step 2 — Choose a Layout Archetype

Match the video type to the right archetype. Use the decision table below.

| Video type | Primary archetype | Secondary option |
|------------|------------------|-----------------|
| Tutorial / tool walkthrough | FACE-RIGHT + MOCKUP-LEFT | SLASH COMMAND / CLEAN ICON CARD |
| Feature reveal / new drop | PILL/BAR CALLOUT + FACE | COMPETITIVE BATTLE |
| Comparison / tool vs tool | COMPARISON SPLIT | COMPETITIVE BATTLE |
| Opinion / take / personal update | LARGE DECLARATIVE TEXT | LIFESTYLE SHOT |
| History / framework explanation | MULTI-PANEL TIMELINE | WHITEBOARD DIAGRAM |
| News response / credibility | TWEET/PROOF SCREENSHOT | LARGE DECLARATIVE TEXT |
| Course / comprehensive guide | FACE-RIGHT + MOCKUP-LEFT | SLASH COMMAND / CLEAN ICON CARD |

### Archetype Quick Reference

**FACE-RIGHT + MOCKUP-LEFT** — Face occupies right 40–50%. UI screenshot, terminal, or app icon cluster on left. Pointing gesture or arrow toward element. Text at top or bottom.

**PILL/BAR CALLOUT + FACE** — 2–4 word lead text (white, heavy) + one key word in a colored pill/bar (teal, orange). Face right. Dark background.

**COMPARISON SPLIT** — Two visual halves with contrast labels (OLD/NEW, BEFORE/AFTER, Tool A vs Tool B). Face center optional. Red X on loser.

**SLASH COMMAND / CLEAN ICON CARD** — Mac window chrome (red/yellow/green dots) frames a `/command` or Claude logo + command. Warm beige or dark. Face right optional. Orange arrow at detail.

**LARGE DECLARATIVE TEXT** — 3–5 word sentence ending with a period. White or dark background. Minimal supporting image (benchmark, icon pair). No face required.

**COMPETITIVE BATTLE** — Claude icon (winner, glowing center) vs competitor icons (cracked, crying, red X). Dark background. Title text above. No face.

**WHITEBOARD DIAGRAM** — Creator beside whiteboard showing concept with red X, green circle, arrows. Face right, pointing.

**MULTI-PANEL TIMELINE** — 2–4 labeled panels (dates, levels, categories) each with a distinct visual. No face required.

**TWEET/PROOF SCREENSHOT** — Real tweet or benchmark with neon glow border. Face reacting right.

**LIFESTYLE SHOT** — Creator in outdoor or lifestyle setting. 2–4 word uppercase overlay. No props.

---

## Step 3 — Write the Hook Text

Pick the formula type that fits the emotional trigger:

**Curiosity gap**
- `It [Verb]s [Everything]` → "It Changes Everything"
- `[Tool] Just [Big Claim]`
- `[Number] [Outcome]` → "93M Tokens Saved"

**Contrast / comparison**
- `[OLD] vs [NEW]`
- `[X] is Dead.`
- `[Year] → [Year]`

**Authority / outcome**
- `$[Number] in [Time]`
- `[Bold Claim].` (period at end = finality)
- `Only [X]% [Reach This]`

**Directive**
- `[Verb] [This]` → "Copy This", "Use Both"
- `/[slash-command]` → `/skills`, `/free`, `/hacked`
- `Your [Noun]` → "Your Move"

**Urgency**
- `[X] Is Making You [Negative]`
- `[Opportunity] Nobody Is Talking About`

**Rules:**
- 2–5 words maximum for the primary hook
- Use heavy/black weight font only — no light or thin fonts
- One word or number may get a colored callout (pill, bar, or underline)
- Avoid sentences — prefer fragments and nouns over full clauses

---

## Step 4 — Compose the Thumbnail

### Color System

| Element | Color |
|---------|-------|
| Dark background | Black `#0A0A0A` or charcoal `#1A1A1A` |
| Light background | Warm cream `#F5EDE0` |
| Primary accent | Claude orange `#E07050`–`#E85000` |
| Callout pill | Teal `#00B8CC` OR orange — pick one per video |
| Contrast label | Blue `#3B82F6` for left side / orange for right |
| Urgency accent | Yellow `#FFD600` for max-FOMO moments only |
| Win/lose markers | Green `#16A34A` ✓ / Red `#DC2626` ✗ |
| Text on dark | White `#FFFFFF` |
| Text on light | Near-black `#0F0F0F` |

### Face Rules

- Right side is the default position
- Must occupy ≥ 35% of frame height — large enough to read expression at phone size
- Expression must match the emotional hook: smile (tutorial/good news), shock (urgency/news), serious (verdict/opinion)
- Pointing gesture toward the key visual element whenever possible
- No heavy outline or glow around face — let it breathe

### UI Element Priority (use the most specific available)

1. Claude Code terminal output (dark window, orange asterisk)
2. Mac window chrome (`⬤ ⬤ ⬤`) with Claude logo + `/command`
3. Phone held up showing app interface
4. Laptop with visible dashboard or revenue numbers
5. Whiteboard with diagram, X marks, and green circle
6. Tweet / X post with neon glow border
7. App icon pair (Claude + competitor)
8. 3-panel or 4-panel labeled comparison

### Arrow / Pointer Usage

- Orange curved arrow (Nick-style): point at a specific UI detail
- In-frame hand gesture (Nate/Liam style): preferred when face is present
- White arrow with label: comparison direction (A → B)

### Verdict Markers

- Red ✗ over the losing option (thick, bold)
- Green oval or circle around the winning option
- Strikethrough text on deprecated/wrong approaches

---

## Step 5 — Generate Three Concepts

For each concept:

1. **Archetype name**
2. **Hook text** (2–5 words)
3. **Background** (dark / warm cream / lifestyle)
4. **Face** (placement + expression, or "no face")
5. **Key visual element** (specific — terminal, /command, icon pair, etc.)
6. **Supporting elements** (arrows, pills, X marks, etc.)
7. **Score** — Curiosity / Clarity / Emotional punch / Phone readability (each 1–10)

Recommend the concept with the highest combined score. Minimum average: 7/10.

---

## Step 6 — Render

Run the local renderer with the recommended concept:

```bash
python3 "Youtube/Input/5. Tools/6. review_tools/thumbnail_renderer.py" \
  "{project_id}" \
  --face "/path/to/daniel-face.png"
```

Save outputs to: `Youtube/Output/6. Review  /{project_id}/`

- `{project_id}_thumbnail_concepts.md`
- `{project_id}_thumbnail.png`

Do not overwrite an existing thumbnail unless explicitly asked.

---

## Reference Library

```
Youtube/Input/4. Resources/6. review_resources/reference_thumbnails/
├── nateherk/       — 17 thumbnails + manifest.json
├── liamottley/     — 16 thumbnails + manifest.json
├── nicksaraev/     — 17 thumbnails + manifest.json
└── pattern_analysis.md
```

Use the reference library to verify your concept against proven examples before rendering. If an archetype is being used, cross-reference the channel folder for a similar example.

---

## Anti-Patterns (never use)

- Generic purple/blue AI glow with no specific claim
- More than 5 words in the primary hook text
- Light or thin font weights
- Face smaller than 35% of frame height when face is included
- Cluttered background that competes with text or UI element
- Abstract "AI" concept with no concrete anchor (number, tool, face, screenshot)
- Copying exact layouts from Nate Herk, Liam Ottley, or Nick Saraev — borrow principles, not executions
