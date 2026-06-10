# Workspace Mega Audit & Quality Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Audit every skill, agent, plugin, and orchestrator file in the workspace; fix broken wiring, correct model assignments, remove clutter, and document the canonical state so the workspace is clean, consistent, and ready for new capabilities.

**Architecture:** Three distinct layers exist — (1) `.agents/skills/` third-party skills + `.claude/skills/` symlinks that expose them to the Skill tool; (2) `.claude/agents/` Claude Code subagent definitions with model assignments; (3) `.claude/plugins/` Anthropic official plugins with agents/commands/skills. All three must be consistent with each other and with CLAUDE.md.

**Tech Stack:** Claude Code CLI, YAML/Markdown frontmatter, `ln -s` symlinks, `claude plugin` CLI commands

---

## Audit Summary — What Was Found

| # | Issue | Severity | Layer |
|---|---|---|---|
| 1 | 4 Higgsfield skills installed but not linked → not accessible via Skill tool | HIGH | `.agents/skills/` |
| 2 | `code-simplifier` agent assigned `model: opus` — should be `sonnet` | HIGH | Official plugin |
| 3 | `swift-lsp` installed but workspace has zero Swift code — dead weight | LOW | Official plugin |
| 4 | Orchestrator personas (Astra/Vera/Clodella/Codex) not cross-referenced in CLAUDE.md agent table | MEDIUM | Docs |
| 5 | CLAUDE.md subagent table lists no model for `researcher` (it is `sonnet`) | LOW | CLAUDE.md |
| 6 | `session-report` and `commit-commands` plugins available but not installed — both useful | INFO | Marketplace |
| 7 | `feature-dev` plugin available — adds code-architect + code-explorer + code-reviewer agents | INFO | Marketplace |
| 8 | Large git backlog of modified files never committed | MEDIUM | Git |

**What is correct / no changes needed:**
- `researcher` → `sonnet` ✓ appropriate for live web research
- `editor-mech`, `publisher`, `analyst` → `haiku` ✓ mechanical/API tasks
- All four `.claude/agents/` descriptions are accurate
- `.claude/skills/` symlinks work for: `find-skills`, `hyperframes`, `hyperframes-cli`, `skill-scout`
- Skill metadata (names, descriptions, versions) on Higgsfield and HyperFrames skills are correct
- `superpowers` 5.1.0, `claude-md-management`, `code-review`, `skill-creator` plugins all wired correctly

---

## Task 1: Fix Higgsfield Skill Links

**Problem:** `higgsfield-generate`, `higgsfield-marketplace-cards`, `higgsfield-product-photoshoot`, `higgsfield-soul-id` are in `.agents/skills/` but have no `.claude/skills/` symlink. The Skill tool cannot find them.

**Files:**
- Create: `.claude/skills/higgsfield-generate` → `../../.agents/skills/higgsfield-generate`
- Create: `.claude/skills/higgsfield-marketplace-cards` → `../../.agents/skills/higgsfield-marketplace-cards`
- Create: `.claude/skills/higgsfield-product-photoshoot` → `../../.agents/skills/higgsfield-product-photoshoot`
- Create: `.claude/skills/higgsfield-soul-id` → `../../.agents/skills/higgsfield-soul-id`

- [ ] **Step 1: Confirm skills are missing from `.claude/skills/`**

```bash
ls /Users/danieldanut/Agentic\ Workspace/.claude/skills/
```
Expected: `find-skills  hyperframes  hyperframes-cli  skill-scout` — no higgsfield entries.

- [ ] **Step 2: Create the four symlinks**

```bash
cd "/Users/danieldanut/Agentic Workspace/.claude/skills"
ln -s ../../.agents/skills/higgsfield-generate higgsfield-generate
ln -s ../../.agents/skills/higgsfield-marketplace-cards higgsfield-marketplace-cards
ln -s ../../.agents/skills/higgsfield-product-photoshoot higgsfield-product-photoshoot
ln -s ../../.agents/skills/higgsfield-soul-id higgsfield-soul-id
```

- [ ] **Step 3: Verify symlinks resolve correctly**

```bash
ls -la "/Users/danieldanut/Agentic Workspace/.claude/skills/"
```
Expected: 8 entries, 4 of them pointing to `../../.agents/skills/higgsfield-*`

- [ ] **Step 4: Spot-check one skill is loadable**

```bash
head -5 "/Users/danieldanut/Agentic Workspace/.claude/skills/higgsfield-generate/SKILL.md"
```
Expected: frontmatter with `name: higgsfield-generate`

- [ ] **Step 5: Commit**

```bash
cd "/Users/danieldanut/Agentic Workspace"
git add .claude/skills/
git commit -m "fix: add missing .claude/skills symlinks for 4 Higgsfield skills

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 2: Fix code-simplifier Model Assignment

**Problem:** The `code-simplifier` agent (official Anthropic plugin) is assigned `model: opus`. For a deterministic code-cleanup task, this wastes tokens on the most expensive model. Sonnet handles code formatting/simplification with full quality.

**Files:**
- Modify: `/Users/danieldanut/.claude/plugins/cache/claude-plugins-official/code-simplifier/1.0.0/agents/code-simplifier.md`

**Note:** This file is in the plugin cache and may be overwritten on `claude plugin update`. Re-apply after any update to `code-simplifier`.

- [ ] **Step 1: Read current model line**

```bash
grep "^model:" "/Users/danieldanut/.claude/plugins/cache/claude-plugins-official/code-simplifier/1.0.0/agents/code-simplifier.md"
```
Expected: `model: opus`

- [ ] **Step 2: Change model from opus to sonnet**

Edit the file — change the frontmatter line:
```
model: opus
```
to:
```
model: sonnet
```

- [ ] **Step 3: Verify change**

```bash
grep "^model:" "/Users/danieldanut/.claude/plugins/cache/claude-plugins-official/code-simplifier/1.0.0/agents/code-simplifier.md"
```
Expected: `model: sonnet`

- [ ] **Step 4: Note in CLAUDE.md** — add a comment to the Subagents table that `code-simplifier` is patched to `sonnet` and needs reapplying after plugin updates.

---

## Task 3: Uninstall swift-lsp

**Problem:** `swift-lsp` v1.0.0 is installed. This workspace contains no Swift code. It adds noise to plugin loading with zero benefit.

- [ ] **Step 1: Confirm swift-lsp has nothing useful**

```bash
ls "/Users/danieldanut/.claude/plugins/cache/claude-plugins-official/swift-lsp/1.0.0/"
cat "/Users/danieldanut/.claude/plugins/cache/claude-plugins-official/swift-lsp/1.0.0/README.md"
```
Expected: Only README, no agents or commands relevant to this workspace.

- [ ] **Step 2: Uninstall via CLI**

```bash
claude plugin uninstall swift-lsp
```
Expected: Confirmation that plugin is removed.

- [ ] **Step 3: Verify removed**

```bash
ls "/Users/danieldanut/.claude/plugins/cache/claude-plugins-official/" 2>/dev/null
```
Expected: `swift-lsp` directory is gone.

---

## Task 4: Evaluate and Install session-report + commit-commands

**Purpose:** Both are available in the official marketplace and directly useful:
- `session-report` — auto-generates a structured summary at session end (what was done, decisions made, files changed). Helps Clodella hand off context.
- `commit-commands` — adds `/commit`, `/commit-push-pr`, `/clean_gone` shortcuts. Tightens the git workflow.

- [ ] **Step 1: Read session-report README**

```bash
cat "/Users/danieldanut/.claude/plugins/marketplaces/claude-plugins-official/plugins/session-report/README.md" 2>/dev/null || echo "No README found"
```

- [ ] **Step 2: Read commit-commands README**

```bash
cat "/Users/danieldanut/.claude/plugins/marketplaces/claude-plugins-official/plugins/commit-commands/README.md"
```

- [ ] **Step 3: Decision — ask Daniel** before installing. Present what each does and get a yes/no per plugin.

- [ ] **Step 4 (if approved): Install**

```bash
claude plugin install session-report
claude plugin install commit-commands
```

- [ ] **Step 5: Verify loaded**

```bash
ls "/Users/danieldanut/.claude/plugins/cache/claude-plugins-official/"
```
Expected: `session-report` and/or `commit-commands` directories present.

---

## Task 5: Evaluate feature-dev Plugin

**Purpose:** `feature-dev` adds three subagents — `code-architect` (designs solutions), `code-explorer` (finds relevant code), `code-reviewer` (reviews PRs). These could reinforce the skill-scout and code-review workflows already installed.

- [ ] **Step 1: Read feature-dev agents**

```bash
for f in "/Users/danieldanut/.claude/plugins/marketplaces/claude-plugins-official/plugins/feature-dev/agents/"*.md; do
  echo "=== $f ===" && head -8 "$f"
done
```

- [ ] **Step 2: Check for model assignments**

```bash
grep "^model:" "/Users/danieldanut/.claude/plugins/marketplaces/claude-plugins-official/plugins/feature-dev/agents/"*.md
```

- [ ] **Step 3: Decision — ask Daniel.** The existing `code-review` plugin already handles review. `code-architect` and `code-explorer` are new. Present the overlap and get go/no-go.

- [ ] **Step 4 (if approved): Install**

```bash
claude plugin install feature-dev
```

---

## Task 6: Update CLAUDE.md Subagent Table

**Problem:** The CLAUDE.md subagent table does not show models, and the Orchestrator personas (Astra/Vera/Clodella/Codex) are not distinguished from Claude Code subagents. This makes the map incomplete for any agent reading the file cold.

**Files:**
- Modify: `/Users/danieldanut/Agentic Workspace/.claude/CLAUDE.md`

- [ ] **Step 1: Read current subagents table in CLAUDE.md**

Read lines around `## Subagents` section.

- [ ] **Step 2: Add model column to the subagents table**

Expand the table to include the `Model` column with actual model IDs:

| Subagent | Model | Owns | Wired into |
|---|---|---|---|
| `researcher` | `claude-sonnet-4-6` | Stage 1: Perplexity saturation/stats/refs → digest | ideation_sop |
| `editor-mech` | `claude-haiku-4-5` | Stage 4: transcribe / pack / render approved EDL / grade / gap-compress | cut_edit_sop |
| `publisher` | `claude-haiku-4-5` | Stage 7: validate pairs+YAML, schedule slot, upload | publishing_sop |
| `analyst` | `claude-haiku-4-5` | Stage 9: due-check, fetch analytics, rollup | analytics_sop |

- [ ] **Step 3: Add an Orchestrator Personas section** beneath Subagents to distinguish the personas from subagents:

```markdown
## Orchestrator Personas

These are *not* Claude Code subagents — they are identity/routing guides read manually or via Telegram.

| Persona | File | Platform | Role |
|---|---|---|---|
| Astra 🦞 | `Orchestrator/Astra/Astra.md` | Telegram (OpenClaw) | Primary mobile orchestrator |
| Vera | `Orchestrator/Vera/Vera.md` | Passive / secondary | Monitoring |
| Clodella | `Orchestrator/Claudella/Clodella.md` | Claude Code | Routine runner |
| Codex | `Orchestrator/Codex/CODEX.md` | Codex CLI | Stage 3/5 production |
```

- [ ] **Step 4: Add Official Plugins section** listing installed Anthropic plugins and their purpose:

```markdown
## Official Plugins (Anthropic)

| Plugin | Version | What it adds |
|---|---|---|
| `superpowers` | 5.1.0 | Planning, debugging, TDD, code-review, git-worktrees, subagent-dev skills |
| `claude-md-management` | 1.0.0 | `/revise-claude-md` command + `claude-md-improver` skill |
| `code-review` | latest | `/code-review` command with `--ultra` multi-agent mode |
| `code-simplifier` | 1.0.0 | `code-simplifier` subagent (patched: `sonnet`, not `opus`) |
| `skill-creator` | latest | `skill-creator` skill for building new skills |
```

- [ ] **Step 5: Commit CLAUDE.md update**

```bash
cd "/Users/danieldanut/Agentic Workspace"
git add .claude/CLAUDE.md
git commit -m "docs: add model column, orchestrator personas, and official plugins table to CLAUDE.md

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 7: Git Housekeeping

**Problem:** The git status shows ~20+ modified/untracked files accumulated across several sessions, including SOP updates, new agent files, deleted output files, new skills, and session artefacts. Everything should be committed or gitignored.

**Files:**
- Modify: `.gitignore`
- Stage all clean workspace changes

- [ ] **Step 1: Full git status**

```bash
cd "/Users/danieldanut/Agentic Workspace"
git status
```

- [ ] **Step 2: Check .gitignore for Playwright MCP logs and session artefacts**

```bash
cat .gitignore | grep -E "playwright|session"
```
If missing, add:
```
.playwright-mcp/
.claude/session_handoff.md
.claude/worktrees/
```

- [ ] **Step 3: Stage all intentional changes**

Stage files in logical groups. First the workflow assets (SOPs, skills, orchestrator):
```bash
git add \
  .claude/CLAUDE.md \
  .claude/agents/ \
  .claude/commands/ \
  Orchestrator/ \
  "Youtube/Input/" \
  TOOLS.md \
  skills-lock.json
```

- [ ] **Step 4: Review staged diff before committing**

```bash
git diff --cached --stat
```
Verify nothing unexpected (no `.env`, no personal data, no huge binaries).

- [ ] **Step 5: Commit staged changes**

```bash
git commit -m "chore: sync workspace — SOP updates, agent definitions, orchestrator docs, new skills

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

- [ ] **Step 6: Handle deleted output files**

The deleted `Youtube/Output/4. Editing/01-transcript-youtube/` files should be staged:
```bash
git add -u "Youtube/Output/"
git commit -m "chore: remove superseded stage-4 output artefacts for 01-transcript-youtube

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

- [ ] **Step 7: Verify clean working tree**

```bash
git status
```
Expected: Nothing to commit, working tree clean (or only intentionally untracked files).

---

## Self-Review

**Spec coverage check:**
- Task 1 → fixes Higgsfield skill wiring ✓
- Task 2 → fixes code-simplifier model assignment ✓
- Task 3 → removes irrelevant swift-lsp ✓
- Task 4–5 → evaluates and installs useful plugins ✓
- Task 6 → updates CLAUDE.md with complete agent map ✓
- Task 7 → cleans git backlog ✓
- "Right model assigned to each skill" → addressed in Tasks 2 + 6 ✓
- "Correctly labeled" → addressed in Tasks 1 + 6 ✓
- "Not over-cluttered" → addressed in Tasks 3 + 7 ✓
- "Recently installed Anthropic plugins" → identified and documented in summary + Task 6 ✓

**No placeholders found.** All steps have exact commands.

**Type consistency:** No code types involved — all shell commands and markdown edits. Consistent throughout.
