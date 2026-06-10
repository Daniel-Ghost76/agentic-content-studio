# Session Handoff

Generate a compressed context brief for the next session. Saves to `.claude/session_handoff.md` and prints to chat.

---

## Phase 1 — Detect active work (read, don't ask)

1. Run `git status` and `git log --oneline -10` to see what changed this session.
2. Scan `Youtube/Output/` for the most recently modified files — infer active `project_id` and stage.
3. Read `MEMORY.md` and any memory files that seem relevant to current work.
4. Scan `.claude/commands/` to remind yourself of available slash commands.

## Phase 2 — Check for memory gaps

Before writing the handoff, check if anything from this session should be written to persistent memory:
- New user preferences or feedback given this session → `feedback_*.md`
- New project decisions or state changes → `project_*.md`
- New external resource references → `reference_*.md`

Write any missing memories now (before the handoff), then mention them in the handoff under **Memory updated**.

## Phase 3 — Write the handoff

Write the handoff to `.claude/session_handoff.md`, overwriting any previous version. Then print the full content to chat.

Use this exact format — dense, no fluff:

```markdown
# Session Handoff
**Date:** {YYYY-MM-DD}  **Model:** {model used}

## Active Work
- **Project:** `{project_id}` · Stage {N} {stage name}
- **Status:** {one sentence — where things stand right now}

## Decisions Made
{bullet list — each decision + what was decided; omit if none}

## Files Created / Modified
{bullet list of paths + one-word description of change; omit unchanged files}

## Blockers / Open Questions
{bullet list; omit section if none}

## Next Step
**`/{command}`** — {one sentence on exactly what to do next and why}
```

Keep each section scannable — one line per bullet, no sub-bullets, no explanations beyond what's needed to act.
