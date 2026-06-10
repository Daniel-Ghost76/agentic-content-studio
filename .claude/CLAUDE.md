# CLAUDE.md

## Business
YouTube (free value) → Skool community (low-ticket) → AI implementation services

---

## Folder Structure

```text
Youtube/
├── Input/     ← SOPs · Skills · Rules · Resources · Tools (by stage number)
└── Output/    ← content produced (by stage number)
```

**Input** = workflow assets. **Output** = episode content. Nothing gets created outside this structure.

---

## Stage Ownership

| Stage | Name | Executor |
|-------|------|----------|
| 1 | Ideation | Claude |
| 2 | Scripts | Claude |
| 3 | Pre-production Materials | Codex |
| 4 | Editing (4a Prep · 4b Cut Edit · 4c Overlay ID · 4d Grade+Zoom) | Codex + Claude Code |
| 5 | Visuals (5a Overlays · 5b Finish) | Codex |
| 6 | Review | Claude |
| 7 | Publishing | Claude / OpenClaw (Astra) via Telegram |
| 8 | Distribution | Claude |
| 9 | Analytics | Claude |

**Astra** = primary mobile orchestrator (Telegram). **Vera/Hermes** = secondary, passive. **Clodella** = Claude Code routine runner.

---

## Agent Instructions

Before any stage task, read: `Youtube/Input/1. SOPs/{N}. {Stage}/{stage}_sop.md` · skill · rules · resources · tools.
Sub-stages 4a/4b/4c/4d → `4. Editing/`; 5a/5b → `5. Visuals/`. Exactly 9 stage folders in each Input section.
Save: workflow assets → Input/; content outputs → Output/.

---

## Canonical Project Naming

```text
Youtube/Output/{stage}/{project_id}/          ← folder
{project_id}_{purpose_suffix}.{ext}           ← filename
```

Examples: `02_codex_mobile_script.pdf` · `02_codex_mobile_raw.mp4`

**Ep 1 override:** project_id = `01-transcript-youtube` — permanent, never rename.

The Stage 1 ideation PDF sets the project ID. All later stages read and reuse it. On Script Draft 1, create empty folders for the project_id in every Output stage (1–9). Raw camera files may keep original names inside `originals/`; all working copies use the project_id prefix.

---

## Subagents (token-saving delegation)

Rule: delegate doing, keep thinking. Mechanical/API/file-ops → subagent. Creative judgment → main session.

| Subagent | Model | Owns | Wired into |
|----------|-------|------|-----------|
| `researcher` | Sonnet | Stage 1: Perplexity saturation/stats/refs → digest | ideation_sop |
| `editor-mech` | Haiku | Stage 4: transcribe / pack / render approved EDL / grade / gap-compress | cut_edit_sop |
| `publisher` | Haiku | Stage 7: validate pairs+YAML, schedule slot, upload | publishing_sop |
| `analyst` | Haiku | Stage 9: due-check, fetch analytics, rollup | analytics_sop |

Agents run in separate context windows on cheaper models; return short summaries only. `editor-mech` executes only an approved EDL — cut strategy stays in main session.

---

## Orchestrator Personas

These are **not** Claude Code subagents — they are identity/routing guides read manually or via Telegram.

| Persona | File | Platform | Role |
|---------|------|----------|------|
| Astra 🦞 | `Orchestrator/Astra/Astra.md` | Telegram (OpenClaw) | Primary mobile orchestrator |
| Vera | `Orchestrator/Vera/Vera.md` | Passive / secondary | Monitoring |
| Clodella | `Orchestrator/Claudella/Clodella.md` | Claude Code | Routine runner |
| Codex | `Orchestrator/Codex/CODEX.md` | Codex CLI | Stage 3 + 5 production |

---

## Official Plugins (Anthropic)

| Plugin | What it adds |
|--------|-------------|
| `superpowers` 5.1.0 | Planning, debugging, TDD, code-review, git-worktrees, subagent-dev skills |
| `claude-md-management` | `/revise-claude-md` command + `claude-md-improver` skill |
| `code-review` | `/code-review` command with `--ultra` multi-agent mode |
| `code-simplifier` | `code-simplifier` subagent — patched to `sonnet` (re-apply after plugin updates) |
| `skill-creator` | `skill-creator` skill for building new skills |
| `session-report` | `/session-report` command — structured session summary for handoffs |
| `commit-commands` | `/commit`, `/commit-push-pr`, `/clean_gone` git shortcuts |
| `feature-dev` | `code-architect`, `code-explorer`, `code-reviewer` subagents (all `sonnet`) |

---

## Shared Tools (MCP)

- **`google-workspace`** — full read/write Google Workspace as `daniel@ministryflow.co`; local stdio (Mac-only). Pass `user_google_email=daniel@ministryflow.co`. Details: memory `project_google_workspace_mcp`.
- **`playwright`** — browser automation; visible browser, starts logged-out.
---

## Auto-suggest

After task completions, output created, or stage approved — append:

```
---
**Next:** `/command` — one sentence tied to current project context.
```

Do not append after questions, mid-task troubleshooting, or config changes. Full catalog: `.claude/commands/suggest.md`.

---

## API Keys

All keys in `~/.claude/.env` — never hardcode, never store elsewhere.

- `PERPLEXITY_API_KEY` — Stage 1 research
- `ELEVENLABS_API_KEY` — Stage 4 transcription
- `YOUTUBE_DATA_API_KEY` — Stages 7, 8, 9
- `OPENAI_API_KEY` · `ANTHROPIC_API_KEY` · `TELEGRAM_BOT_TOKEN` · `SKOOL_API_KEY`
