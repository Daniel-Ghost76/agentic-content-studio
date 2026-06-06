# Notes

**Status:** draft — seeded from eRS3CmvrOvA

## References

- `eRS3CmvrOvA/screenshots/frame_0002000ms.jpg` — "Claude code / 0hrs → 400hrs" opening hero

## Testing

- Test 1: not run
- Fresh-session test: not run

## Open Questions

- The background screenshot panels in the reference are very dark and blurred — does Higgsfield handle this level of blur naturally, or should we provide a pre-composited background image as a reference frame?
- The progress bar in the reference has a dark teal fill showing partial progress (not full) — this suggests the bar is animated from empty to partial. Consider whether to ask Higgsfield to animate this or composite it separately in HyperFrames post-generation.
- Test whether supplying two DALL-E reference frames (first + last) gives Higgsfield enough to interpolate a clean motion sequence, vs. providing a single reference.
