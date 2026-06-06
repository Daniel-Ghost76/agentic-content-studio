# HyperFrames Capsule Prompt: Next Video Tease

**Sub-library:** `06_cta_subscribe_visuals`  
**Capsule:** `06b_next_video_tease`  
**Aesthetic:** liquid glass / dark minimal  
**Status:** draft

---

## Visual Spec

- Canvas: `1920 × 1080px`, transparent (composited over footage)
- Card: glass panel, bottom-right corner, `160px` from edges, max `320px wide`
- Font: Geist from design system
- Animation: slides in from right edge (`translateX(40px) opacity(0)` → rest) over `350ms ease-out`, long hold, exits right

## Variables

- `{next_label}` — label above the title (default: `"WATCH NEXT"`) — small caps
- `{title}` — next video title — max 6 words, wraps to 2 lines if needed
- `{thumbnail_src}` — optional path/URL to thumbnail image — leave empty to show title-only card
- `{hold_ms}` — how long to display (default: `18000` — 18 seconds, covers end section)

## Anti-list

- No card wider than 340px
- No title longer than 6 words
- No autoplay arrow icons that look like fake player UI
- No bright red or YouTube-branded colours
- Do not cover the bottom-right end-screen click target zone in the final 20 seconds

## Code Instruction

Write a HyperFrames HTML composition. Transparent `1920 × 1080px` canvas.

Glass card at bottom-right, `160px` from right and bottom edges.

If `{thumbnail_src}` is provided: card layout top-to-bottom — thumbnail image at top (`100% wide`, `height: 90px`, `object-fit: cover`, `border-radius: 8px 8px 0 0`), then label + title below inside padded area.

If no thumbnail: label + title only, padded `16px 18px`.

Label: `11px`, `font-weight: 600`, `letter-spacing: 0.10em`, `text-transform: uppercase`, `#a1a1aa`.  
Arrow: `→` inline after label, same style.  
Title: `16px`, `font-weight: 600`, `#ffffff`, `line-height: 1.3`, `margin-top: 6px`.

Apply glass recipe. Entrance: `translateX(40px) opacity(0)` → rest over `350ms ease-out` starting at `200ms` after scene opens. After `{hold_ms}` ms, exit `translateX(40px) opacity(0)` over `300ms ease-in`.

Include Google Fonts Geist import.
