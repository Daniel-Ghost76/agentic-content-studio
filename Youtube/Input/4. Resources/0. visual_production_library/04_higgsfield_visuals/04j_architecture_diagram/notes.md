# Notes

**Status:** draft — seeded from eRS3CmvrOvA

## References

- `eRS3CmvrOvA/screenshots/frame_0151000ms.jpg` — SKILL → Markdown → Claude (Hooks/Edits/Offers/Design) horizontal node diagram with teal frame

## Testing

- Test 1: not run
- Fresh-session test: not run

## Open Questions

- The "Claude" node in the reference is a rectangle (not a circle) containing a 2×2 icon grid — this is a hybrid node type. The prompt handles this with the "rounded rectangle box with grid" description, but test whether Higgsfield renders it accurately.
- The teal label pill at the top-center of the frame (reading "SKILL") matches the `04e_section_intro_circle` pill style — could reuse that component. Consider whether to add a `{header_pill}` variable to make the top label optional and configurable.
- This diagram type could also be built entirely in HyperFrames (D3/Canvas based) for perfect accuracy. Higgsfield for the atmospheric background + frame, HyperFrames for the actual diagram nodes and connections.
