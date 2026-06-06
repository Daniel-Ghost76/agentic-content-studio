# HyperFrames Capsule Prompt: Install Command Bar

**Sub-library:** `02_partial_overlays_hyperframes`  
**Capsule:** `02d_install_command_bar`  
**Aesthetic:** teal glow / dark minimal  
**Status:** draft — seeded from eRS3CmvrOvA

---

## Visual Spec

- Canvas: `1920 × 1080px`, transparent background (composited over footage)
- Pill size: `~1100px wide`, `72px tall`, `border-radius: 36px`
- Position: horizontally centered, `60px` from bottom edge
- Background: `rgba(9, 9, 11, 0.88)`
- Border: `1.5px solid rgba(16, 185, 129, 0.75)`
- Box shadow: `0 0 24px rgba(16, 185, 129, 0.20), 0 0 8px rgba(16, 185, 129, 0.12)`
- Font: `JetBrains Mono` or `Space Mono`, `28px`, `font-weight: 500`, `color: #ffffff`, centered
- Animation in: `opacity 0→1` + `scale 0.96→1.0`, `250ms ease-out`
- Hold: `{hold_ms}` ms
- Animation out: `opacity 1→0`, `180ms ease-in`

## Variables

- `{command}` — the full terminal/slash command to display (e.g. `/plugin install skill-creator@claude-plugins-official`)
- `{hold_ms}` — display duration in ms (default: `3500`, range: `2500–6000`)

## Code Instruction

Write a HyperFrames HTML composition. Single overlay layer on a transparent 1920×1080 canvas.

Create one pill element:
```
width: 1100px
height: 72px
border-radius: 36px
background: rgba(9,9,11,0.88)
border: 1.5px solid rgba(16,185,129,0.75)
box-shadow: 0 0 28px rgba(16,185,129,0.18), 0 0 8px rgba(16,185,129,0.10)
position: absolute
bottom: 60px
left: 50%
transform: translateX(-50%)
display: flex
align-items: center
justify-content: center
```

Inside the pill, one `<code>` element:
```
font-family: 'JetBrains Mono', 'Space Mono', monospace
font-size: 28px
font-weight: 500
color: #ffffff
letter-spacing: 0.01em
```

On enter: `gsap.from(pill, { opacity: 0, scale: 0.96, duration: 0.25, ease: 'power2.out' })`.
After `{hold_ms}` ms: `gsap.to(pill, { opacity: 0, duration: 0.18, ease: 'power2.in' })`.

## Anti-list

- No icon elements inside the bar
- No label text above or below — command only
- No gradient fills — near-black solid only
- Do not wrap long commands — if text overflows reduce font size to 22px minimum
