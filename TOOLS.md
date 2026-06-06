# TOOLS.md - Local Notes

## Workspace

- **Root path:** `/Users/danieldanut/Desktop/Agentic Workspace`
- **YouTube pipeline:** `Youtube/Input/` (agents, tools, resources) + `Youtube/Output/` (content produced)
- **Visual Production Library:** `Youtube/Input/4. Resources/0. visual_production_library/` — master capsule library for pre-production visuals, overlays, Higgsfield clips, emphasis words, CTA visuals, and thumbnails
- **API keys:** All in `~/.claude/.env` — never hardcode, never ask Daniel inline

## Telegram

- **Daniel's user ID:** `6174417525`
- Both Astra (OpenClaw) and Hermes have Telegram bots configured
- Astra is the primary trigger point; Hermes is secondary fallback

## YouTube Pipeline — Stage Map

| Stage | Name | Executor | Input Path | Output Path |
|-------|------|----------|-----------|-------------|
| 1 | Ideation | Claude | `Input/1. Sub-agents/1. Ideation/1. ideation_sub-agent.md` | `Output/1. Ideation/{project_id}/` |
| 2 | Scripts | Claude | `Input/1. Sub-agents/2. Scripting/2. scripting_sub-agent.md` | `Output/2. Scripts/{project_id}/` |
| 3 | Pre-production Materials | Codex | `Input/1. Sub-agents/3. Pre-production Materials/3. pre-production_materials_sub-agent.md` | `Output/3. Pre-production Materials/{project_id}/` |
| 4 | Editing | Claude | `Input/1. Sub-agents/4. Editing/4. editing_sub-agent.md` | `Output/4. Editing/{project_id}/` |
| 4a | Cut Edit | Claude | `Input/1. Sub-agents/4. Editing/4b. cut_edit_sub-agent.md` | `Output/4. Editing/{project_id}/{project_id}_cut.mp4` |
| 5 | Visuals / Overlays | Codex | `Input/1. Sub-agents/5. Visuals/5. visuals_sub-agent.md` | `Output/5. Visuals/{project_id}/` |
| 5a | Overlay Compositing | Codex | `Input/1. Sub-agents/5. Visuals/5a. overlays_sub-agent.md` | `Output/5. Visuals/{project_id}/{project_id}_overlaid.mp4` |
| 6 | Review | Claude | `Input/1. Sub-agents/6. Review/6. review_sub-agent.md` | `Output/6. Review  /{project_id}/` |
| 7 | Publishing | Claude / Astra (mobile) | `Input/1. Sub-agents/7. Publishing/7. publishing_sub-agent.md` | `Output/7. Publishing/{project_id}/` |
| 8 | Distribution | Claude | `Input/1. Sub-agents/8. Distribution/8. distribution_sub-agent.md` | `Output/8. Distribution/{project_id}/` |
| 9 | Analytics | Claude | `Input/1. Sub-agents/9. Analytics/9. analytics_sub-agent.md` | `Output/9. Analytics/{project_id}/` |

## Project Naming Convention

- Format: `{NN}_{lowercase_slug}` — e.g. `03_next_video`, `04_ai_automation`
- Episode 1 exception: `01-transcript-youtube` (explicit Daniel rename, do not change)
- Project ID is set at Stage 1 (ideation) and used unchanged through all 9 stages
- Artifact filenames: `{project_id}_{purpose_suffix}.{ext}`

## Publish Schedule

- Videos 1–3 in queue: next 3 Fridays at 4:00 PM London time
- Videos 4+: consecutive Tuesdays at 4:00 PM London time
- Videos are **never published immediately** — always scheduled

## Mobile Publishing Rule

- Before answering or acting on "what videos are available to publish/post", "what videos are ready to publish/post", "publish/post/upload a YouTube video", scheduling a YouTube video, or deleting a YouTube test upload, read and execute `Youtube/Input/5. Tools/7. publishing_tools/mobilepublishing.md` first.
- Treat that file as the source of truth for mobile YouTube publishing requests. Do not start by scanning every pipeline file or reading the broader Stage 7 rules unless `mobilepublishing.md` points there or something is missing/blocking.
- This rule applies even if the request sounds like a quick status check. The mobile workflow defines which folders count, how to summarize metadata, how to move files, and the browser/Apple Notes completion steps.
- In Apple Notes/status updates, reference the short video name in quotation marks followed by "YouTube video"; e.g. `"Codex Mobile" YouTube video test 2 passed.`
- After deleting a scheduled YouTube test upload, move the local publish pair back to `Youtube/Output/6. Review  /{project_id}/` so the next test can start from Review.

## Key Scripts

| Script | Location | Purpose |
|--------|----------|---------|
| `validate_publish_pairs.py` | `Input/5. Tools/7. publishing_tools/` | Scan Publishing folder for eligible pairs |
| `validate_yaml.py` | `Input/5. Tools/7. publishing_tools/` | Validate metadata YAML before upload |
| `upload_to_youtube.py` | `Input/4. Resources/7. publishing_resources/` | Upload + schedule to YouTube |
| `validate_filler_words.py` | `Input/5. Tools/4. editing_tools/` | Pre-scan transcript before cut edit |
| `check_analytics_due.py` | `Input/5. Tools/9. analytics_tools/` | Check which episodes have Day 7/30 windows open |

## API Keys (all in `~/.claude/.env`)

- `ELEVENLABS_API_KEY` — ElevenLabs Scribe transcription (Stage 4)
- `YOUTUBE_DATA_API_KEY` — YouTube Data API v3 (Stages 7, 8, 9)
- `OPENAI_API_KEY` — OpenAI / DALL-E (slide generation)
- `ANTHROPIC_API_KEY` — Anthropic Claude API
- `TELEGRAM_BOT_TOKEN` — YouTube notification bot
- `SKOOL_API_KEY` — Skool community

## Pipeline Status

When Daniel asks where things stand, what's in production, what needs doing, or anything about the pipeline — run this immediately:

```bash
python3 "/Users/danieldanut/Desktop/Agentic Workspace/Youtube/Input/5. Tools/pipeline_status.py"
```

That script scans the Output folders and returns a plain-English summary of every video currently in production and what's blocking each one. Send the output back to Daniel as-is.

To push directly to Telegram instead of replying in chat, add `--send`. The cron job runs this automatically every morning at 6:00 AM London time.

### OpenClaw Cron

- Job: `Daily YouTube pipeline status to Telegram`
- Cron ID: `3ea14ab3-8ffd-4d22-886d-942716015a21`
- Schedule: daily at 6:00 AM Europe/London
- Script: `python3 "/Users/danieldanut/Agentic Workspace/Youtube/Input/5. Tools/pipeline_status.py"`
- Delivery: OpenClaw/Astra sends output to Daniel on Telegram target `telegram:6174417525`
- Important: use Astra/OpenClaw cron and bot, not Claude's cron/bot.

## Claude Code Slash Commands

Available in `.claude/.commands/` — trigger the corresponding sub-agent:
`/ideate` · `/script` · `/production-materials` · `/edit` · `/cut-edit` · `/visuals` · `/overlay` · `/review` · `/publish` · `/distribute` · `/analytics` · `/cleanup`
