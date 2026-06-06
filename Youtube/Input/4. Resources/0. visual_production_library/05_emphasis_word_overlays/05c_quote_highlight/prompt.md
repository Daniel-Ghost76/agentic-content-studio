# HyperFrames Capsule Prompt: Quote Highlight

**Sub-library:** `05_emphasis_word_overlays`  
**Capsule:** `05c_quote_highlight`  
**Aesthetic:** liquid glass / dark minimal  
**Status:** draft

---

## Visual Spec

- Canvas: `1920 × 1080px`, transparent background
- Text: 1–2 lines, `36–52px`, Geist `font-weight: 600`, `#ffffff`, centred
- Word-by-word reveal: each word fades in with `translateX(4px)→0` + `opacity 0→1` over `150ms`, staggered `80–120ms` per word
- Optional underline sweep: thin `2px` line appears under the full phrase after all words land, sweeping left→right over `400ms`
- Short hold after full reveal, clean fade out

## Variables

- `{quote}` — the phrase or thesis line (max 10 words, 1–2 lines)
- `{attribution}` — optional small attribution below (e.g. `"— Daniel"`) — leave empty to omit
- `{underline}` — `true` or `false` — whether the sweep underline appears after reveal (default: `false`)
- `{font_size}` — `large` (52px) or `normal` (38px) (default: `normal`)
- `{hold_ms}` — hold after full reveal (default: `2000`)

## Anti-list

- No more than 10 words
- No quote marks as decorative graphic elements
- No glass panel behind the text — raw type only
- No per-character animation (word-level only — per-character is too complex and looks busy)
- Do not use for subtitles — this is for designed thesis moments only

## Code Instruction

Write a HyperFrames HTML composition. Transparent `1920 × 1080px` canvas.

Split `{quote}` into individual word `<span>` elements. Centre the full phrase using flexbox wrapping on the canvas. Font: Geist `600`, size from `{font_size}` variable, `line-height: 1.3`, `#ffffff`.

All word spans start `opacity: 0` and `transform: translateX(4px)`. Each word animates to `opacity: 1, translateX(0)` over `150ms ease-out`, staggered `100ms` apart. Start the first word at `200ms` after scene opens.

If `{underline}` is `true`: after the last word lands (add a 200ms buffer), draw a `2px` `rgba(255,255,255,0.5)` underline using a pseudo-element or SVG line that sweeps from `width: 0` to `width: 100%` of the text over `400ms ease-out`.

If `{attribution}` provided: fade in below the quote, `14px`, `#a1a1aa`, `100ms` after the underline (or after last word if no underline).

After all elements visible + `{hold_ms}` ms, fade entire composition to `opacity: 0` over `200ms ease-in`.

Include Google Fonts Geist import.
