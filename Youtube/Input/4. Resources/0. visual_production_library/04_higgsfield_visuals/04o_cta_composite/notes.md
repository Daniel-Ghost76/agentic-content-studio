# Notes

**Status:** draft — seeded from eRS3CmvrOvA

## References

- `eRS3CmvrOvA/screenshots/frame_0803000ms.jpg` — Variant A: "FREE SKOOL COMMUNITY" + Skool browser (Nate Herk's community, posts visible, leaderboard visible)
- `eRS3CmvrOvA/screenshots/frame_0813000ms.jpg` — Variant B: YouTube player end card, "I Tried 100+ Claude Code Skills, These 6 are the Best", like button animation, "697K subscribers"

## Testing

- Test 1: not run
- Fresh-session test: not run

## Open Questions

- Variant B (YouTube player) is a sophisticated animation that Higgsfield likely cannot generate accurately. Strongly recommend building this as a HyperFrames HTML composition — mock the YouTube UI in code, animate the cursor and like button programmatically.
- For Variant A, the browser window in the reference shows a very specific community platform (Skool) with real posts and member names. This will need to be a screenshot composite, not Higgsfield-generated, to avoid hallucinated or inaccurate content.
- Consider whether the "check out this video" end card (pointing up-right to a suggested video) should be a third variant of this capsule, or a separate `04p` capsule.
