# Visuals Brief Format — Reference & Template

## What This File Is For

This document defines the format for all Visuals Brief files produced by the scripting agent. The Codex pre-production materials agent reads these briefs to build presentation-ready slides and visual materials before Daniel records the video.

**Important:** Visuals Briefs are for SLIDE CREATION — not raw video editing. Slides are built BEFORE recording so Daniel can share his screen and present them during the recording session. Do not edit any recorded footage; that is a separate stage handled by a different agent.

---

## When the Scripting Agent Generates a Visuals Brief

Generate when:
- Video type is concept/explainer, news drop, or story/business
- Daniel confirmed during Phase 1 that slides or screen visuals are needed

Skip entirely when:
- Video is a pure demo or tutorial where the screen recording carries all the visual weight
- Daniel confirmed in Phase 1 that it is talking head only with no slides

---

## File Naming and Save Location

Name: `{project_id}_visuals_brief.md`
Save to: `Youtube/Input/4. Resources/3. pre-production_materials_resources/`

Example: `02_codex_mobile_visuals_brief.md`

---

## Required File Structure

Every Visuals Brief must open with this header block:

```
# Visuals Brief — {Title}
**Project ID:** {project_id}
**Episode:** {N} of 30
**Series:** Building an AI Business From Scratch
**Script status:** Draft 2 approved / under review

---

## What This Brief Is For

This brief is for the SLIDE CREATION stage — not raw video editing.
These slides are built BEFORE Daniel records the video so he can present them on screen during recording.

The Codex pre-production materials agent's job: produce presentation-ready slides or visuals for each beat listed below.
Daniel will share his screen showing these slides while recording the corresponding section.

Do not edit any recorded footage. That is a separate stage.

---
```

Then one section per beat, using this format:

```
## Beat {N} — {Beat Name}

**Visual type:** slide | diagram | text-overlay | b-roll-instruction | none
**Content:** [What the Codex pre-production materials agent should create — specific enough to execute without follow-up]
**On-screen text (if any):** [Exact words that should appear — verbatim, not paraphrased]
**Style notes:** [Minimal / high contrast / dark background / brand colours / etc.]
**Timing notes:** [How long this is on screen / whether it should animate in / etc.]
```

Beats with no visual still get an entry with `**Visual type:** none` — so the Codex pre-production materials agent has a complete picture of the full video.

---

## Visual Type Definitions

| Type | Use when |
|------|----------|
| `slide` | A clean slide with headline + supporting text or bullets |
| `diagram` | A visual that shows a relationship, flow, or structure |
| `text-overlay` | A single word, phrase, or short line that appears over footage |
| `b-roll-instruction` | Instructions for what footage to source (not a slide — a note to the editor) |
| `none` | Beat has no visual — talking head or demo only |

---

## Example — Concept Video

```
# Visuals Brief — LLMs Explained
**Project ID:** 03_llms_explained
**Episode:** 2 of 30
**Series:** Building an AI Business From Scratch
**Script status:** Draft 2 approved

---

## What This Brief Is For

This brief is for the SLIDE CREATION stage — not raw video editing.
These slides are built BEFORE Daniel records the video so he can present them on screen during recording.

The Codex pre-production materials agent's job: produce presentation-ready slides or visuals for each beat listed below.
Daniel will share his screen showing these slides while recording the corresponding section.

Do not edit any recorded footage. That is a separate stage.

---

## Beat 1 — The Black Box Problem

**Visual type:** none
**Content:** No visual — Daniel on camera only. Starts with screen recording of typing into ChatGPT.
**On-screen text (if any):** n/a
**Style notes:** n/a
**Timing notes:** n/a

---

## Beat 2 — Prediction Machines

**Visual type:** diagram
**Content:** Simple left-to-right flow: Input text → LLM → Output text. Under the LLM box, label: "trained to predict the next word, at scale." Show tokens building up word by word.
**On-screen text (if any):** "The sky is... [blue]" — shown building word by word
**Style notes:** Dark background, minimal. White text. No gradients.
**Timing notes:** Animate word-by-word build slowly — allow 3–4 seconds per word reveal.

---

## Beat 3 — Why They're All Different

**Visual type:** slide
**Content:** Three-column comparison: Claude (Anthropic) / ChatGPT (OpenAI) / Gemini (Google). Each column: logo placeholder + 2-line personality note.
**On-screen text (if any):** Same prompt shown at top. Three different-toned outputs shown below each column.
**Style notes:** Clean grid. Brand colours of each company if available, otherwise white on dark.
**Timing notes:** All three columns visible at once — no animation needed.

---

## Beat 4 — What This Means For You

**Visual type:** slide
**Content:** Two-column before/after: LEFT = "Vague prompt: write me a summary." RIGHT = "Structured prompt: [role] [task] [format] [constraints]."
**On-screen text (if any):** Left column output: generic paragraph. Right column output: tight structured result.
**Style notes:** Contrast left/right clearly — red tint left, green tint right, or just label them BAD / BETTER.
**Timing notes:** Start with left column only, reveal right on cue.

---

## Beat 5 — CTA Bridge

**Visual type:** none
**Content:** No visual — Daniel on camera only.
**On-screen text (if any):** n/a
**Style notes:** n/a
**Timing notes:** n/a
```
