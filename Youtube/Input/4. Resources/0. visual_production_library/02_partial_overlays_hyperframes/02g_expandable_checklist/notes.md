# Notes

**Status:** draft — seeded from eRS3CmvrOvA

## References

- `eRS3CmvrOvA/screenshots/frame_0610000ms.jpg` — "PLAIN TEXT FILES" pill + "Claude.md" item (1 of 2)
- `eRS3CmvrOvA/screenshots/frame_0615000ms.jpg` — "PLAIN TEXT FILES" pill + "Claude.md" + "Memory files" (both visible)

## Testing

- Test 1: not run
- Fresh-session test: not run

## Open Questions

- The card in the reference has a very slight rounded top-left/right as well — verify whether the pill and card should overlap slightly (pill overlapping card top by ~8px) or be flush adjacent.
- The checkmark icons in the reference appear to be green (slightly different from teal) — could be a lighter #22C55E vs #10B981. Test both.
- The second item ("Memory files") appears dimmer/greyed out while "Claude.md" is bright — suggests items may dim after the active item moves to the next one. Consider an `active state` vs `completed state` for each item.
