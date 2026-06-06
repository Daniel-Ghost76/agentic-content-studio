# Notes

**Status:** draft — seeded from eRS3CmvrOvA

## References

- `eRS3CmvrOvA/screenshots/frame_0046000ms.jpg` — all 5 items visible in 2-column grid, none highlighted yet (video opening)
- `eRS3CmvrOvA/screenshots/frame_0276000ms.jpg` — "2 SUPER POWERS" highlighted bright, "SKILL CREATOR" and others dimmed

## Testing

- Test 1: not run
- Fresh-session test: not run

## Open Questions

- In frame_0046000ms all items appear equally dimmed — is this a "before any section starts" state? If so, the `{active_index}` variable could be set to `0` (none) for the opening overview shot.
- The macOS dock in the reference shows Photos, Notion, App Store, System Preferences, Final Cut Pro icons — these are the creator's actual dock. For Daniel's version, we can swap to more relevant icons (Claude, VSCode, Telegram, etc.) but this detail requires Higgsfield to render specific icons, which may not be reliable.
- Consider whether a HyperFrames-composited version (generate the window frame in Higgsfield, composite the text/items in HyperFrames) would give better text control for the labels.
