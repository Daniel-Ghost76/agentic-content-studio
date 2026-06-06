# HyperFrames Capsule Prompt: Chapter Break

**Sub-library:** `03_full_screen_overlays`  
**Capsule:** `03a_chapter_break`  
**Aesthetic:** liquid glass / dark minimal  
**Status:** draft

---

## Visual Spec

- Canvas: `1920 × 1080px`, solid `#09090b` background
- Central glass card: max `720px wide`, height auto
- Font: Geist from `_channel_design_system.md`
- Position: centred horizontally and vertically
- Animation: background fades from 0 opacity over `200ms`, card scales from `0.96` + `opacity 0` to rest over `350ms ease-out`, exit fade all `300ms ease-in`

## Variables

- `{chapter_number}` — optional chapter label (e.g. `"CHAPTER 1"`, `"STEP 2"`, `"PART THREE"`) — leave empty to omit
- `{title}` — main chapter title (e.g. `"Building the System"`) — max 5 words
- `{description}` — optional one-line subtitle (e.g. `"How the agent pipeline is structured"`) — max 8 words, leave empty to omit
- `{hold_ms}` — duration of full-visibility hold before exit (default: `2500`)

## Anti-list

- No more than 5 words in the title
- No busy background — pure `#09090b` only
- No icons or decorative graphics
- No text smaller than 18px
- No card wider than 720px
- No animation longer than 400ms entrance

## Code Instruction

Write a HyperFrames HTML composition. Full `1920 × 1080px` frame, `background: #09090b`.

Single centred glass card. Layout (vertical stack, gap 8px):
1. If `{chapter_number}` provided: `13px`, `font-weight: 600`, `letter-spacing: 0.12em`, `text-transform: uppercase`, colour `#a1a1aa`
2. Title: `52px`, `font-weight: 700`, `letter-spacing: -0.02em`, colour `#ffffff`, `line-height: 1.1`
3. If `{description}` provided: `18px`, `font-weight: 400`, colour `#71717a`, `margin-top: 4px`

Card padding: `32px 48px`. Apply glass recipe from design system. Centre card using flexbox on the full frame.

Entrance: background fades in from `opacity: 0` over `200ms`. Card simultaneously animates from `scale(0.96) opacity(0)` to `scale(1) opacity(1)` over `350ms ease-out`. After `{hold_ms}` ms, entire composition exits: `opacity: 1 → 0` over `300ms ease-in`.

**Flash fix (mandatory):** Before building the timeline, call `gsap.set()` on every animated element to lock its initial state from frame 0. This prevents the GSAP `from()` flash where elements are briefly visible at their natural CSS state before GSAP initialises:

```js
gsap.set('#bg-blur', { opacity: 0 });
gsap.set('#card',    { opacity: 0, scale: 0.96 });
gsap.set(['#chapter-number', '#chapter-title', '#chapter-description'], { opacity: 0 });
```

**Background:** Use `background-color: #09090b` + separate `background-image` (not the `background` shorthand) so the dark fallback is always present before the image loads — no white flash on first frame.

Font: `Space Grotesk` (HyperFrames auto-resolves — no import needed).
