# Notes

**Status:** draft — seeded from eRS3CmvrOvA

## References

- `eRS3CmvrOvA/screenshots/frame_0440000ms.jpg` — Card 1: Anthropic pixel robot, "Claude code version 2.1.86 or later". 3 ghost cards right.

## Testing

- Test 1: not run
- Fresh-session test: not run

## Open Questions

- The video likely animates through each card in the deck sequentially (card 1 → card 2 → etc.). Is each card its own Higgsfield generation, or is the full deck animated as a single clip with the front card changing? If individual generations, the ghost cards behind each need to show the remaining unviewed cards.
- The numbered circle in the reference uses just a plain outline circle (not filled) — confirm this is the right style vs. a filled teal circle.
- Consider a HyperFrames-composited approach for better text control: generate the card frame/glass and ghost cards in Higgsfield, then composite the text content (number, icon, body lines) in HyperFrames on top.
