# Overlay Map — 01-transcript-youtube
**Date:** 2026-06-09 | **Agent:** Overlay (Claude Code) | **Status:** Approved for build

> All timestamps pinned from `transcripts/01-transcript-youtube_raw.json` (word-level).
> Higgsfield slots omitted — handled by Codex separately.
> Face cam: **bottom-left**. All overlays: right-panel, bottom-right, or lower-third centered.
> ✅ = already built in `hook_caption_test/index.html`

---

## Summary

| Type | Count | Built | To Build |
|------|-------|-------|----------|
| CAPTION (glass panel) | 4 | 0 | 4 |
| PUNCH_WORD | 1 | 0 | 1 |
| ZOOM (bg scale) | 5 | 0 | 5 |
| CALLOUT card | 5 | 1 | 4 |
| STEP_LIST | 2 | 1 | 1 |
| STAT_CARD | 2 | 0 | 2 |
| CTA | 2 | 0 | 2 |
| **TOTAL** | **21** | **2** | **19** |

---

## Section 1 — HOOK (0:00–0:35)

### OV-01 — CAPTION
```
[0:01.3] CAPTION
text:     "I'm building an AI business from scratch."
duration: 3.5s  (0:01.3 → 0:04.8)
position: lower-third, right-side clear of face cam (right: 160px, bottom: 80px)
capsule:  glass-panel-frosted
trigger:  word "scratch" ends at 1.70s — show immediately after
```

### OV-02 — PUNCH_WORD
```
[0:05.4] PUNCH_WORD
text:     "DAY ONE."
duration: 2.5s  (0:05.4 → 0:07.9)
position: center-screen
capsule:  05a_punch_word
trigger:  "This is day one" starts at 5.40s — fires on "day"
```

---

## Section 2 — Channel Context (0:35–1:30)

### OV-03 — ZOOM
```
[1:03.5] ZOOM
peak:     1.08×
ease_in:  0.8s  (starts 1:03.5, peaks 1:04.3)
hold:     1.2s  (1:04.3 → 1:05.5)
ease_out: 0.6s  (1:05.5 → 1:06.1)
reason:   "angle for the channel" payoff at 1:04.48
```

### OV-04 — CAPTION
```
[1:05.0] CAPTION
text:     "The raw process of building the business from scratch."
duration: 4.0s  (1:05.0 → 1:09.0)
position: lower-third, right-aligned (right: 160px, bottom: 80px)
capsule:  glass-panel-frosted
trigger:  "raw process of building" starts at 1:06.12 — show just before
```

---

## Section 3 — Tools Overview (1:30–2:30)

### OV-05 — STAT_CARD
```
[2:08.0] STAT_CARD
content:  label: "WORKFLOW" | value: "Any YouTube Channel → Clean Transcript Data"
duration: 6.0s  (2:08.0 → 2:14.0)
position: right-panel (right: 160px, vertically centered)
capsule:  02b_stat_metric_card
trigger:  "The output will look something like this" at 2:07.52
```

### OV-06 — CALLOUT ✅ BUILT (slot_001)
```
[2:14.0] CALLOUT — slot_001 — "TOOL / yt-dlp"
```

---

## Section 4 — Live Demo Part A (2:30–5:00)

### OV-07 — ZOOM
```
[3:01.0] ZOOM
peak:     1.10×
ease_in:  0.6s  (starts 3:01.0, peaks 3:01.6)
hold:     2.5s  (3:01.6 → 3:04.1)
ease_out: 0.8s  (3:04.1 → 3:04.9)
reason:   entering live demo — "let's go to YouTube" at 3:02.22
```

### OV-08 — CALLOUT
```
[3:05.0] CALLOUT
label:    "CREATOR"
value:    "Alex Hormozi"
duration: 6.0s  (3:05.0 → 3:11.0)
position: bottom-right (right: 160px, bottom: 60px)
capsule:  02a_callout_card
trigger:  navigating to Alex's channel at 3:02.36
```

### OV-09 — CAPTION
```
[4:01.5] CAPTION
text:     "It just blows my mind every time."
duration: 3.0s  (4:01.5 → 4:04.5)
position: lower-third, right-aligned (right: 160px, bottom: 80px)
capsule:  glass-panel-frosted
trigger:  "blows my mind every time" at 4:02.16
```

### OV-10 — ZOOM
```
[4:01.5] ZOOM
peak:     1.08×
ease_in:  0.5s  (starts 4:01.5, peaks 4:02.0)
hold:     2.0s  (4:02.0 → 4:04.0)
ease_out: 0.6s  (4:04.0 → 4:04.6)
reason:   speed/efficiency payoff — "blows my mind every time"
```

---

## Section 5 — Folder Structure (5:00–5:30)

### OV-11 — STEP_LIST ✅ BUILT (slot_002)
```
[5:11.0] STEP_LIST — slot_002 — Input / Output / Tools (5:11 → 5:26)
```

---

## Section 6 — Live Demo Part B (5:30–8:00)

### OV-12 — ZOOM
```
[6:03.0] ZOOM
peak:     1.08×
ease_in:  0.6s  (starts 6:03.0, peaks 6:03.6)
hold:     1.5s  (6:03.6 → 6:05.1)
ease_out: 0.5s  (6:05.1 → 6:05.6)
reason:   screen zoom onto yt-dlp in folder — "you can see yt-dlp" at 6:03.90
```

### OV-13 — CALLOUT
```
[6:05.5] CALLOUT
label:    "TOOL"
value:    "yt-dlp"
duration: 5.0s  (6:05.5 → 6:10.5)
position: bottom-right (right: 160px, bottom: 60px)
capsule:  02a_callout_card
trigger:  "you can see yt-dlp. This is the tool we just downloaded" at 6:03.90
note:     second yt-dlp appearance — Daniel showing it in the folder
```

### OV-14 — CAPTION
```
[7:09.0] CAPTION
text:     "Make sure it's all nice and clean."
duration: 3.5s  (7:09.0 → 7:12.5)
position: lower-third, right-aligned (right: 160px, bottom: 80px)
capsule:  glass-panel-frosted
trigger:  exact spoken phrase at 7:10.16
```

---

## Section 7 — ChatGPT Troubleshooting (8:00–9:30)

### OV-15 — CALLOUT
```
[8:00.0] CALLOUT
label:    "TOOL"
value:    "ChatGPT"
duration: 5.0s  (8:00.0 → 8:05.0)
position: bottom-right (right: 160px, bottom: 60px)
capsule:  02a_callout_card
trigger:  "you just tell Chat" at 8:00.82 — error handling moment
```

### OV-16 — STEP_LIST
```
[8:02.0] STEP_LIST
steps:    1. Spot the error  |  2. Paste into Chat  |  3. Run it again
duration: 9.0s  (8:02.0 → 8:11.0)
position: right-panel (right: 160px, vertically centered)
capsule:  02c_step_list
stagger:  step 1 at 0s, step 2 at +2.5s, step 3 at +4.5s
trigger:  the "when you do" error-fix loop at 8:00.12
```

### OV-17 — CALLOUT
```
[9:01.0] CALLOUT
label:    "PROMPT"
value:    "Give me 10 URLs of the best AI creators"
duration: 6.0s  (9:01.0 → 9:07.0)
position: bottom-right (right: 160px, bottom: 60px)
capsule:  02a_callout_card
trigger:  Daniel's exact ChatGPT prompt at 9:02.26
```

### OV-18 — ZOOM
```
[9:09.0] ZOOM
peak:     1.08×
ease_in:  0.5s  (starts 9:09.0, peaks 9:09.5)
hold:     2.0s  (9:09.5 → 9:11.5)
ease_out: 0.6s  (9:11.5 → 9:12.1)
reason:   "look at what's working, look at what's not" — search capability payoff
```

---

## Section 8 — Results + Use Cases (9:30–10:45)

### OV-19 — ZOOM
```
[10:02.0] ZOOM
peak:     1.08×
ease_in:  0.5s  (starts 10:02.0, peaks 10:02.5)
hold:     2.0s  (10:02.5 → 10:04.5)
ease_out: 0.5s  (10:04.5 → 10:05.0)
reason:   landing on the actual transcript output with real stats
```

### OV-20 — STAT_CARD
```
[10:03.0] STAT_CARD
content:  "36 min · 47K views · 1,600 likes"
sub:      "→ Full transcript, ready to use"
duration: 7.0s  (10:03.0 → 10:10.0)
position: right-panel (right: 160px, vertically centered)
capsule:  02b_stat_metric_card
trigger:  "47,000 views, 1,600 likes" at 10:03.32
note:     count-up animation on each number
```

### OV-21 — CTA
```
[10:35.0] CTA subscribe-ask
type:     subscribe pill
duration: 8.0s  (10:35.0 → 10:43.0)
position: bottom-right (right: 160px, bottom: 60px)
capsule:  06a_subscribe_ask
```

### OV-22 — CTA
```
[10:40.0] CTA comment-prompt
text:     "What will you build with this?"
duration: 7.0s  (10:40.0 → 10:44.3)
position: bottom-center (centered, bottom: 60px)
capsule:  06c_comment_prompt
```

---

## Build Notes

- All overlays built inside `hook_caption_test/index.html` master composition
- Zooms implemented as GSAP `transform: scale()` on `#bg` video element
- Face cam at bottom-left — no overlays placed in that quadrant (except slot_001 which pre-dates this rule and was approved)
- Slot_001 and slot_002 already present in the HTML — do not re-add
- After all events added: run `npx hyperframes lint` + `npx hyperframes inspect` — zero errors before render
