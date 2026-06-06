# HyperFrames Capsule Prompt: Version Badge

**Sub-library:** `02_partial_overlays_hyperframes`  
**Capsule:** `02e_version_badge`  
**Aesthetic:** teal glow / dark minimal  
**Status:** draft — seeded from eRS3CmvrOvA

---

## Visual Spec

- Canvas: `1920 × 1080px`, transparent background
- Group position: bottom-center, group bottom edge `120px` from frame bottom, horizontally centered
- **Top label:** `{label_text}` — `font-size: 72px`, `font-weight: 700`, `color: #ffffff`, no background, no panel, centered
- **Gap:** `16px` between label bottom and pill top
- **Bottom pill:** `width: {pill_width}px` (default 640), `height: 64px`, `border-radius: 32px`
  - Background: `rgba(9, 9, 11, 0.88)`
  - Border: `1.5px solid rgba(16, 185, 129, 0.78)`
  - Box shadow: `0 0 24px rgba(16,185,129,0.18)`
  - Text: `{command_text}`, monospace 26px, white, centered

## Variables

- `{label_text}` — large version/product label (e.g. `"Opus 4.7"`, `"Claude 3.5"`, `"v2.1.86"`) — max 3 words
- `{command_text}` — the command inside the pill (e.g. `"/ultrareview"`, `"/gsd-help"`)
- `{pill_width}` — pill width in px (default: `640`, adjust to fit command text)
- `{hold_ms}` — total hold duration in ms (default: `3000`)

## Code Instruction

Write a HyperFrames HTML composition. Single overlay layer on a transparent 1920×1080 canvas.

Create a flex column group (`display: flex; flex-direction: column; align-items: center; gap: 16px`) positioned `bottom: 120px; left: 50%; transform: translateX(-50%); position: absolute`.

Inside the group:
1. Label element: `font-family: 'Space Grotesk'; font-size: 72px; font-weight: 700; color: #fff; text-shadow: 0 0 40px rgba(255,255,255,0.15)`
2. Pill element: same spec as `02d_install_command_bar` but narrower — width fits `{command_text}`

Animate: `gsap.from([label, pill], { opacity: 0, scale: 0.95, duration: 0.22, stagger: 0.08, ease: 'power2.out' })`.
After `{hold_ms}` ms: `gsap.to([label, pill], { opacity: 0, duration: 0.18, ease: 'power2.in' })`.

## Anti-list

- No background panel behind the top label — it must float freely over footage
- No icon on the pill for this capsule (command only)
- Label text must not exceed 3 words / ~12 characters
