# Thumbnail Workflow

This workflow creates a repeatable thumbnail package for approved videos in the Review stage.

## Inputs

Default review root:
`Youtube/Output/6. Review  /`

Before generating concepts, read:

```text
Youtube/Input/4. Resources/0. visual_production_library/README.md
Youtube/Input/4. Resources/0. visual_production_library/selection_matrix.md
Youtube/Input/4. Resources/0. visual_production_library/07_thumbnails/
```

If no target is provided, use the newest subfolder in the review root.

Input priority inside the target folder:
1. `.txt` transcript
2. `.srt` transcript
3. matching script PDF from `Youtube/Output/2. Scripts/`

The review folder is the approval signal. If a video has reached Review, it is ready for thumbnail work.

## Outputs

Save both files inside the target review folder:

- `{project_id}_thumbnail_concepts.md`
- `{project_id}_thumbnail.png`

Never overwrite an existing thumbnail unless the user explicitly asks for replacement.

## Concept Generation

Create three concepts. Each concept must include:

- short hook text, 2-5 words
- chosen Visual Production Library thumbnail capsule
- visual metaphor
- face placement
- background idea
- supporting UI/app/tool elements
- score out of 10 for curiosity, clarity, emotional punch, and YouTube readability

Recommend one concept and render that final thumbnail first.

## Rendering

Use the local renderer:

```bash
python3 "Youtube/Input/5. Tools/6. review_tools/thumbnail_renderer.py"
```

Common commands:

```bash
# Newest Review folder, requires a face image for the final thumbnail.
python3 "Youtube/Input/5. Tools/6. review_tools/thumbnail_renderer.py" --face "/path/to/daniel-photo.png"

# Explicit target.
python3 "Youtube/Input/5. Tools/6. review_tools/thumbnail_renderer.py" "01-transcript-youtube" --face "/path/to/daniel-photo.png"

# Concepts only, no final image.
python3 "Youtube/Input/5. Tools/6. review_tools/thumbnail_renderer.py" --concepts-only

# Pipeline test without a face photo. Use only for setup validation.
python3 "Youtube/Input/5. Tools/6. review_tools/thumbnail_renderer.py" --allow-placeholder --overwrite
```

## Face Photo Policy

For real thumbnails, use Daniel's attached face photo as the canonical person reference.

If no face photo is available:

- still generate concept notes
- do not create a production final thumbnail
- only use placeholder mode when testing the system

## Image Generation Policy

Use AI image generation for optional supporting assets when needed, especially:

- stylized backgrounds
- software/product mockups
- graphic objects
- face cutouts or background extension

The final composition should still be created by the deterministic local renderer so layout, dimensions, and text remain consistent.
