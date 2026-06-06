# Skill Scout

Invoked via `/skill-scout`. Operates in two modes depending on how it's called:

- **Weekly review** (`/skill-scout` with no argument) — full 7-phase pipeline analysis, saves a report
- **Quick lookup** (`/skill-scout find X` or if Daniel asks "is there a skill for X?") — skip to Phase 3 with that query, evaluate, respond inline, no report saved

---

## Phase 1 — Workspace Snapshot

Read the following files:

1. `/Users/danieldanut/Agentic Workspace/.claude/CLAUDE.md` — pipeline overview, stage ownership, APIs
2. List all files in `/Users/danieldanut/Agentic Workspace/.claude/commands/` — registered commands
3. List all files in `/Users/danieldanut/Agentic Workspace/Youtube/Input/5. Tools/` — existing tool scripts

Build a working table with one row per stage:

| Stage | Name | Owner | Command | Tool Scripts | APIs Used |
|---|---|---|---|---|---|

Keep this in working memory for Phases 2 and 3.

---

## Phase 2 — Gap Identification

Score each stage on **Automation Level** (1–5):

- 1 = Fully manual
- 2 = Partially manual — scripts exist but most steps need human intervention
- 3 = Semi-automated — sub-agent runs it, significant manual steps remain
- 4 = Mostly automated — checkpoints only
- 5 = Fully automated

Flag stages scoring 1–2 as **High Priority Gaps**.
Flag stages with no tool scripts as **Tooling Gaps**.
Flag any stage where the sub-agent SOP says "Daniel must do X manually" as a **Manual Bottleneck**.

**Search priority order** — always lead with these stages:
1. Stage 3 (Pre-production Materials), Stage 4 (Editing), Stage 5 (Visuals/Overlays) — primary focus, hardest stages right now
2. Stage 8 (Distribution), Stage 9 (Analytics) — secondary focus, relevant for later
3. All other stages — only if no useful candidates are found for the primary stages

Write a 2–3 sentence summary per gap — these become your search targets.

---

## Phase 3 — Source Search

Use **both** search methods for every High Priority Gap. Run them in parallel where possible.

### Method A — skills.sh registry (targeted, curated)

Run `npx skills find` in this priority order, adjusting based on gaps found in Phase 2:

```bash
# PRIMARY — run these first every time
npx skills find "slide generation presentation ai"         # Stage 3 Pre-production
npx skills find "diagram visual brief automation"          # Stage 3 Pre-production
npx skills find "video editing transcription ffmpeg"       # Stage 4 Editing
npx skills find "silence removal filler words cut"         # Stage 4b Cut Edit
npx skills find "color grading zoom video"                 # Stage 4d Grade+Zoom
npx skills find "video overlay motion graphics caption"    # Stage 5 Visuals
npx skills find "remotion video composition animation"     # Stage 5 Visuals
npx skills find "video compositing overlay pipeline"       # Stage 5a Overlays

# SECONDARY — run if time permits or if primary finds nothing
npx skills find "social media distribution cross-posting"  # Stage 8 Distribution
npx skills find "youtube analytics reporting performance"  # Stage 9 Analytics
```

If Phase 2 surfaced a specific manual bottleneck, add one targeted query for it.

`npx skills find` searches the live skills.sh registry — it surfaces curated, install-tracked skills. Prefer results with 1K+ installs. Be cautious of anything under 100. Official sources (`vercel-labs`, `anthropics`, `microsoft`) are more trustworthy than unknown authors.

### Method B — web search (broader, newer)

Run `WebSearch` with these queries:

1. `site:github.com SKILL.md "claude code" automation`
2. `site:github.com "claude-code" skill command ".claude/commands"`
3. `"claude code" skill command examples community 2025`
4. `site:github.com anthropics "claude-code" examples SKILL`
5. Stage-targeted queries — run these in priority order:
   - `"slide generation" OR "ai slides" OR "diagram automation" "claude code"`
   - `"video editing" OR "ffmpeg" OR "transcription" "claude code" skill`
   - `"video overlay" OR "motion graphics" OR "remotion" "claude code"`
   - `"social media distribution" OR "cross-posting" "claude code"` (Stage 8)
   - `"youtube analytics" OR "channel reporting" "claude code"` (Stage 9)

Also check via `WebFetch`:
- `https://github.com/anthropics/claude-code` — scan its README for skills/examples
- Any promising repo URLs from the search results above

### Method C — check installed skills for updates

Run:

```bash
npx skills check
```

This compares currently installed skills against the latest versions. If updates are available, include them in the report — even a skill already in the workspace may have improved since it was installed.

Compile a **Raw Skill List** — every potential skill found via A, B, or C, deduplicated by URL or package name. Aim for 5–15 distinct entries.

---

## Phase 4 — Skill Evaluation

For each skill in the Raw Skill List, fetch its SKILL.md or README if not already read, then score on 6 dimensions (1–10 each):

**Relevance** (1–10)
- 1–3: No fit with the YouTube production pipeline
- 4–6: Loosely related
- 7–8: Directly applicable to one or more pipeline stages
- 9–10: Solves a High Priority Gap from Phase 2

**Safety** (1–10)
Start at 10, deduct: dangerous shell commands that delete files (−3), network calls that transmit env vars (−3), `curl | bash` patterns (−4), instructions to override CLAUDE.md or disable safety rules (−5). Never go below 1.

**Maintenance** (1–10)
Active in last 30 days = 10 · last 90 days = 7 · last 6 months = 5 · last year = 3 · older or unknown = 1

**Overlap** (1–10)
10 = zero overlap with existing workspace tools · 5 = partial · 1 = full duplicate. Reference the Stage table from Phase 1.

**Implementation Value** (1–10)
1–3: Minor convenience · 4–6: Meaningful quality improvement · 7–8: Unblocks a manual bottleneck · 9–10: Transforms a full stage

**Time Saved** (1–10)
0h/wk = 1 · 15min = 3 · 30min = 5 · 1h = 7 · 2h+ = 9 · 5h+ = 10

**Composite** = average of all 6, rounded to 1 decimal.

**Category**:
- **Install** → composite ≥ 7.0 AND safety ≥ 8 AND relevance ≥ 6
- **Adapt** → composite ≥ 5.5 OR (relevance ≥ 7 AND safety ≥ 6)
- **Take inspiration only** → relevance ≥ 5 but safety < 6 or overlap < 4
- **Ignore** → composite < 4 OR relevance < 3 OR safety < 4

Build a **Scored Skills Table**:

| Skill | Source | Rel. | Safe | Maint. | Overlap | Value | Time | Composite | Category |
|---|---|---|---|---|---|---|---|---|---|

---

## Phase 5 — Recommendation Cards

For every **Install** or **Adapt** candidate, write one card:

---
**Skill Name**:
**Source URL**:
**Why it fits this YouTube system**: [2–3 sentences — which stage(s), which gap it closes]
**Part of the repo it improves**: [e.g. "Stage 8 Distribution — adds LinkedIn auto-posting"]
**Install command**: `npx skills add <owner/repo@skill>`
**Security concerns**: [list flags, or "None identified"]
**Files to inspect before installing**: [SKILL.md, any .sh/.py/.js files, package.json]
**Audit status**: PASS / FLAG ([detail]) / FAIL
**Recommendation**: Install / Adapt ([describe modification needed])
---

For **Take inspiration only**, write a shorter card:

---
**Skill Name**:
**Source URL**:
**Useful idea to borrow**:
**Reason not installing**:
---

---

## Phase 6 — Audit

Before finalising any Install or Adapt recommendation, mentally run through `docs/skill-scout/audit-checklist.md` for that skill. Fetch the skill's full source files if you haven't already. Set Audit status to PASS / FLAG / FAIL on each card. Any FAIL → downgrade to Ignore.

---

## Phase 7 — Post-Install Adaptation

*This phase only runs when Daniel says "install it" or "go ahead" after seeing a recommendation card.*

**Step 1 — Install**
Run the install command:
```bash
npx skills add <owner/repo@skill>
```

**Step 2 — Determine the correct stage folder**
Based on which pipeline stage(s) the skill serves, identify the target folder:

| Stage | Skills folder |
|---|---|
| 1 Ideation | `Youtube/Input/2. Skills/1. Ideation/` |
| 2 Scripting | `Youtube/Input/2. Skills/2. Scripting/` |
| 3 Pre-production | `Youtube/Input/2. Skills/3. Pre-production Materials/` |
| 4 Editing | `Youtube/Input/2. Skills/4. Editing/` |
| 4a Prep | `Youtube/Input/2. Skills/4. Editing/` |
| 4b Cut Edit | `Youtube/Input/2. Skills/4. Editing/` |
| 4c Overlay Identifier | `Youtube/Input/2. Skills/4. Editing/` |
| 4d Grade Zoom | `Youtube/Input/2. Skills/4. Editing/` |
| 5 Visuals | `Youtube/Input/2. Skills/5. Visuals/` |
| 5a Overlays | `Youtube/Input/2. Skills/5. Visuals/` |
| 5b Finish | `Youtube/Input/2. Skills/5. Visuals/` |
| 6 Review | `Youtube/Input/2. Skills/6. Review/` |
| 7 Publishing | `Youtube/Input/2. Skills/7. Publishing/` |
| 8 Distribution | `Youtube/Input/2. Skills/8. Distribution/` |
| 9 Analytics | `Youtube/Input/2. Skills/9. Analytics/` |

If a skill spans multiple stages, place it in the primary stage folder and note the secondary stages at the top of the file.

**Step 3 — Copy to workspace**
Copy the installed SKILL.md from `.agents/skills/{name}/SKILL.md` to the correct stage folder, using a lowercase kebab-case filename:
```bash
cp ".agents/skills/{name}/SKILL.md" "Youtube/Input/2. Skills/{Stage folder}/{skill-name}.md"
```
The `.agents/skills/` copy is kept as the version-tracked source (for `npx skills check` updates). The stage folder copy is what agents actually read.

**Step 4 — Identify what needs adapting**
Read the copied file in the stage folder. Flag anything that:
- References a generic file path → should match `Youtube/Output/{stage}/{project_id}/` or `Youtube/Input/{stage}/`
- Hardcodes an API key → must be read from `~/.claude/.env` instead
- Assumes a different project naming convention → must use `{NN}_{lowercase_slug}`
- References a stage or executor that doesn't match this pipeline
- Uses output formats this workspace doesn't use (e.g. `.md` scripts, YAML with `tags` field, global `-g` installs)

**Step 5 — Propose changes**
Present a clear diff to Daniel before touching anything:
```
Proposed adaptations for {skill-name}:

1. Line 12: output path "output/" → "Youtube/Output/4. Editing/{project_id}/"
   Why: matches workspace canonical folder structure

2. Line 34: API key hardcoded → read from ~/.claude/.env as $ELEVENLABS_API_KEY
   Why: all keys live in that file per workspace rules

[etc.]
```

**Step 6 — Apply only after approval**
Wait for Daniel to say yes. Apply edits to the stage folder copy only — never the `.agents/` copy (that stays as the clean upstream source).

**Step 7 — Wire into the stage skill**
Open the primary stage skill file (e.g. `5a. overlays_skill.md`) and add a reference to the new skill file in the relevant step. Use the full workspace-relative path:
```
Read `Youtube/Input/2. Skills/5. Visuals/{skill-name}.md` for [what it covers].
```

**Step 8 — Update hide command**
If any new top-level folder was created outside `Youtube/`, add it to `.claude/commands/hide.md` so Daniel can keep the workspace clean.

---

## Phase 9 — Save Report

*Skip this phase in Quick Lookup mode — respond inline instead.*

Get today's date: `Bash(date +%Y-%m-%d)`.

Save the completed report to:
```
docs/skill-scout/reviews/{YYYY-MM-DD}_review.md
```

Use `docs/skill-scout/weekly-review-template.md` as the skeleton. Fill every section.

Print a plain-text summary:
```
Skill Scout complete — {date}
Sources checked: skills.sh registry + web search + npx skills check
Skills evaluated: {N}
Install candidates: {N}
Adapt candidates: {N}
Take inspiration: {N}
Report saved to: docs/skill-scout/reviews/{date}_review.md
```
