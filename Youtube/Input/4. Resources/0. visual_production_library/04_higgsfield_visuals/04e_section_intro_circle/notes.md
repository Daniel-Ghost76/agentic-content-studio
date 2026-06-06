# Notes

**Status:** draft — seeded from eRS3CmvrOvA

## References

- `eRS3CmvrOvA/screenshots/frame_0091000ms.jpg` — "SKILL CREATOR" — clean single circle in teal frame
- `eRS3CmvrOvA/screenshots/frame_0360000ms.jpg` — "SUPERPOWERS" variant with title above and Anthropic icon below — slightly more complex layout

## Testing

- Test 1: not run
- Fresh-session test: not run

## Open Questions

- Frame 0360 shows a variant where the section name ("SUPERPOWERS") is a title ABOVE the rectangle frame (not inside the circle), and the circle contains only the "Process" pill + Anthropic icon. This might warrant a separate capsule variant (`04e_b_section_process_variant`) or a prompt variable flag.
- Does Higgsfield reliably generate legible text inside shapes? If not, consider generating the circle/frame background in Higgsfield and compositing the text in HyperFrames on top.
