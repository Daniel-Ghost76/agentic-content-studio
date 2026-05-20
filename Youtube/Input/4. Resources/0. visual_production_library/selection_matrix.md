# Selection Matrix

Use this matrix to choose the right sub-library before creating a visual.

| Need | First Library To Check | Typical Tool | Notes |
|------|------------------------|--------------|-------|
| Daniel records from slides or diagrams | `01_pre_production_materials/` | deterministic renderer or image generation | Stage 3 only |
| Small card/callout on top of footage | `02_partial_overlays_hyperframes/` | HyperFrames | Must not cover face or key UI |
| Full-screen animated explainer or chapter break | `03_full_screen_overlays/` | HyperFrames, Remotion, or generated video | Usually replaces footage temporarily |
| Cinematic/generated AI visual clip | `04_higgsfield_visuals/` | Higgsfield | Prompt must include anti-list and duration |
| Designed key words or phrases, not subtitles | `05_emphasis_word_overlays/` | HyperFrames | Use sparingly for punchlines and pivots |
| Like/subscribe/next-video visual | `06_cta_subscribe_visuals/` | HyperFrames or deterministic renderer | Keep YouTube-native, not corporate |
| Thumbnail concept or final thumbnail | `07_thumbnails/` | thumbnail renderer + optional image generation | Stage 6 Review |

## Common Choices

- Educational concept: pre-production material, full-screen overlay, or emphasis word overlay.
- Product/tool demo: pre-production material, partial overlay, proof screen, thumbnail.
- Abstract AI workflow: Higgsfield visual or full-screen overlay.
- Strong quote/punchline: emphasis word overlay.
- Outro ask: CTA / subscribe visual.
- Publishing/review packaging: thumbnail library.

## Fallback

If no capsule fits, create a new draft capsule from `_templates/capsule_template/`, test it, and keep it marked `draft` until Daniel approves it.

