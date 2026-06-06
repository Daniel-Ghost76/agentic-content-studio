# Notes

**Status:** approved

## References

No approved references yet. Source from: Dribbble (step list card, numbered list UI), Layers, CollectUI.

## Testing

- Test 1: ✅ passed — 3 steps, title "THE PROCESS", right-centre, 500ms stagger. Sequential build confirmed across 3 frames. Typography clean.
- Test 2: ✅ passed — 4 steps, no title, bottom-right, 500ms stagger. Title-less layout compact and clean. 4-step max confirmed.
- Test 3: ✅ passed — 2 steps, title, right-centre, 80ms auto-cascade. Both steps fire near-simultaneously. Compact 2-step layout good.
- Fresh-session test: pending

## Open Questions For Build Session

- Should completed steps dim or stay bright when the next step appears?
- Auto-stagger vs. cue-based reveal — which is more practical in HyperFrames for the editing workflow?
- Should there be a thin horizontal divider between steps, or clean spacing only?
