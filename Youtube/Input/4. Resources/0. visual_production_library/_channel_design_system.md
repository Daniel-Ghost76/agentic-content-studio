# Channel Design System

This file is the single source of truth for all visual tokens used across sub-libraries 02–06. Every HyperFrames capsule prompt references these values instead of respecifying them. When Daniel approves a change here, it propagates to every future capsule build.

**Status: accent locked 2026-06-06 — seeded from eRS3CmvrOvA (Nate Herk) analysis. Other tokens confirmed draft.**

---

## Colour Tokens

| Token | Value | Use |
|-------|-------|-----|
| `--bg` | `#09090b` | Full-frame background when no footage underneath |
| `--glass-fill` | `rgba(255,255,255,0.07)` | Glass panel background |
| `--glass-border` | `rgba(255,255,255,0.10)` | Glass panel border |
| `--glass-highlight` | `rgba(255,255,255,0.04)` | Inner top/left highlight on glass panels |
| `--text-primary` | `#ffffff` | Main headings and values |
| `--text-secondary` | `#a1a1aa` | Labels, captions, supporting copy |
| `--text-tertiary` | `#52525b` | Dividers, placeholder text |
| `--accent` | `#10B981` | Primary teal/emerald — pill fills, glow borders, icon circles, teal highlights |
| `--accent-glow` | `rgba(16, 185, 129, 0.70)` | Border glow variant — use on teal-outline pills and frame borders |
| `--accent-fill-subtle` | `rgba(16, 185, 129, 0.12)` | Low-opacity teal fill — icon circle backgrounds, pill bg on footage |
| `--accent-dark` | `#0D9488` | Darker teal — active/highlighted states, solid filled buttons |

---

## Glass Panel Recipe

```css
background: rgba(255,255,255,0.07);
backdrop-filter: blur(20px) saturate(180%);
-webkit-backdrop-filter: blur(20px) saturate(180%);
border: 1px solid rgba(255,255,255,0.10);
border-radius: 12px;
box-shadow: 0 8px 32px rgba(0,0,0,0.40), inset 0 1px 0 rgba(255,255,255,0.08);
```

For overlays on top of footage (not on `--bg`), lower the blur to `blur(12px)` and raise the fill to `rgba(255,255,255,0.10)` so the panel reads against motion.

---

## Typography

| Token | Value |
|-------|-------|
| Font family | `'Space Grotesk', system-ui, sans-serif` |
| HyperFrames | Auto-resolved — write `font-family: 'Space Grotesk'` in CSS, no import needed |
| Headline size | `48–72px` depending on capsule type |
| Label size | `13–14px`, `font-weight: 500`, `letter-spacing: 0.08em`, `text-transform: uppercase` |
| Body / value size | `36px` (confirmed — callout card Test 1) |
| Line height | `1.15` for headlines, `1.5` for body |

---

## Layout & Safe Zone

| Token | Value |
|-------|-------|
| Canvas | `1920 × 1080px` |
| Safe zone inset | `160px` from all edges |
| Partial overlay max width | `480px` |
| Partial overlay max height | `280px` |
| Full-screen content max width | `1200px` centred |

---

## Motion Defaults

| Event | Value |
|-------|-------|
| Entrance | `300ms ease-out` |
| Hold | driven by script timing |
| Exit | `200ms ease-in` |
| Stagger between list items | `80ms` |
| Number count-up duration | `600ms ease-out` |

Entrance transforms: prefer `translateY(12px) → translateY(0)` + `opacity 0 → 1`. Avoid scale bounces or rotation unless the capsule explicitly calls for it.

---

## GSAP Flash Fix (Mandatory For All Capsules)

Set all initial states in **CSS**, not GSAP. Then use `tl.to()` to animate into view. Never use `gsap.set()` with `tl.from()` — `set()` changes the current value so `from()` sees 0→0, producing no animation and white rendering artifacts.

```css
/* Initial states in CSS — invisible from frame 0, no GSAP involvement */
.bg-blur  { opacity: 0; }
.card     { opacity: 0; }
.title    { opacity: 0; }
```

```js
/* tl.to() animates INTO the visible state */
tl.to('#bg-blur', { opacity: 1, duration: 0.3, ease: 'power2.out' }, 0.1);
tl.to('#card',    { opacity: 1, scale: 1, duration: 0.35, ease: 'power3.out' }, 0.25);
```

Also never use the `background` shorthand when combining an image with a fallback colour — use separate properties:

```css
background-color: #09090b;
background-image: url('...');
background-size: cover;
background-position: center;
```

---

## What Not To Do (Applies To All Capsules)

- No harsh neon, glitch, or over-saturated colour
- No long sentences inside overlay panels (max 8 words per line)
- No busy backgrounds or fake UI behind glass panels
- No generic AI glow without a specific visual idea
- No animations longer than 400ms entrance (feels slow at 1080p preview)
- No font sizes below 13px at 1920×1080 (unreadable at YouTube phone grid)
