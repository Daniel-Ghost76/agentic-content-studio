# CLAUDE.md

## The Business

YouTube (free value) -> Skool community (low-ticket) -> AI implementation services

---

## Folder Structure

```text
Orchestrator/
├── Astra/
├── Claudella/
├── Codex/
└── Vera/

Youtube/
├── Input/              ← agents, SOPs, tools, resources needed TO DO the work
│   ├── 1. Sub-agents/
│   ├── 2. Skills/
│   ├── 3. Rules/
│   ├── 4. Resources/
│   │   ├── 1. ideation_resources/
│   │   ├── 2. scripting_resources/
│   │   ├── 3. pre-production_materials_resources/
│   │   ├── 4. editing_resources/
│   │   ├── 5. visuals_resources/
│   │   ├── 6. review_resources/
│   │   ├── 7. publishing_resources/
│   │   ├── 8. distribution_resources/
│   │   └── 9. analytics_resources/
│   └── 5. Tools/
│       ├── 1. ideation_tools/
│       ├── 2. scripting_tools/
│       ├── 3. pre-production_materials_tools/
│       ├── 4. editing_tools/
│       ├── 5. visuals_tools/
│       ├── 6. review_tools/
│       ├── 7. publishing_tools/
│       ├── 8. distribution_tools/
│       └── 9. analytics_tools/
└── Output/             ← content produced by the system
    ├── 1. Ideation/
    ├── 2. Scripts/
    ├── 3. Pre-production Materials/
    ├── 4. Editing/
    ├── 5. Visuals/
    ├── 6. Review  /
    ├── 7. Publishing/
    ├── 8. Distribution/
    └── 9. Analytics/
```

**Input** is where agents save MD files, tools, credentials, and anything needed to perform a workflow.
**Output** is where the content produced by those workflows gets saved.

---

## Stage Ownership

| Stage | Name | Executor |
|-------|------|----------|
| 1 | Ideation | Claude |
| 2 | Scripts | Claude |
| 3 | Pre-production Materials | Codex |
| 4 | Editing (4a Prep · 4b Cut Edit · 4c Overlay Identifier · 4d Grade+Zoom) | Codex + Claude Code |
| 5 | Visuals / Overlays (5a Overlays · 5b Finish) | Codex |
| 6 | Review | Claude |
| 7 | Publishing | Claude by default; OpenClaw (Astra) orchestrates from mobile via Telegram |
| 8 | Distribution | Claude |
| 9 | Analytics | Claude |

**OpenClaw (Astra)** is the primary mobile orchestrator. Daniel triggers stages by messaging Astra on Telegram. **Hermes (Vera)** is the secondary assistant — passive, Telegram-triggered only, no background work. **Clodella** is the Claude Code routine runner — executes specific tasks and task-completion updates from within the workspace.

---

## Canonical Project Naming

Every YouTube video has one permanent project ID. That ID is carried through every Output stage.

Project folders:

```text
Youtube/Output/{stage}/{project_id}/
```

Artifact filenames:

```text
{project_id}_{purpose_suffix}.{ext}
```

Examples:

- `02_codex_mobile`
- `02_codex_mobile_idea.pdf`
- `02_codex_mobile_script.pdf`
- `02_codex_mobile_visuals_brief.md`
- `02_codex_mobile_raw.mp4`
- `02_codex_mobile_review.mp4`
- `02_codex_mobile_publish.mp4`
- `02_codex_mobile_analytics_d07.md`

Current Episode 1 override: Daniel explicitly renamed the first project to `01-transcript-youtube`. Use that exact project ID for Episode 1. Do not rename it back to any previous Day 1 ID.

The Stage 1 ideation PDF establishes the project ID. Later stages must read and reuse the upstream project ID instead of inventing a new folder or display name. Raw imported camera exports may keep original filenames only inside an `originals/` subfolder; normalized working copies must use the project ID prefix.

Once an idea is accepted and Script Draft 1 has been created, the scripting agent must create empty project folders for that `project_id` in every Output stage. This gives the episode a complete lane from ideation through analytics even before later assets exist.

Required folder set:

```text
Youtube/Output/1. Ideation/{project_id}/
Youtube/Output/2. Scripts/{project_id}/
Youtube/Output/3. Pre-production Materials/{project_id}/
Youtube/Output/4. Editing/{project_id}/
Youtube/Output/5. Visuals/{project_id}/
Youtube/Output/6. Review  /{project_id}/
Youtube/Output/7. Publishing/{project_id}/
Youtube/Output/8. Distribution/{project_id}/
Youtube/Output/9. Analytics/{project_id}/
```

---

## Agent Instructions

**Before performing any task, read your stage's Input files:**
- Sub-agent: `Youtube/Input/1. Sub-agents/{N}. {Stage}/{stage}_sub-agent.md`
- Skill: `Youtube/Input/2. Skills/{N}. {Stage}/{stage}_skill.md` (folder may contain multiple skill files — read all)
- Rules: `Youtube/Input/3. Rules/{N}. {Stage}/{stage}_rules.md`
- Resources: `Youtube/Input/4. Resources/{N}. {stage}_resources/`
- Tools: `Youtube/Input/5. Tools/{N}. {stage}_tools/`

Sub-stages 4a/4b/4c/4d live inside `4. Editing/`; sub-stages 5a/5b live inside `5. Visuals/`. There are exactly 9 stage folders in Sub-agents, Skills, and Rules.

**Save files to the right place:**
- Workflow SOPs, agent MD files, tools -> `Youtube/Input/` in the relevant stage folder
- Content outputs -> `Youtube/Output/` in the relevant stage folder
- Nothing gets created outside the existing folder structure

---

## Ideation Stage

Approved idea PDFs go to:

```text
Youtube/Output/1. Ideation/{project_id}/{project_id}_idea.pdf
```

The ideation agent creates the permanent project ID from the ordered idea number and title. That ID is passed to every later stage.

Brief format: voice_reference pointer · Core Idea · Hook Type · The One Thing · Target Viewer · Value Proof · Build/Demo Steps · Personal Angle `[DANIEL TO FILL]` · Vulnerability Moment `[DANIEL TO FILL]` · Analogy Idea · CTA Direction · Constraints

---

## Pre-production Materials Stage

**Stage 3 — Pre-production Materials:** Input = Visuals Brief MD from scripting agent. Codex builds slides, diagrams, and presentation assets before Daniel records. Output -> `Youtube/Output/3. Pre-production Materials/{project_id}/`

---

## Editing And Visuals Stages

**Stage 4 — Editing:** Claude runs four sequential sub-agents to take raw footage to a graded, zoomed, overlay-mapped cut. Output -> `Youtube/Output/4. Editing/{project_id}/`

**Stage 4a — Prep:** Claude ingests `originals/`, normalizes footage to spec, syncs multi-source (face cam + screen recording), enhances audio with DeepFilterNet. Outputs: `normalized/`, `audio/`, `manifest.json`, `sync.json`.

**Stage 4b — Cut Edit:** Claude transcribes (ElevenLabs Scribe), proposes cut strategy (Daniel approves), removes filler words/silences/bad takes, renders `{project_id}_cut.mp4`.

**Stage 4c — Overlay Identifier:** Claude reads the transcript and cut video once, maps all visual events as stubs — captions (glass panel overlays, 10–15% of words), zoom keyframes, HyperFrames motion graphics, Higgsfield full-screen clips, additional materials. Daniel approves the overlay map before Stage 5 builds anything.

**Stage 4d — Grade + Zoom:** Claude applies color grade and bakes zoom keyframes into the footage in a single render pass. Outputs `{project_id}_cut_final.mp4` — the base video Agent 5 composites onto.

**Stage 5 — Visuals / Overlays:** Codex runs two sequential sub-agents to build all overlays and finish the video. Output -> `Youtube/Output/5. Visuals/{project_id}/`

**Stage 5a — Overlays:** Codex reads the overlay map from 4c, cleans up the screen recording, builds all overlay slots in parallel (HyperFrames for captions/motion graphics, Higgsfield for full-screen clips), and composites everything onto `cut_final.mp4`.

**Stage 5b — Finish:** Codex adds branded intro/outro (cached, rendered once per brand version), optional background music (ducks under speech automatically), and runs automatic QC verification. Outputs `{project_id}_final.mp4` + `{project_id}_qc_report.md` → Stage 6.

---

## API Keys

All API keys live in `~/.claude/.env` (`/Users/danieldanut/.claude/.env`).

**Any agent that needs an API key must read it from that file — never hardcode keys, never store them anywhere else.**

Current keys registered:
- `ELEVENLABS_API_KEY` — Scribe transcription (Stage 4 editing)
- `YOUTUBE_DATA_API_KEY` — YouTube Data API v3 (Stages 7, 8, 9)
- `OPENAI_API_KEY` — OpenAI / ChatGPT
- `ANTHROPIC_API_KEY` — Anthropic Claude API
- `TELEGRAM_BOT_TOKEN` — YouTube notification bot
- `SKOOL_API_KEY` — Skool community

---

## Voice Reference

`Youtube/Input/4. Resources/2. scripting_resources/voice_reference/nate_herk_voice_reference.md` — style analysis of Nate Herk's channel. Use as pattern reference only; apply Daniel's own voice.

Key sections: 1 (hooks) · 5 (credential drops) · 6 (transitions) · 8 (framework) · 9 (analogies) · 11 (vocabulary) · 13 (CTA) · 16 (pacing) · 17 (specificity)
