# Mobile Publishing Workflow

Use this reference when Daniel asks from mobile to check, schedule, publish, or delete YouTube videos. The goal is to make the interaction feel like Codex is operating the publishing system directly, while the local automation handles the upload once files enter the Publishing folder.

## Ready-To-Post Definition

A video is available to post when there is a matching pair:

- `{project_id}_publish.mp4` video file
- `{project_id}_metadata.yaml` metadata file

Check both locations:

- `Youtube/Output/6. Review  /{project_id}/`
- `Youtube/Output/7. Publishing/{project_id}/`

Ignore anything inside:

- `Youtube/Output/7. Publishing/{project_id}/published/`

If filenames are nearly the same but not exact, tell Daniel the likely pair and ask before renaming anything. Current Episode 1 is `01-transcript-youtube`.

## Listing Videos

When Daniel asks what videos are ready, answer simply:

```text
These are the videos available to post today:

1. Video One
2. Video Two
3. Video Three

Which one would you like to post?
```

Do not over-explain the folder structure unless there is a problem.

## Before Publishing

After Daniel chooses a video, read its `.yaml` file and give a short plain-English summary.

Keep it brief:

```text
Codex Mobile is ready to post.

The description explains that the video is about [simple summary]. It includes the description, timestamps, tags, and upload settings.

Would you like me to publish it now or schedule it?
```

If the metadata looks wrong, say so clearly:

```text
Codex Mobile is available, but the description does not look right. It appears to be about [other topic].

Would you like me to fix the metadata before publishing, or should I leave it as-is for this test?
```

Only fix metadata or filenames after Daniel confirms.

## Scheduling Or Publishing

If Daniel says to publish or schedule, move the selected pair into:

`Youtube/Output/7. Publishing/{project_id}/`

Move both files together:

- the `.mp4`
- the matching `.yaml`

Do not move files directly into `published/`. The automation moves files there after a successful upload.

If Daniel gives a specific schedule, confirm the date in plain language. For example, if today is Saturday, May 16, 2026, then "following Friday at 4 p.m." means Friday, May 22, 2026 at 4:00 PM London.

## YouTube Studio

After moving the pair into Publishing:

1. Open YouTube Studio channel content / Manage Videos.
2. Keep the YouTube Studio tab open.
3. Refresh Channel Content every 10 seconds for up to 1 minute 30 seconds.
4. Stop early if the task is confirmed complete.
5. After completion, open the uploaded/scheduled YouTube video URL in a new browser tab.
6. Refresh the uploaded/scheduled video page every 10 seconds for up to 1 minute so the page has time to process/load.
7. Then show the Apple Notes completion message on top of the browser.

Completion can be confirmed by:

- the file pair moving into `Youtube/Output/7. Publishing/{project_id}/published/`
- a new row appearing in `Youtube/Output/9. Analytics/upload_log.md`
- a YouTube API check confirming the video state

## Apple Notes Status

After a publish, schedule, or delete task completes, show Apple Notes on top of the browser and add a short friendly note. Finish with the uploaded/scheduled YouTube video tab active behind the note window.

Preferred presentation:

- Use the Apple Notes app, not TextEdit.
- Create the status note, then open that note in its own separate window using Notes' `Window > Open Note in New Window`.
- Close the main Notes list/window afterward, leaving only the small individual note window visible.
- Center the individual note window over the browser.
- Make the message large and bold, similar to header/title-style text.
- Keep both browser tabs open behind the note: YouTube Studio channel content and the uploaded/scheduled video page.
- Return focus to the browser after writing the note, select the uploaded/scheduled YouTube video tab, then leave the small note window floating on top.
- The final visible browser page behind the note should be the uploaded/scheduled YouTube video page, not YouTube Studio.
- Include the short working video name, not only the long YouTube title. Examples: `YouTube Transcript`, `Codex Mobile`, `Prompts Explained`.
- Verify Notes has exactly one visible individual note window after opening it. If the main Notes list/window appears, close it and leave the individual note window open.

Example:

```text
Hi Daniel, this is your publishing agent.

YouTube Transcript has been scheduled successfully. I opened the video link and left YouTube Studio open so you can check all the details.
```

For scheduled videos, include the scheduled date:

```text
Hi Daniel, this is your publishing agent.

YouTube Transcript has been scheduled for Friday, May 22, 2026 at 4:00 PM London.

I opened the video link and left YouTube Studio open so you can check any details.
```

Use normal capitalization, not all caps.

## Deleting Test Videos

If Daniel asks to delete a scheduled test video:

1. Identify the exact target using the upload log and/or YouTube Studio.
2. Confirm the title, video ID, URL, and scheduled date if there is any ambiguity.
3. Delete only the requested test video.
4. After deletion is confirmed, move the local publish pair back to the matching Review folder so the test can be run again from the start:
   - From: `Youtube/Output/7. Publishing/{project_id}/published/{project_id}_publish.mp4`
   - From: `Youtube/Output/7. Publishing/{project_id}/published/{project_id}_metadata.yaml`
   - To: `Youtube/Output/6. Review  /{project_id}/`
5. Move both files together. Do not leave one file in `published/` and one file in Review.
6. Refresh YouTube Studio every 10 seconds for up to 1 minute.
7. Stop early once deletion is confirmed.
8. Add a friendly Apple Notes status message.

Use the local helper when appropriate:

```bash
"Youtube/Input/4. Resources/7. publishing_resources/venv/bin/python3" \
  "Youtube/Input/4. Resources/7. publishing_resources/delete_videos.py" VIDEO_ID
```

Confirm deletion with an API check when possible. `FOUND=0` means the video is gone.

After a successful test deletion, the local pair should end in Review, not in Publishing or `published/`.

## Tone

Daniel is recording this workflow as an automation demo, so keep responses natural and operational:

- Say "publish", "schedule", and "posted" in user-facing language.
- Do not say "move the pair" unless Daniel asks about implementation.
- Keep summaries short.
- Ask only the necessary confirmation question.
