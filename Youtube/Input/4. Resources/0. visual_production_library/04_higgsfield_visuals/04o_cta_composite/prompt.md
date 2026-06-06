# Higgsfield Capsule Prompt: CTA Composite

**Sub-library:** `04_higgsfield_visuals`  
**Capsule:** `04o_cta_composite`  
**Tool:** Higgsfield video generation API  
**Status:** draft — seeded from eRS3CmvrOvA

---

## Variant A — Community / Resource CTA

### Prompt Template

```
End-of-video CTA shot. Near-black background (#09090b).

Top portion: large bold uppercase white text "{cta_headline}" (~80px, font-weight 800, 
centred horizontally at ~35% from top).

Below the text: a browser window (macOS-style, dark chrome, traffic-light dots, 
URL bar showing "{destination_url}") showing a screenshot of {page_description}.
The browser window is centred and takes up ~60% of the frame width.

A faint teal glow traces the bottom edge of the browser window.
Mostly static — minor ambient glow motion.

Aspect ratio: 16:9. Duration: {duration_s} seconds.
```

### Variables (Variant A)
- `{cta_headline}` — e.g. `"FREE SKOOL COMMUNITY"`, `"GET THE FREE GUIDE"`, `"JOIN THE COMMUNITY"`
- `{destination_url}` — the URL shown in the browser bar (e.g. `"skool.com/ais"`)
- `{page_description}` — what the browser shows (e.g. `"a community platform feed with posts, a leaderboard, and member avatars visible"`)
- `{duration_s}` — clip duration in seconds (default: `5`)

---

## Variant B — YouTube Player End Card

### Prompt Template

```
YouTube end card. Dark background (#111111).

Full-width YouTube player frame showing a video with:
- YouTube logo (red) top-left: "YouTube"
- Video thumbnail in the player: {video_thumbnail_description}
- Below the player: video title "{video_title}" in white, bold
- Channel info: channel name "{channel_name}", subscriber count "{subscriber_count}", 
  verified checkmark
- Action row: Like button (thumbs up), Dislike, Share, Thanks, more (...)

Animation: a cursor/hand icon slowly moves toward the Like button, 
the Like button fills/activates (turns blue/filled), the like count increments by 1.

Aspect ratio: 16:9. Duration: {duration_s} seconds.
```

### Variables (Variant B)
- `{video_thumbnail_description}` — description of the thumbnail (e.g. `"a man in a black hoodie in front of a white wall, text overlay 'I Tried 100+ Claude Code Skills'"`)
- `{video_title}` — full video title
- `{channel_name}` — e.g. `"Daniel Danut | AI Systems"`
- `{subscriber_count}` — e.g. `"2.4K subscribers"`
- `{duration_s}` — clip duration in seconds (default: `5`)

---

## Hybrid Approach Note

For Variant A: generate the background + browser frame in Higgsfield, composite the actual screenshot of the destination page inside the browser using HyperFrames perspective transform.

For Variant B: this may be best built entirely in HyperFrames as an HTML mockup of the YouTube UI, rather than relying on Higgsfield to render accurate YouTube UI elements and the like animation.

---

## Anti-list

- No fake subscriber counts or like counts unless they are specifically set in variables
- Variant A headline must be ≤4 words
- Variant B should not show competitor channels or videos in the thumbnail
- Do not use these clips mid-video
