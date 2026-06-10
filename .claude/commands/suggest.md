# Suggest — Next Command Advisor

When invoked as `/suggest`, read the conversation context and output exactly one recommendation block. No preamble, no explanation — just the block.

---

## Command Catalog

### YouTube Pipeline (Workspace)

| Command | Stage | Suggest when... |
|---------|-------|-----------------|
| `/ideate` | 1 | Starting a new video, no idea locked yet, or Daniel mentions a topic he wants to cover |
| `/script` | 2 | Idea approved and PDF saved; ready to write |
| `/production-materials` | 3 | Script done; Daniel is about to record |
| `/edit` | 4 | Raw footage dropped in; ready to start full editing pipeline |
| `/cut-edit` | 4b | Footage normalized and manifest exists; ready to cut |
| `/overlay` | 5a | Cut approved; building visual overlays |
| `/visuals` | 5 | Overlay map from 4c approved; ready for full visual production |
| `/review` | 6 | Final video exists; pre-publish QC needed |
| `/thumbnails` | 6/7 | Review passed; thumbnail needed before publish |
| `/publish` | 7 | Thumbnail done; video ready to go live |
| `/distribute` | 8 | Video published; push to other platforms/formats |
| `/analytics` | 9 | Video has been live 7+ days; check performance |
| `/reverse-engineer` | 4 | Analyzing a reference video for editing style or structure |
| `/cleanup` | any | Session ended or pipeline has temp/orphaned files to clear |

### Utility (Workspace + Global)

| Command | Suggest when... |
|---------|-----------------|
| `/grill-me` | Kicking off a complex task with unclear alignment or gaps in requirements |
| `/skill-scout` | Weekly review, or a repeated manual step that should be automated |
| `/critique` | A plan is written and needs a brutal honest audit before executing |
| `/hide` | About to share screen or record; internal workspace files should be invisible |
| `/unhide` | Done recording; restore full file visibility in VS Code |
| `/session-handoff` | Ending a session, OR context is visibly large (long session, many tool calls, Daniel mentions context/tokens/cost) |

### Built-in Claude Code

| Command | Suggest when... |
|---------|-----------------|
| `/code-review` | Code or scripts changed and need a quality pass before committing |
| `/code-review ultra` | High-stakes or large change; want multi-agent cloud review |
| `/simplify` | Code works but feels over-engineered or redundant |
| `/verify` | Change made but not yet confirmed working in the real running app |
| `/run` | Need to see the app actually running to confirm a fix |
| `/loop` | Repeating a command on a schedule (e.g. polling a status) |
| `/schedule` | Setting up a recurring automated agent routine |
| `/fast` | Long session; want faster responses (toggles Opus fast mode) |
| `/compact` | Context getting large; want to compress history without clearing it |
| `/clear` | Starting fresh; clearing all conversation history |
| `/memory` | Checking, editing, or auditing persistent memory entries |
| `/cost` | Wondering how many tokens this session has consumed |
| `/model` | Switching models mid-session |
| `/config` | Changing theme, model default, or simple settings |
| `/init` | New project or repo that needs a CLAUDE.md created |
| `/update-config` | Adding a hook, permission, or environment variable to settings.json |
| `/fewer-permission-prompts` | Too many permission dialogs appearing on routine tool calls |
| `/keybindings-help` | Wanting to rebind a key or add a chord keyboard shortcut |
| `/find-skills` | Looking for a capability that might exist as an installable skill |
| `/claude-api` | Working with the Anthropic API; need model IDs, pricing, or params |
| `/hyperframes` | Building any HTML-based video overlay, caption, or animation |
| `/hyperframes-cli` | Running HyperFrames init, lint, preview, or render commands |
| `/help` | Need a full overview of Claude Code capabilities |

### Trigger Phrases (no slash required)

| Phrase | Effect | Suggest when... |
|--------|--------|-----------------|
| `think` / `think hard` | Activates extended reasoning | Problem is complex and the first-pass answer feels shallow |
| `think harder` | Deeper extended reasoning | Previous answer missed something important |
| `/code-review ultra` or `ultrareview` | Multi-agent cloud PR review | PR is large, high-stakes, or touches shared infrastructure |
| `plan` / `/plan` | Enters plan mode (read-only design phase) | About to implement something non-trivial with multiple valid approaches |

---

## Selection Rules

Pick the command that is:
1. **Stage-appropriate** — matches where Daniel is in the current project pipeline
2. **Unambiguous** — one clear next step, not a fork between equals
3. **Actionable right now** — prerequisites already exist

Do NOT suggest if:
- No command fits clearly better than the others
- The response is answering a general question
- Mid-troubleshooting or mid-task (wait for the current task to complete)
- The suggestion would just repeat the command just run

---

## Output Format

Single line, after a horizontal rule. No bullet. No preamble.

```
---
**Next:** `/command` — one sentence tied to the current project and context.
```

Example:
```
---
**Next:** `/script` — idea locked for `03_ai_agency`, ready to draft the script.
```

For trigger phrases (no slash):
```
---
**Next:** `think harder` — this problem has multiple edge cases worth reasoning through before committing.
```
