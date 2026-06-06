# 04f — Chapter Menu

**Sub-library:** `04_higgsfield_visuals`  
**Status:** draft — seeded from eRS3CmvrOvA (Nate Herk)

## What It Is

A Higgsfield clip showing all video sections as a numbered list inside a styled window frame (resembles a macOS app window or file browser). The current section is brightly highlighted in a filled teal rounded rectangle; the others appear dimmed. Used as a navigation overlay when first listing what the video will cover, and again to mark where you are in the list.

## When To Use

- Immediately after the hook, when Daniel says "here are the 6 skills" — show all 6 in the menu
- Each time a new section starts — highlight the current item, dim the rest
- Works best for 4–8 items; fewer than 4 feels like a short list, not a menu

## When Not To Use

- When the video doesn't have a clearly numbered list structure
- More than 8 items — too crowded
- Back-to-back with `04e_section_intro_circle` in the same transition

## What Good Looks Like

- Window frame: macOS-style, dark, with traffic light buttons (red/yellow/green) top-left, toolbar icons top-right
- Background behind window: very dark, near-black, soft ambient glow at bottom center
- Inside window: numbered skill rows in a 2-column grid (or single column for ≤5 items)
- Each row: a rounded rectangle with a large bold number on left + skill name on right
- Active row: bright teal fill, white text, full opacity
- Inactive rows: dark fill, dimmed text (~30% opacity), barely readable (intentionally blurred in some frames)
- Macbook-style dock visible at the very bottom (Photos, Notion, App Store icons) — optional, adds realism
- Duration: 3–5 seconds, mostly static, small ambient motion

## Reference

`eRS3CmvrOvA/screenshots/frame_0046000ms.jpg` — full menu at video start (all 5 dimmed equally).  
`eRS3CmvrOvA/screenshots/frame_0276000ms.jpg` — "2 SUPER POWERS" highlighted, "SKILL CREATOR" dimmed, others blurred in background.
