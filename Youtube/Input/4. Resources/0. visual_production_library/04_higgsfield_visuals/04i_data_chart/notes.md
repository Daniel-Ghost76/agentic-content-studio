# Notes

**Status:** draft — seeded from eRS3CmvrOvA

## References

- `eRS3CmvrOvA/screenshots/frame_0534000ms.jpg` — "Claude benchmark" two-line compression chart with 299b/109b endpoints

## Testing

- Test 1: not run
- Fresh-session test: not run

## Open Questions

- Higgsfield may struggle to generate reliable chart animations with accurate data points. Consider generating the dark background and atmosphere in Higgsfield, then building the actual chart (axes, lines, labels) in HyperFrames/D3 composited on top for accuracy.
- The legend pills at the bottom have a specific style (rounded pill, filled circle on left, text on right) that matches the `02f_icon_pill` aesthetic — they may be the same component used in two different contexts.
- Y-axis in the reference uses a logarithmic-style scale (300kb, 10kb, 500b, 100b, 0b are not linearly spaced) — verify whether HyperFrames or the chart library can handle this scale type.
