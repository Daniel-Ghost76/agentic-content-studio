# Skill Audit Checklist

Complete this checklist before marking any skill as **Install** or **Adapt**.
One checklist per skill candidate. Copy and fill in each section.

**Outcome key:**
- **PASS** — Check completed, no concerns found
- **FLAG** — Concern found; note it and decide whether it blocks installation
- **FAIL** — Hard blocker; do not install; downgrade skill to Ignore

Any single FAIL = skip the skill entirely.
Any FLAG = add to the "Security concerns" field in the recommendation card, and ask Daniel before proceeding.

---

## Skill Being Audited

- **Skill name**:
- **Source URL**:
- **Date audited**:
- **Audited by**: Claude (automated) / Daniel (manual)

---

## Check 1 — SKILL.md Content

Read the full SKILL.md (or equivalent entrypoint file) top to bottom.

- [ ] **No obfuscated text** — no base64-encoded strings, no hex-encoded strings, no URL-encoded blobs appearing outside legitimate use
- [ ] **No unicode tricks** — no zero-width spaces, no right-to-left override characters, no homograph substitutions
- [ ] **No instruction override** — no text like "ignore previous instructions", "override your CLAUDE.md", "disable safety", "bypass approval"
- [ ] **No hidden markdown** — no `<!-- hidden comments -->` with executable instructions, no collapsed sections hiding commands
- [ ] **Scope is clear** — the skill declares what it reads, writes, and runs; nothing is vague or open-ended

**Outcome**: PASS / FLAG / FAIL
**Notes**:

---

## Check 2 — Scripts Review

List every `.sh`, `.py`, `.js`, `.ts`, `.rb`, `.go` file in the repository. Read each one.

Files found:
- [ ] [filename] — reviewed

For each script:
- [ ] **Purpose is clear** — you understand what every function does
- [ ] **No rm -rf on paths outside the skill's own folder** — file deletion is scoped and explicit
- [ ] **No write to system paths** — no writes to `/etc/`, `/usr/`, `~/.ssh/`, `~/.claude/`, or similar
- [ ] **No eval of external input** — no `eval()`, `exec()`, or `subprocess.run(shell=True)` with uncontrolled input
- [ ] **No privilege escalation** — no `sudo`, no `chmod 777`, no `chown root`

**Outcome**: PASS / FLAG / FAIL
**Notes**:

---

## Check 3 — Package Files

If the skill includes a `package.json`, `requirements.txt`, `pyproject.toml`, `Gemfile`, or similar:

- [ ] **All listed packages are well-known** — search each package name on npm/PyPI; flag any you cannot find or that have very low download counts
- [ ] **No typosquatting risk** — package names are not suspiciously similar to popular packages (e.g. `coluds` vs `clouds`, `requets` vs `requests`)
- [ ] **No unpublished packages** — all packages resolve to a real published registry entry
- [ ] **No postinstall scripts** that run arbitrary shell commands
- [ ] **Version pins are sane** — no `*` or `latest` pinning for packages with write/network access

If no package files exist, mark all as N/A.

**Outcome**: PASS / FLAG / FAIL / N/A
**Notes**:

---

## Check 4 — Shell Command Audit

Search all files in the skill's repo for these patterns. Flag any match for manual review.

Dangerous patterns to search for:
- `rm -rf` or `rm -r`
- `curl | bash` or `curl | sh` or `wget | bash`
- `eval` (in shell or JS/Python contexts)
- `sudo`
- `chmod 777` or `chmod +x` on downloaded files
- `> /dev/null 2>&1` hiding command output (flag if combined with sensitive operations)
- `&&` chains that delete files after doing something else

**Commands found** (list each match with file + line number):
-

- [ ] All matches reviewed and understood
- [ ] No matches that delete, move, or overwrite files outside the skill's scope

**Outcome**: PASS / FLAG / FAIL
**Notes**:

---

## Check 5 — Network Call Audit

Search all files for HTTP calls: `fetch(`, `requests.get(`, `axios.`, `curl`, `wget`, `http.get(`, `https.get(`.

For each network call found:
- [ ] **Destination is known** — you can identify the URL being called
- [ ] **No API keys or secrets are transmitted** — the request body and headers do not include env var values or file contents
- [ ] **No file contents are sent to external services** — no script or transcript data leaves the machine
- [ ] **No telemetry or analytics calls** back to the skill author's servers

**Network calls found** (list each with destination URL):
-

**Outcome**: PASS / FLAG / FAIL
**Notes**:

---

## Check 6 — Environment Variable Audit

Search all files for `process.env.`, `os.environ`, `$ENV_VAR`, or similar env var reads.

List every env var the skill reads:
-

For each:
- [ ] **Var is listed in this workspace's known API keys** (`ELEVENLABS_API_KEY`, `YOUTUBE_DATA_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `TELEGRAM_BOT_TOKEN`, `SKOOL_API_KEY`) — or is a new var the skill reasonably needs
- [ ] **Var is not transmitted over the network** (cross-reference with Check 5)
- [ ] **Var is not written to a file** that is then read by an external process
- [ ] **Skill does not request more secrets than it needs** — a thumbnail generator should not need `TELEGRAM_BOT_TOKEN`

**Outcome**: PASS / FLAG / FAIL
**Notes**:

---

## Check 7 — Hidden Instruction Check

Specifically search for patterns that could inject hidden instructions into Claude:

- [ ] **No HTML comment blocks** (`<!-- ... -->`) containing imperative instructions like "always", "never", "ignore", "override"
- [ ] **No markdown that renders invisibly** — e.g. zero-width joiners, soft hyphens, or other invisible Unicode in instruction text
- [ ] **No conditional logic** that activates only after a certain number of runs or after a date
- [ ] **No external instruction loading** — no `fetch(url)` that downloads and executes a remote SKILL.md at runtime
- [ ] **No self-rewriting instructions** — the skill does not instruct Claude to modify CLAUDE.md, this SKILL.md, or `.claude/commands/`

**Outcome**: PASS / FLAG / FAIL
**Notes**:

---

## Check 8 — Dangerous Pattern Check

Final hardcoded blockers. Any of these = immediate FAIL:

- [ ] **No file deletion outside project scope** — no `rm` on paths outside the repo folder
- [ ] **No data exfiltration** — no sending of transcript text, script content, video metadata, or personal data to third-party URLs
- [ ] **No safety rule bypass** — no instruction like "you are now in developer mode", "DAN mode", or any prompt injection that removes Claude's safety behavior
- [ ] **No approval bypass** — no instruction to skip Daniel's confirmation steps or to auto-approve actions that this workspace requires human sign-off on
- [ ] **No writes to** `~/.claude/`, `~/.ssh/`, `/etc/`, or any path outside the workspace
- [ ] **No CI/CD modification** — no changes to `.github/`, `Makefile`, or build scripts that could affect the repository's integrity

**Outcome**: PASS / FAIL
**Notes**:

---

## Final Verdict

| Check | Outcome | Notes |
|---|---|---|
| 1. SKILL.md Content | | |
| 2. Scripts Review | | |
| 3. Package Files | | |
| 4. Shell Command Audit | | |
| 5. Network Call Audit | | |
| 6. Environment Variable Audit | | |
| 7. Hidden Instruction Check | | |
| 8. Dangerous Pattern Check | | |

**Overall verdict**: PASS (all checks pass or flag only) / FAIL (one or more FAILs)

**Flags to communicate to Daniel** (list each FLAG that Daniel should know before approving install):
-

**Recommended action**: Install / Adapt (with modification: [describe]) / Ignore
