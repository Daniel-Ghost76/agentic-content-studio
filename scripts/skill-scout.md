# Skill Scout — Weekly Runbook

A simple weekly process for discovering new Claude Code skills and agent tools that could improve the YouTube production pipeline. No automation, no background services — you run it when you want it.

---

## When to Run

Run it any time you want — there's no fixed schedule. Good natural triggers:
- Feel like a pipeline stage is taking too long manually
- Want to check if a new tool exists for a specific problem
- Are about to build something from scratch and want to check if it already exists

---

## How to Run

Two modes, one command:

```
/skill-scout                   # full weekly review — gap analysis, scoring, saved report
/skill-scout find X            # quick lookup — "is there a skill for X right now?"
```

**Weekly review** runs the full 7-phase workflow automatically:
1. Snapshot the current workspace state
2. Score each pipeline stage for automation gaps
3. Search GitHub and trusted sources for relevant skills
4. Score each skill on 6 dimensions
5. Write detailed recommendation cards for anything promising
6. Flag any security concerns before recommending install
7. Save a report to `docs/skill-scout/reviews/YYYY-MM-DD_review.md`

The whole run takes 5–10 minutes. Claude prints a summary to the terminal when done.

---

## After the Run — What to Do With the Report

**Step 1 — Read the summary**
Claude prints it to the terminal. It tells you how many skills were found, evaluated, and categorised.

**Step 2 — Open the report**
```
docs/skill-scout/reviews/YYYY-MM-DD_review.md
```
Read the "Top Recommendations" section first. These are the Install and Adapt candidates.

**Step 3 — For each Install or Adapt candidate**
Before doing anything else, open the audit checklist and work through it:
```
docs/skill-scout/audit-checklist.md
```
Claude will have already done a high-level audit pass in Phase 6 of the workflow, but you should do a final manual pass for anything you plan to actually install. The checklist takes 10–15 minutes per skill.

**Step 4 — Make your decision**
Write your decision in the "Carry Forward" section of the report:
- Install → follow the install command in the recommendation card
- Adapt → copy the skill manually into `Youtube/Input/2. Skills/` and modify it to fit the workflow
- Ignore → note why and move on

**Step 5 — Never install automatically**
The skill scout never installs anything on its own. Every install is a conscious decision you make after reading the audit checklist.

---

## How to Install an Approved Skill

Once you've read the skill's source files and completed the audit checklist with no FAILs:

**Option A — Add as a new Claude Code command**
Copy the skill's SKILL.md into this workspace's commands folder:
```bash
cp [downloaded-skill]/SKILL.md ".claude/commands/[skill-name].md"
```
Then edit the file to match this workspace's naming conventions and file paths.

**Option B — Integrate into an existing sub-agent**
Open the relevant sub-agent in `Youtube/Input/1. Sub-agents/` and paste in the relevant technique or step from the skill.

**Option C — Add as a standalone tool script**
Place the script in the relevant tools folder:
```
Youtube/Input/5. Tools/{N}. {stage}_tools/[tool-name].py
```
Reference it from the stage's sub-agent and skill files.

---

## What to Do If a Source Doesn't Exist

The skill scout checks three specific sources: `github.com/anthropics/claude-code`, `skills.sh`, and `github.com/vercel-labs/skills`. As of the time this runbook was written, these URLs needed verification — some may not exist or may have changed.

If a source returns 404 or is unrelated:
- The scout marks it as "Not found / not relevant" in the report
- The search still continues via GitHub queries
- This is normal — the skill ecosystem is evolving; dead links don't mean nothing was found

---

## How to Adapt a Skill Into This Workspace

If a skill is categorised as **Adapt** (good concept, needs modification):

1. Download or copy the skill's source files to a temporary location outside the workspace
2. Read through the SKILL.md and identify which parts are reusable
3. Create a new file in `Youtube/Input/2. Skills/` named after the relevant stage (e.g. `7a. publish_scheduler_skill.md`)
4. Rewrite the skill instructions using this workspace's conventions:
   - Use this workspace's project ID format (`{NN}_{lowercase_slug}`)
   - Read API keys from `~/.claude/.env`
   - Save outputs to `Youtube/Output/{stage}/{project_id}/`
   - Follow the existing sub-agent/skill/rules file pattern
5. Reference the original source URL in a comment at the top of the file

---

## Troubleshooting

**The report is empty or has very few skills**
The Claude Code skill ecosystem is still early. Some weeks there may genuinely be nothing new. This is fine — the value is in the audit process when something does appear, not in finding things every week.

**Claude couldn't access a GitHub URL**
GitHub's web pages sometimes block scrapers. Ask Claude to try the raw README URL instead:
```
https://raw.githubusercontent.com/[owner]/[repo]/main/README.md
```

**A skill looks great but the audit has FLAGS**
Flags are not automatic blockers — they're things to understand before installing. Ask Claude to explain each flag and decide if it's acceptable for this workspace. FAILs, however, are hard blockers.

**I want to run skill-scout for a specific stage only**
Tell Claude directly:
```
/skill-scout — focus on Stage 8 Distribution only
```
Claude will run the full workflow but weight its search queries toward that stage.

---

## File Map

```
.claude/
  commands/
    skill-scout.md                  ← /skill-scout command entry point
  skills/
    skill-scout/
      SKILL.md                      ← full 7-phase skill definition

docs/
  skill-scout/
    weekly-review-template.md       ← template Claude uses to save reports
    audit-checklist.md              ← security checklist before any install
    reviews/
      YYYY-MM-DD_review.md          ← saved weekly reports (Claude creates these)

scripts/
  skill-scout.md                    ← this file (manual runbook)
```
