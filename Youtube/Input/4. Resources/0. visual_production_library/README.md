# Visual Production Library

This is the master reference library for every reusable visual choice in the YouTube pipeline.

Use it for:

- pre-production slides and recording materials
- partial overlays built with HyperFrames
- full-screen visual overlays
- Higgsfield visual clips and prompts
- emphasis word overlays
- CTA / subscribe visuals
- thumbnails

## How Agents Use This Library

When Daniel says, "I want to work on the visual production library," ask:

```text
Which sub-library do you want to work on?

1. Pre-production materials
2. Partial overlays with HyperFrames
3. Full-screen overlays
4. Higgsfield visuals
5. Emphasis word overlays
6. CTA / subscribe visuals
7. Thumbnails
```

After Daniel chooses one, open that sub-library README and start with its starter question.

When generating assets for a real episode, do not invent a style from memory. First check `selection_matrix.md`, then choose the closest approved capsule in the relevant sub-library. If no approved capsule fits, ask Daniel whether to build a new capsule.

## Capsule Contract

Each reusable visual option lives in one capsule folder:

```text
capsule_name/
├── README.md
├── prompt.md
├── reference_images/
├── reference_videos/
├── test_outputs/
└── notes.md
```

The reference images/videos, exact prompt, notes, and test outputs stay together. Do not split the prompt away from its references.

## Approval Standard

A capsule is approved only when:

- it has at least one reference image or video, unless it is a pure code-native HyperFrames preset
- `prompt.md` contains the exact current prompt
- at least 3 test outputs have been reviewed
- the prompt has been tested once in a fresh chat/session
- `notes.md` says `Status: approved`

If the fresh-session test does not land close to the references, keep the capsule in draft.

## Output Notes

Every stage that uses this library must name the capsule it used in its output note:

- Stage 3: `{project_id}_production_note.md`
- Stage 4: `{project_id}_project.md` and/or `{project_id}_overlay_map.md`
- Stage 5: `{project_id}_overlay_check.md`
- Stage 6: `{project_id}_thumbnail_concepts.md`

## Seeding Capsules from Reference Videos

Use `/reverse-engineer` to analyze a finished YouTube video and propose new capsules based on what you observe. When a new draft capsule is proposed from a reference video:

1. Review the `_reverse_analysis.md` — confirm the pattern is genuinely reusable, not specific to that one video
2. Confirm the proposed design tokens fit or intentionally extend the channel design system (`_channel_design_system.md`)
3. Accept the draft capsule as-is — it starts at 0 tests
4. Run 3 test outputs + 1 fresh-session test before changing status to approved
5. Never promote a reference-seeded capsule to approved in the same session it was created

Reference-seeded capsules carry this marker in `notes.md`:
```
Status: draft — seeded from {VIDEO_ID}
```

Analyzed reference videos are stored at:
```
Youtube/Output/4. Editing/reference_videos/{VIDEO_ID}/
```

