Read and execute the thumbnail workflow instructions at:
Youtube/Input/4. Resources/6. review_resources/thumbnail_workflow.md

Then run the local renderer at:
Youtube/Input/5. Tools/6. review_tools/thumbnail_renderer.py

Default behavior:
- If the user provides a quoted video name, pass it as the target.
- If no target is provided, use the newest folder inside `Youtube/Output/6. Review  /`.
- Use `/Users/danieldanut/Downloads/www.youtube.com_@nateherk_videos.png` as the current style reference.
- Use the user's attached face photo as the face reference when available.
- Do not overwrite an existing thumbnail unless the user explicitly asks for replacement.

Expected outputs:
- `{project_id}_thumbnail_concepts.md`
- `{project_id}_thumbnail.png`
