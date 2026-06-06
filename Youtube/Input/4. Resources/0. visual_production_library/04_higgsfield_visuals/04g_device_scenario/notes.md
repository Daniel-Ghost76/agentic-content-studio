# Notes

**Status:** draft — seeded from eRS3CmvrOvA

## References

- `eRS3CmvrOvA/screenshots/frame_0107000ms.jpg` — Phone, teal glow, "Real estate agency" / "We waste hours every week" messaging UI

## Testing

- Test 1: not run
- Fresh-session test: not run

## Open Questions

- The messaging UI in the reference uses a blue bubble (iOS iMessage style) — this suggests the scenario is shown as if from the client's perspective (they're the ones sending the message). Consider whether to keep this convention.
- The teal glow outline is quite pronounced — appears to be a composite (device photo + teal outline added in post). Higgsfield may need a strong prompt to achieve this. Consider whether to use Higgsfield for the background/glow and composite the actual device frame + screen content in HyperFrames.
- Text legibility: Higgsfield may struggle to render specific text reliably. If so, generate the device/background as a Higgsfield clip, then overlay actual readable text in HyperFrames.
