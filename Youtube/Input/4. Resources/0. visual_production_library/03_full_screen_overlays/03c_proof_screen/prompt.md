# HyperFrames Capsule Prompt: Proof Screen

**Sub-library:** `03_full_screen_overlays`  
**Capsule:** `03c_proof_screen`  
**Aesthetic:** liquid glass / dark minimal  
**Status:** draft

---

## Visual Spec

- Canvas: `1920 × 1080px`, solid `#09090b` background
- Screenshot frame: max `1200px wide`, centred, glass border, `border-radius: 12px`
- Label panel: small glass pill below the screenshot frame, centred
- Font: Geist from `_channel_design_system.md`
- Animation: background fades in, frame scales from `0.97` + opacity 0 → rest over `350ms ease-out`, label slides up from `+8px` after frame settles

## Variables

- `{screenshot_src}` — path or URL to the screenshot image
- `{label}` — short descriptor for what the screenshot shows (e.g. `"Claude Code output"`, `"Scheduled agent run"`) — max 6 words
- `{sublabel}` — optional secondary label (e.g. `"05 Jan 2026"`, `"Production environment"`) — leave empty to omit
- `{frame_style}` — `normal` (full screenshot centred) or `cropped` (screenshot fills frame with slight overflow crop)
- `{hold_ms}` — hold after entrance completes (default: `3000`)

## Anti-list

- No editorial colour grading on the screenshot — show it as-is
- No fake data overlaid onto the screenshot content
- No decorative graphics around the frame
- No label text longer than 6 words
- Do not obscure any critical part of the screenshot with the label panel
- No animations inside the screenshot content itself

## Code Instruction

Write a HyperFrames HTML composition. Full `1920 × 1080px` frame, `background: #09090b`.

Layout: vertically centred flex column. Screenshot image inside a glass-bordered container — `border: 1px solid rgba(255,255,255,0.10)`, `border-radius: 12px`, `overflow: hidden`. If `{frame_style}` is `normal`, image scales to fit max `1200px wide` with natural aspect ratio. If `cropped`, image covers the container with `object-fit: cover`.

Below the screenshot frame (gap `16px`): a glass pill label — padding `8px 16px`, `border-radius: 100px`. Inside: `{label}` at `14px font-weight: 500 #ffffff`. If `{sublabel}` provided, add a `·` separator and sublabel at `14px colour: #a1a1aa`.

Entrance: background fades `opacity 0→1` over `200ms`. Screenshot container: `scale(0.97) opacity(0) → scale(1) opacity(1)` over `350ms ease-out`. Label pill: `translateY(8px) opacity(0) → rest` over `250ms ease-out` starting `150ms` after container enters.

After `{hold_ms}` ms, fade everything out over `300ms ease-in`.

Include Google Fonts Geist import.
