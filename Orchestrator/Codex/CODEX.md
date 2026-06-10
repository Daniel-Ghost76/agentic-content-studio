# CODEX.md

## Purpose

This file is the Codex operating guide for Daniel's YouTube production workspace.

The main production system is split between Claude Code and Codex. Claude owns most planning, scripting, editing, review, publishing, distribution, and analytics stages. Codex owns Stage 3 Pre-production Materials, Stage 5 Visuals / Overlays, and mobile orchestration from Daniel's phone.

Before doing project work, read this file, then read any stage-specific files for the part of the pipeline you are touching.

## Business Context

The channel supports this funnel:

`YouTube free value -> Skool community -> AI implementation services`

The content direction is build-in-public: Daniel is showing the real process of building an AI business from scratch, including imperfect demos, mistakes, setup work, tool choices, and practical workflow automation.

The target viewer is practical, non-technical or semi-technical: small business owners, freelancers, people exploring AI as a career or business, and people who want to use AI tools in real workflows.

## Workspace Map

Root:

```text
Youtube/
├── Input/   # agents, rules, skills, tools, resources
└── Output/  # produced assets and pipeline outputs
```

Claude project config:

```text
.claude/
├── CLAUDE.md             # main project structure and business context
├── codex.md              # this Codex guide
└── commands/
    ├── analytics.md
    ├── publish.md
    └── thumbnails.md
```

Input structure:

```text
Youtube/Input/
├── 1. Sub-agents/        # stage agent instructions
├── 2. Skills/            # how each stage executes
├── 3. Rules/             # hard rules and quality bars
├── 4. Resources/         # references, credentials, briefs, style guides
└── 5. Tools/             # local scripts and tool projects
```

Output structure:

```text
Youtube/Output/
├── 1. Ideation/          # idea PDFs
├── 2. Scripts/           # approved scripts
├── 3. Pre-production Materials/ # slides and recording materials
├── 4. Editing/           # raw footage and cut edits
├── 5. Visuals/           # post-production overlays and visual polish
├── 6. Review  /          # reviewed packages, thumbnails, metadata
├── 7. Publishing/        # videos ready for upload, plus published/
├── 8. Distribution/      # cross-platform distribution assets
└── 9. Analytics/         # upload log, Day 7/30 snapshots, rollups
```

Important path details:

- `Youtube/Output/6. Review  /` has two spaces before the slash in the actual folder name.
- Every Output stage uses a project folder named with the permanent project ID.
- Published videos live inside each project folder at `Youtube/Output/7. Publishing/{project_id}/published/` and should not be reprocessed unless Daniel explicitly asks.

## Canonical Project Naming

Every video uses one project ID from Stage 1 through Stage 9:

```text
Youtube/Output/{stage}/{project_id}/{project_id}_{suffix}.{ext}
```

Examples:

```text
Youtube/Output/2. Scripts/02_codex_mobile/02_codex_mobile_script.pdf
Youtube/Output/3. Pre-production Materials/02_codex_mobile/02_codex_mobile_slide_01.png
Youtube/Output/4. Editing/02_codex_mobile/02_codex_mobile_raw.mp4
Youtube/Output/5. Visuals/02_codex_mobile/02_codex_mobile_overlaid.mp4
Youtube/Output/6. Review  /02_codex_mobile/02_codex_mobile_review.mp4
Youtube/Output/7. Publishing/02_codex_mobile/02_codex_mobile_publish.mp4
Youtube/Output/9. Analytics/02_codex_mobile/02_codex_mobile_analytics_d07.md
```

Current Episode 1 project ID is `01-transcript-youtube`. Daniel explicitly renamed it; never use any previous Day 1 ID for that project.

Codex must not invent project names for Stage 3, Stage 5, or mobile publishing. Read the upstream project folder or artifact prefix and keep it unchanged.

When an idea has been accepted and Script Draft 1 exists, the project should already have folders in every Output stage. If Codex notices an active scripted project without the full folder set, create the missing empty folders before continuing.

## Stage Ownership

Stage ownership is explicit:

| Stage | Primary owner | Codex role |
|-------|---------------|------------|
| 1 Ideation | Claude Code | Inspect state, summarize, run commands if asked |
| 2 Scripting | Claude Code | Inspect scripts, summarize, help locate files |
| 3 Pre-production Materials | Codex | Execute slides, diagrams, and recording materials |
| 4 Editing | Claude Code | Inspect or support only when explicitly assigned |
| 4a Cut Edit | Claude Code | Inspect or support only when explicitly assigned |
| 5 Visuals / Overlays | Codex | Execute overlays, motion graphics, and visual polish |
| 5a Overlay Compositing | Codex | Render and composite overlays on cut videos |
| 6 Review | Claude Code | Ready-to-post checks and thumbnails when asked |
| 7 Publishing | Claude Code by default | Mobile orchestration when Daniel asks from Codex |
| 8 Distribution | Claude Code | Inspect status or run local commands if asked |
| 9 Analytics | Claude Code | Run or summarize analytics when requested |

## What Codex Should Read For Each Task

For any stage-specific task, read the matching files before acting:

```text
Youtube/Input/1. Sub-agents/{N}. {Stage}/{stage}_sub-agent.md
Youtube/Input/2. Skills/{N}. {Stage}/{stage}_skill.md  (folder may contain multiple skill files — read all)
Youtube/Input/3. Rules/{N}. {Stage}/{stage}_rules.md
Youtube/Input/4. Resources/{stage}_resources/
Youtube/Input/5. Tools/{stage}_tools/
```

## Codex Core Responsibilities

### 1. Mobile Orchestration

When Daniel uses Codex from mobile, keep the interaction operational and short.

Typical jobs:

- Check what videos are ready to post.
- Read metadata and summarize it plainly.
- Move approved video packages into Publishing.
- Run the publishing script with the requested schedule.
- Open YouTube Studio and the video URL.
- Leave a friendly Apple Notes completion message.
- Report system status or command results.

Use this workflow for mobile publishing:

`Youtube/Input/5. Tools/7. publishing_tools/mobilepublishing.md`

### 1a. Stage 3 Pre-production Materials

Codex owns Stage 3.

Read:

```text
Youtube/Input/1. Sub-agents/3. Pre-production Materials/3. pre-production_materials_sub-agent.md
Youtube/Input/2. Skills/3. Pre-production Materials/3. pre-production_materials_skill.md
Youtube/Input/3. Rules/3. Pre-production Materials/3. pre-production_materials_rules.md
Youtube/Input/4. Resources/3. pre-production_materials_resources/
Youtube/Input/5. Tools/3. pre-production_materials_tools/
```

Output goes to:

```text
Youtube/Output/3. Pre-production Materials/{project_id}/
```

### 1b. Stage 5 Visuals / Overlays

Codex owns Stage 5 and Stage 5a.

Read:

```text
Youtube/Input/1. Sub-agents/5. Visuals/5. visuals_sub-agent.md
Youtube/Input/1. Sub-agents/5. Visuals/5a. overlays_sub-agent.md
Youtube/Input/2. Skills/5. Visuals/5. visuals_skill.md
Youtube/Input/2. Skills/5. Visuals/5a. overlays_skill.md
Youtube/Input/3. Rules/5. Visuals/5. visuals_rules.md
```

Final overlaid outputs go to:

```text
Youtube/Output/5. Visuals/{project_id}/{project_id}_overlaid.mp4
```

### 2. Ready-To-Post Checks

For mobile ready-to-post checks, a video is available when there is an exact matching pair:

- `.mp4` video file
- `.yaml` metadata file with the same base filename

Check both:

```text
Youtube/Output/6. Review  /{project_id}/
Youtube/Output/7. Publishing/{project_id}/
```

Ignore:

```text
Youtube/Output/7. Publishing/{project_id}/published/
```

If the filename pair is not exact but looks close, tell Daniel the likely pair and ask before renaming anything.

When listing available videos, keep it simple:

```text
These are the videos available to post today:

1. Video One
2. Video Two
3. Video Three

Which one would you like to post?
```

If metadata looks wrong, say so before publishing.

### 3. Publishing

Publishing must always be scheduled, never immediate.

Core rules:

- Read `Youtube/Input/3. Rules/7. Publishing/7. publishing_rules.md` before publishing.
- Confirm title, metadata summary, and schedule with Daniel before upload.
- Move selected `.mp4` + matching `.yaml` into `Youtube/Output/7. Publishing/{project_id}/`.
- Do not move files into `published/` manually until the YouTube API returns a successful video ID.
- Use the publishing venv Python:

```bash
"Youtube/Input/4. Resources/7. publishing_resources/venv/bin/python3"
```

Upload script:

```bash
"Youtube/Input/4. Resources/7. publishing_resources/upload_to_youtube.py"
```

Schedule helper:

```bash
"Youtube/Input/4. Resources/7. publishing_resources/schedule_slots.py"
```

After a successful upload:

- Move the `.mp4` and `.yaml` to `Youtube/Output/7. Publishing/{project_id}/published/`.
- Append one row to `Youtube/Output/9. Analytics/upload_log.md`.
- Open YouTube Studio and the uploaded/scheduled video URL.
- Create the Apple Notes status message as described in `mobilepublishing.md`.

Apple Notes final screen rule:

- Only the small individual note window should remain visible.
- Close the main Notes list/window where possible.
- End with the uploaded/scheduled YouTube video tab active behind the note.

### 4. Thumbnail Work

Thumbnail work is one of the places Codex may help.

Read:

```text
.claude/commands/thumbnails.md
Youtube/Input/4. Resources/6. review_resources/thumbnail_workflow.md
Youtube/Input/4. Resources/6. review_resources/thumbnail_style_guide.md
```

Default review root:

```text
Youtube/Output/6. Review  /
```

Expected outputs inside the target review folder:

```text
{project_id}_thumbnail_concepts.md
{project_id}_thumbnail.png
```

Do not overwrite existing thumbnails unless Daniel explicitly asks.

For real thumbnails, use Daniel's attached face photo when provided. If no face photo is available, generate concepts only unless Daniel approves placeholder mode.

### 5. Editing Support

Claude Code owns cut editing. Codex owns overlay workflows after the cut edit is complete.

Before any editing work, read:

```text
Youtube/Input/1. Sub-agents/4. Editing/4. editing_sub-agent.md
Youtube/Input/1. Sub-agents/4. Editing/4b. cut_edit_sub-agent.md
Youtube/Input/2. Skills/4. Editing/4b. cut_edit_skill.md
Youtube/Input/3. Rules/4. Editing/4. editing_rules.md
```

Hard editing rules:

- Never touch raw files.
- Confirm the plain-English strategy before cutting or rendering.
- One file at a time unless Daniel explicitly says otherwise.
- Verify outputs with `ffprobe`.
- Final video spec: 1920x1080, H.264, AAC 48kHz, 30fps.

## Commands And Useful Checks

List ready-to-post pairs:

```bash
setopt null_glob
for d in "Youtube/Output/6. Review  "/* "Youtube/Output/7. Publishing"/*; do
  [ -d "$d" ] || continue
  for v in "$d"/*.mp4 "$d"/*.MP4; do
    base="${v%.*}"
    if [ -f "$base.yaml" ]; then
      printf 'READY\t%s\t%s\n' "$v" "$base.yaml"
    elif [ -f "$base.yml" ]; then
      printf 'READY\t%s\t%s\n' "$v" "$base.yml"
    fi
  done
done
```

Read upload log:

```bash
sed -n '1,120p' "Youtube/Output/9. Analytics/upload_log.md"
```

Inspect a video:

```bash
ffprobe -v error \
  -show_entries format=duration,size \
  -show_entries stream=codec_type,width,height,avg_frame_rate \
  -of default=noprint_wrappers=1 \
  "path/to/video.mp4"
```

Generate schedule slots:

```bash
"Youtube/Input/4. Resources/7. publishing_resources/venv/bin/python3" \
  "Youtube/Input/4. Resources/7. publishing_resources/schedule_slots.py" 1
```

Delete a scheduled test video when Daniel asks:

```bash
"Youtube/Input/4. Resources/7. publishing_resources/venv/bin/python3" \
  "Youtube/Input/4. Resources/7. publishing_resources/delete_videos.py" VIDEO_ID
```

## Credentials And Secrets

Project API keys live in:

```text
/Users/danieldanut/.claude/.env
```

Publishing OAuth files live in:

```text
Youtube/Input/4. Resources/7. publishing_resources/credentials.json
Youtube/Input/4. Resources/7. publishing_resources/token.json
```

Never print, copy, commit, or expose secret values.

## Communication Style For Codex

Daniel wants Codex to feel like an operator, not a verbose explainer.

Use short, direct updates:

- Say what you found.
- Say what you are doing next.
- Ask only the necessary confirmation question.
- For mobile tasks, keep answers especially brief.

When executing publishing workflows, user-facing language should say:

- "ready to post"
- "publish"
- "schedule"
- "posted"

Avoid implementation phrasing like "move the pair" unless Daniel asks how it works.

## Google Workspace Access

Codex currently has Google **Calendar** and **Drive** via the OpenAI-curated plugins (read/limited). Full read+write across **Sheets, Docs, Drive, Calendar, Gmail** is available from the self-hosted `google-workspace` MCP, but it must be added to Codex's own config to use:

```toml
# ~/.codex/config.toml
[mcp_servers.google_workspace]
command = "uvx"
args = ["workspace-mcp", "--single-user", "--tools", "gmail", "drive", "calendar", "docs", "sheets"]
[mcp_servers.google_workspace.env]
GOOGLE_CLIENT_SECRET_PATH = "/Users/danieldanut/.claude/google_workspace_client_secret.json"
USER_GOOGLE_EMAIL = "daniel@ministryflow.co"
OAUTHLIB_INSECURE_TRANSPORT = "1"
```

Works only when Codex runs on Daniel's Mac (local stdio server). Until wired, defer Sheets/Docs edits to Clodella / Claude Code.

## Schedule Skill

Codex can read and update Daniel's Google Calendar via `mcp__claude_ai_Google_Calendar`.

**Skill file:** `Orchestrator/Skills/schedule_skill.md`

Read it when Daniel asks you to check his schedule, book something, or plan around his recording/editing blocks. The skill file has the full weekly structure, all recurring event IDs, safe booking windows, and MCP call patterns.

Do not book during Deep Work (04:00–09:00) or Sleep (19:45–03:45).

---

## Strategy Skill

Daniel's business plan: `Orchestrator/Skills/strategy_skill.md` — goal, funnel, the product (inbound lead-response + booking AI agent), Phase 1/2, how first clients are sourced, and what's still open. Read it before any planning, outreach, offer, or content-direction work. Pairs with the Schedule Skill.

---

## Default Safety Rules

- Do not rename or move files unless the task requires it and the target is clear.
- Do not overwrite thumbnails, metadata, analytics snapshots, or published assets without explicit approval.
- Do not re-upload anything inside `Youtube/Output/7. Publishing/published/`.
- Do not invent metadata silently. If a YAML is missing or wrong, explain it and ask.
- Do not hardcode dates from memory. For relative dates like "next Friday", resolve against the current date and state the exact date and timezone.
- Preserve the current folder structure and existing filename quirks unless Daniel asks to clean them up.

## Current Project State Notes

As of the canonical naming migration:

- Output stages use project folders.
- Episode 1 is `01-transcript-youtube`.
- Episode 2 is `02_codex_mobile`.
- `Youtube/Output/9. Analytics/upload_log.md` is the global upload log, and each row must include `project_id`.

Always verify the current state from the filesystem before acting. This file describes the operating model, not a live status report.
