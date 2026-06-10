# NotebookLM — Research Aid (Manual, Daniel-Operated)

NotebookLM is a **manual tool Daniel uses by hand** — it has no API and is not wired into any agent or pipeline stage. The scripting agent does not call it. This doc exists so the scripting stage knows when to *suggest* Daniel use it and for what.

It ingests a fixed set of sources (PDFs, Google Docs, URLs, YouTube videos, audio) into a "notebook" and answers questions **grounded only in those sources, with citations** — no open-web guessing. It also generates study guides, briefing docs, mind maps, and Audio Overviews (a podcast-style summary you can listen to away from the desk).

Free with a Google account (`daniel@ministryflow.co`). Web + mobile app.

## When it helps scripting

**1. Tutorial-build videos that must be technically correct.**
Before/during the Phase 2 deep-dive, Daniel gathers the real source docs for the tool being demoed (official docs, changelogs, a reliable guide) into a notebook and interrogates it for accurate, cited specifics — version numbers, exact commands, real limits. Use this when a wrong detail on camera would cost credibility. Complements, does not replace, the Perplexity ideation tool: **Perplexity = live open web; NotebookLM = deep dive on a trusted closed corpus.**

**2. Voice / structure synthesis (one-time).**
The `Nate Herk YT Transcript/` folder in this directory is a ready-made corpus. Daniel can load those transcripts into a notebook and ask it to extract recurring structural and tonal patterns, then fold the findings into `voice_reference/nate_herk_voice_reference.md`. Do once, reuse forever.

## How the scripting agent uses this

- For **tutorial-build** videos, the agent may remind Daniel: "If you want cited technical accuracy, run the source docs through NotebookLM before we lock Phase 2."
- The agent never automates it and never blocks on it. If Daniel skips it, proceed.
- Live, open-web facts still come from the Perplexity ideation tool, not NotebookLM.

## Daniel's primary personal use (outside scripting)

Learning. Dump the docs of whatever tool he's skilling up on into a notebook, generate an Audio Overview, and absorb it on the go. This is the highest-value use of the tool and is independent of the content pipeline.
