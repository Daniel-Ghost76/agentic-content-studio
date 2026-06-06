# Selection Matrix

Use this matrix to choose the right sub-library before creating a visual.

| Need | First Library To Check | Capsules Available | Typical Tool | Notes |
|------|------------------------|--------------------|--------------|-------|
| Daniel records from slides or diagrams | `01_pre_production_materials/` | — | deterministic renderer or image generation | Stage 3 only — deferred |
| Label / callout on top of footage | `02_partial_overlays_hyperframes/` | `02a_callout_card` ✅ · `02b_stat_metric_card` · `02c_step_list` | HyperFrames | Must not cover face or key UI |
| Number or metric reveal | `02_partial_overlays_hyperframes/` | `02b_stat_metric_card` ✅ | HyperFrames | Count-up animation available |
| Numbered steps building in over footage | `02_partial_overlays_hyperframes/` | `02c_step_list` ✅ | HyperFrames | Max 4 steps |
| Chapter break or section divider | `03_full_screen_overlays/` | `03a_chapter_break` ✅ | HyperFrames | Replaces footage 2–4s |
| Process / pipeline / architecture diagram | `03_full_screen_overlays/` | `03b_workflow_map` | HyperFrames | Nodes build in sequentially |
| Screenshot or result as proof | `03_full_screen_overlays/` | `03c_proof_screen` | HyperFrames | Documentary frame around screenshot |
| Abstract AI / tech b-roll | `04_higgsfield_visuals/` | `04a_ai_tech_hud` | Higgsfield | Data-flow, atmospheric |
| Before/after or transformation visual | `04_higgsfield_visuals/` | `04b_workflow_transformation` | Higgsfield | Clear start and resolved final frame |
| Atmospheric metaphor or concept visual | `04_higgsfield_visuals/` | `04c_abstract_concept` | Higgsfield | Use `{atmosphere_description}` precisely |
| Single impact word on screen | `05_emphasis_word_overlays/` | `05a_punch_word` | HyperFrames | Hook payoffs only — max 2× per video |
| Old vs new / before vs after phrase | `05_emphasis_word_overlays/` | `05b_two_word_contrast` | HyperFrames | Sequential reveal, A dim → B bright |
| Thesis line or memorable quote | `05_emphasis_word_overlays/` | `05c_quote_highlight` | HyperFrames | Word-by-word reveal, optional underline |
| Subscribe prompt | `06_cta_subscribe_visuals/` | `06a_subscribe_ask` | HyperFrames | Quiet pill — after value is delivered |
| Next video tease | `06_cta_subscribe_visuals/` | `06b_next_video_tease` | HyperFrames | Bottom-right, final 20–30s |
| Comment prompt / question CTA | `06_cta_subscribe_visuals/` | `06c_comment_prompt` | HyperFrames | Daniel's question on screen |
| Thumbnail concept or final thumbnail | `07_thumbnails/` | — | thumbnail renderer + optional image generation | Stage 6 Review — deferred |

## Common Choices

- Educational concept: pre-production material, full-screen overlay, or emphasis word overlay.
- Product/tool demo: pre-production material, partial overlay, proof screen, thumbnail.
- Abstract AI workflow: Higgsfield visual or full-screen overlay.
- Strong quote/punchline: emphasis word overlay.
- Outro ask: CTA / subscribe visual.
- Publishing/review packaging: thumbnail library.

## Fallback

If no capsule fits, create a new draft capsule from `_templates/capsule_template/`, test it, and keep it marked `draft` until Daniel approves it.

