# Project Log — 02_codex_mobile Cut Edit

## Session: 2026-05-19

### Source
- **File:** `originals/2026-05-18 23-40-35.mov` (6.18 GB, 133m 30.5s)
- **Audio:** 160kbps, healthy signal — was the main camera recording
- **Note:** A second file `originals/ScreenRecording_05-19-2026 00-46-47_1.MP4` also exists
  but has no microphone audio (mean vol -91dB) — not used for cut

### Transcription
- **Tool:** Groq Whisper large-v3 (free tier)
- **Output:** `transcripts/2026-05-18 23-40-35.json` (9,383 words, 1,229 KB)
- **Shared copy:** `../transcripts/02_codex_mobile_transcript.json`
- **ElevenLabs was NOT used** — monthly quota was exhausted by Episode 1 (8,906 credits needed,
  1,236 remaining). Groq Whisper is now the default transcription tool for this workspace.
- **Groq API key** stored in `~/.claude/.env` under `GROQ_API_KEY`
- **Note on accuracy:** Groq word-level timestamps have ~150ms drift. Cut padding set to
  100ms before / 120ms after word boundaries to compensate.

### EDL
- **File:** `edl.json` — 21 segments, ~9m32s estimated cut
- **Grade:** auto (per-segment color correction)
- **Approach:** Conservative — KEEP-marked takes used where available; for unmarked beats,
  best single attempt selected; MAYBE segments preserved in alternatives_review.md

### Beat selections
| Beat | Source range (s) | Duration | Notes |
|------|-----------------|----------|-------|
| 1 Hook | 1907.04–1938.44 | 31s | KEEP-marked (6× keep) |
| 2A What is it | 2409.90–2451.92 | 42s | KEEP at end |
| 2B What can it do | 2698.79–2725.12 | 26s | KEEP at 2736 |
| 2C Thesis | 2975.18–3004.28 | 29s | "keep approve this is it" at 3010; trimmed restarts from start |
| 3 Setup | 3150.68–3161.70 | 11s | Cleanest attempt; covers download + pro plan + workspace |
| 3C QR code | 3558.87–3593.00 | 34s | KEEP at very end (trimmed) |
| 3D Permissions | 3700.32–3728.00 | 28s | No explicit keep; best clean take |
| 4 Demo (9 segments) | 4092–5399 | ~3m40s | Run 1 for prompts 1+2; Run 3 for prompt 3+result |
| 5 Personal | 5628.90–5647.44 | 18s | Cleaner short take; alternatives in review file |
| 6A Remote ctrl | 6043.76–6055.82 | 12s | Claude Code note; trimmed messy restart at start |
| 6B Either way | 6163.51–6174.33 | 11s | Best delivery |
| 6C UI | 6281.01–6294.43 | 13s | Cleanest complete delivery |
| 7 CTA | 7374.36–7407.56 | 33s | "keep keep keep keep keep approve" at 7410 |

### Output
- **Final cut:** `../02_codex_mobile_cut.mp4`
- **Spec:** 1920×1080, H.264 fast CRF 20, AAC 192k 48kHz, 24fps, loudnorm -14 LUFS
- **Duration:** 572.8s (9m 32.8s)
- **Size:** 112 MB
- **Stage 5 copy:** `Youtube/Output/5. Visuals/02_codex_mobile/02_codex_mobile_cut.mp4` ✓

### Self-eval (timeline_view)
Checked 7 cut boundaries — all passed. No flashes, no audio pops, grade
consistent across segments. Outputs in `verify/`.

### Alternatives
See `alternatives_review.md` for:
- 4 late hook retakes (end of recording)
- Workspace detail segment for Beat 3
- Beat 4 results narration (removed for pacing)
- Beat 4 Run 2 (full alternative demo)
- Beat 5 full take and conclusion line
- Beat 6C extended ending

### Next
Stage 5 (Visuals/Overlays) picks up from `02_codex_mobile_cut.mp4` in the Stage 5 folder.
