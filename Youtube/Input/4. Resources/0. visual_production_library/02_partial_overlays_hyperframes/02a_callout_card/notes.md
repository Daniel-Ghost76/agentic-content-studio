# Notes

**Status:** approved

## References

No approved references yet. Source from: Dribbble (callout card, lower third), Layers (glass UI card), Motionsites.

## Testing

- Test 1: ✅ passed — `{label}: TOOL`, `{value}: Claude Code`, `{position}: bottom-right`. Value bumped 28px→36px during test, approved. Font Space Grotesk confirmed loading. 0 errors, 1 non-blocking font warning (acceptable — online renders resolve correctly).
- Test 2: ✅ passed — `{label}: STAGE`, `{value}: Editing`, `{position}: bottom-left`, `{entrance_from}: left`. Card appeared bottom-left, slid in from left correctly. Variables generalise.
- Test 3: ✅ passed — `{label}: CONCEPT`, `{value}: Agentic Workflow`, `{position}: bottom-right`, `{entrance_from}: bottom`. Longer two-word value, bottom entrance. Card width expanded naturally, layout held. 
- Fresh-session test: pending

## Open Questions For Build Session

- Should the label be above or below the value, or is it configurable per use?
- Should the panel have a subtle left-side accent bar (coloured strip) or stay pure glass?
- Does the position variable need a third option (bottom-centre) for certain moments?
