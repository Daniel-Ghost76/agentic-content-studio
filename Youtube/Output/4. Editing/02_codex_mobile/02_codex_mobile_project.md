# 02_codex_mobile — Project Log

## Session 1 — Cut Edit (Stage 4b) — 2026-06-05

**Strategy:** Full cut from scratch. Source is a 133-minute single-camera recording (`originals/2026-05-18 23-40-35.mov`). Daniel used a deliberate keep/maybe/cut vocal protocol during recording — each section was repeated until he said "keep," at which point all prior retakes were discarded. Target: under 10 minutes, aggressive silence removal, default filler list.

**Decisions:**
- HOOK: kept take at [1907–1938] — marked with 7× "keep" immediately after; clean delivery
- WHAT IS IT: kept take at [2410–2453] — QR code setup, connects to ChatGPT, streams to phone
- CAPABILITIES: kept take at [2461–2479] — explicit "Keep." marker at 2481
- WHY USEFUL: kept take at [2963–3008] — "your computer is running, you're not sitting at it" — marked keep+approve at 3015
- SETUP INTRO: [3168–3173] — clean opener for the how-to block
- HOW TO CONNECT: [3415–3456] — settings → connections → control this Mac → add device → QR code
- PERMISSIONS: two anchors [3654–3658] + [3714–3727] — brief, no explicit keep but only one clean take
- DEMO: hybrid — used first run for command/results/schedule/watch-it-run (ends before camera-angle blocker at ~4611); jumped to second run for AI note reading and YouTube verification (second run has cleaner camera angle on the screen)
- OUTRO: [5475–5510] — "I never touched the computer, just voice prompts"
- PERSONAL NOTE: [5905–5961] — Amazon cart test, it was slow then got faster, it learns
- CTA: [7374–7407] — kept take marked keep×5 + approve at 7410

**compress_gaps results:** 16 ranges → 59 sub-segments; 595.7s → 486.7s; 109s removed (18.3% silence compression) at --max-gap 250 --keep-gap 100

**Visual opportunities (for Stage 4c — Overlay Identifier):**
- HOOK: "AI agent physically go into my Mac Mini" — potential HyperFrame graphic
- CAPABILITIES list: "send messages / schedule YouTube videos / run agents / pull data / open files / trigger workflows" — each item is a caption candidate
- DEMO: full screen recording overlay throughout demo section (~280–395s in output) — the iPhone screen or desktop screen should be composited here
- OUTRO: "it's scheduled for 22 of May 2026 at 4pm" + YouTube Studio UI is on screen — timestamp callout overlay
- CTA: "prompts explained" next video title card

**Reasoning log:**
- Dropped the Claude Code remote-control comparison section (6163–6294) — content is secondary and would push output to 10+ min; can be its own future video
- Used second demo run [5338+] only for verification (not the full second run) — cleaner camera angle on the YouTube Studio confirmation screen; first run's "hands up + AI note" moment was the better capture of the autonomous agent behavior
- compress_gaps threshold set to 250ms/100ms (more aggressive than default 400ms/150ms) per Daniel's instruction to aggressively cut pauses

---

## Session 2 — Cut Edit Re-draft (Draft 3) — 2026-06-06

**Strategy:** Full EDL rebuild from scratch. 30 content ranges → compress_gaps at 800ms/300ms → 45 segments → render → 1.1x speed. Fixed all 10 wrongly-included clips and 4 wrongly-cut clips identified in draft 2 post-mortem.

**Root causes fixed:**
1. compress_gaps threshold: 250ms/100ms → 800ms/300ms. Draft 2 produced 59 micro-fragments; draft 3 produces 45 (sane). Silence reduction: 4.7% vs 18.3%.
2. Content selection: rebuilt EDL from scratch with precise per-error fixes (see list below).

**Content fixes applied:**
- WRONGLY CUT (now added): pro plan info [3150.78–3161.58], update ChatGPT app [3457.17–3469.55], demo intro [4040.70–4060.06], "I didn't touch this. It's the AI." moment [4934.00–4967.34] + YouTube verify [5006.78–5018.48]
- WRONGLY INCLUDED (now removed): WHY USEFUL 26s retake block [2963–2987], "you're you're" stutter split at 2449, "you've you've" stutter start corrected to 3420, "a like a" stutter start corrected to 3433, DEMO RESULTS restart cut at 4290, duplicate DEMO RUNNING narration [4537–4551] dropped in favour of second run, "I I...where where" stutter end at 4588, DEMO VERIFY mess [5338–5399] replaced with second run verify, PERSONAL NOTE 4 false starts [5905–5930] clipped, CTA "um" words removed by starting at 7378/7395
- Demo section restructured: first run (command → results → select → confirm) + second run (schedule → "I didn't touch this" → verify)

**Self-eval:** 4 filmstrip checks passed — no flash, no waveform pop at any sampled boundary.

**Output:**
- `02_codex_mobile_cut.mp4` — 500.1s (8m 20s), 1920×1080 h264 24fps, −14 LUFS
- `02_codex_mobile_cut_1.1x.mp4` — 454.7s (7m 35s), final delivery

**Outstanding:**
- Screen recording (`ScreenRecording_05-19-2026 00-46-47_1.MP4`) exists in originals/ but was NOT used — demo section relies on talking-head narration only; Stage 4c should assess whether iPhone screen recording footage can be composited over the demo section timestamps
- Filler words within kept segments not surgically removed (compress_gaps only compresses silence, not embedded fillers); Stage 4c review may flag any that remain audible

**Output:** `Youtube/Output/4. Editing/02_codex_mobile/02_codex_mobile_cut.mp4`
- Duration: 487.87s (8 min 8s)
- Resolution: 1920×1080, h264, 24fps, 48kHz stereo AAC
- Size: 91.7 MB
- Loudnorm: −14 LUFS / −1 dBTP / LRA 11 applied
