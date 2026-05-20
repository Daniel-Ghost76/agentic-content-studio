# Alternatives Review — 02_codex_mobile

All segments below are cut and ready to swap into the EDL. Each entry shows
the beat it replaces, the source timestamps, and the transcript text. To swap,
replace the matching entry in `edl.json` with the start/end listed here.

---

## Beat 1 — Hook (Late Retakes at End of Recording)

Daniel did the hook several more times near the very end of the session. The
main cut uses the KEEP-marked take at 1907–1938. Review these if you want a
fresher or tighter delivery.

### Alt 1 — Late hook v1 (marked "Maybe")
**Swap out:** `beat_1_hook` [1907.04–1938.44]
**Swap in:** `start: 7664.58, end: 7699.44`
> "So, OpenAI just dropped Codex Mobile and honestly this thing is kind of
> insane. I'm going to show you an AI agent physically going to my Mac Mini,
> open up YouTube and schedule a video with description, timestamps, everything
> all from my phone. So in this video I'll walk you through everything you need
> to know, what it does, how to set it up and how to actually put it to work.
> Alright let's jump in. Maybe."

### Alt 2 — Late hook v2 (unmarked)
**Swap in:** `start: 7784.84, end: 7815.82`
> "OpenAI just dropped Codex Mobile and honestly this thing is kind of insane.
> I'm going to show you an AI agent physically go into my Mac mini, open up
> YouTube and schedule a full video with descriptions, timestamps, everything
> all from my phone. So in this video, I'll walk you through everything you
> need to know what this is about, what this does and how to set up and how to
> actually put it to work. All right, let's jump in."

### Alt 3 — Late hook v3 (unmarked)
**Swap in:** `start: 7837.20, end: 7887.36`
> "So, OpenAI just dropped Codex Mobile and honestly, this thing is kind of
> insane. I'm going to show you an AI agent physically go into my Mac Mini,
> open YouTube and schedule a full video with description, timestamps,
> everything all from my phone. So in this video, I'll walk you through
> everything you need to know, what this is about, what this does, how to set
> it up, and how to put it to work and how to actually put it to work. All
> right, let's jump in."

### Alt 4 — Late hook v4 (unmarked)
**Swap in:** `start: 7903.52, end: 7941.70`
> "OpenAI just dropped Codex Mobile and honestly this thing is kind of insane.
> Now I'm going to show you an AI agent physically go into my Mac mini, open up
> YouTube and schedule a full video with description, timestamps, everything
> all from my phone."

---

## Beat 3 — Setup: Workspace Detail

The main cut uses a short setup line [3150–3161] for speed. This segment gives
more workspace setup detail if you want that context.

### Alt — Workspace setup detail
**Insert after:** `beat_3_setup` [3150.68–3161.70]  
**Add segment:** `start: 3106.18, end: 3124.62, beat: "beat_3b_workspace"`
> "But assuming you have the desktop app, you set up your workspace inside
> Codex. You get your agents together, put your workflows in place, your tasks,
> everything you need to get done. It's all going to live inside your Codex
> workspace. That's your setup, right?"

---

## Beat 4 — Demo: Initial Results Narration

Skipped from main cut to tighten the flow (goes straight from scan to full
results). Add this back if the jump feels abrupt.

### Alt — Results start narration
**Insert between** `beat_4_scan` [4147–4169] and `beat_4_results_prompt2` [4278–4323]  
**Add segment:** `start: 4200.28, end: 4210.38, beat: "beat_4_results_start"`
> "Right so you can see it just said what videos are ready to be posted and
> ones that are not ready so I'm just going to go ahead and"

---

## Beat 4 — Demo: Description Confirmation Detail

Fills in the middle of the description check. Sits between `beat_4_desc_check`
and `beat_4_confirm` if you want the full result narration.

### Alt — Description confirmed detail
**Insert between** `beat_4_desc_check` [4330–4354] and `beat_4_confirm` [4407–4427]  
**Add segment:** `start: 4373.47, end: 4398.69, beat: "beat_4_desc_confirmed"`
> "There we go. Yes, Codex Mobile is ready to be posted / scheduled. It
> includes description. It explains... covers it... it includes tools used,
> timestamps and hashtags so everything is ready to be posted."

---

## Beat 4 — Demo: Run 2 (Full Alternative Demo)

A complete second demo run where the agent succeeded. If you prefer Run 2's
pacing or footage over the main cut's Run 1+3 splice, swap the full Beat 4
demo section.

### Alt — Full demo Run 2
**Replace:** `beat_4_setup` through `beat_4_confirm` (segments 4092–4427) AND
`beat_4_prompt3` through `beat_4_result` (segments 5233–5399)  
**Use instead:** `start: 4879.08, end: 5018.60, beat: "beat_4_run2_full"`
> "Okay, cool. Go ahead and schedule this one for Friday at 4pm for me. And
> you're going to see a pullout YouTube. My hands are up here so I'm not going
> to be touching the keyboard... it gives me a note, this task has been
> completed... And it's been scheduled. This video has been scheduled."
>
> **Note:** Run 2 is one continuous segment vs. the main cut's multi-segment
> splice across Run 1 and Run 3.

---

## Beat 5 — Personal Angle (Alternatives)

Main cut uses the cleaner short take [5629–5647]. Two alternatives available
if you want more detail.

### Alt 1 — Full take with "give it patience" ending (has restarts at start)
**Swap in:** `start: 5904.94, end: 5966.58`
> [has multiple false starts] "...when I got this the first thing I did I added
> something to my Amazon cart to see if it works and first time honestly it was
> a bit slow and I asked it to do it again and it just got noticeably faster it
> learns so give it patience in the beginning And."
>
> **Note:** Contains internal restarts in the first ~40s. The clean delivery
> starts at approximately t=5945.

### Alt 2 — Brief conclusion line
**Append after** `beat_5_personal`:  
**Add segment:** `start: 6002.64, end: 6018.24, beat: "beat_5_conclusion"`
> "So you have to be a bit patient with it in the beginning, but once you learn
> how to set up, how to get everything up and running, it can be a really
> powerful tool."

---

## Beat 6C — UI Observation Extended

Main cut ends at "from a small screen." [6281–6294]. This adds the "worth
having in your toolkit" conclusion.

### Alt — Extended ending
**Extend** `beat_6c_ui` end to `6307.76` (or add as new segment after it):  
**Add segment:** `start: 6295.53, end: 6307.76, beat: "beat_6c_ui_conclusion"`
> "It's generally a tool worth having in your toolkit. And so far, I generally
> think this is a tool worth having in your toolkit."
>
> **Note:** Has a repeated phrase — may want to trim to just "It's generally a
> tool worth having in your toolkit." ending at approximately 6305.

---

## Swapping Instructions

1. Open `edl.json`
2. Find the `beat` entry you want to replace
3. Change `start` and `end` to the values listed here
4. Save and re-run render.py

For inserts (adding a segment that isn't in the main cut), add a new JSON object
to the `ranges` array at the correct position. The ranges must be in output
order — not source order. Timestamps within a range refer to source video time.
