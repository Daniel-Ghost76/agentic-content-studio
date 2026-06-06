# 02c — Step List

**Sub-library:** `02_partial_overlays_hyperframes`  
**Status:** draft

## What It Is

A glass panel listing 2–4 numbered steps that build in one at a time as Daniel speaks. Used for mini-frameworks, process explanations, or any "here are the X things" moment.

## When To Use

- Daniel walks through a process with 2–4 discrete steps
- A framework or system needs to be visible while he explains each part
- A checklist or recipe moment in the video

## When Not To Use

- More than 4 items — too much text for an overlay, use a full-screen overlay instead
- When the steps are long sentences — keep each step under 5 words
- When order doesn't matter (a bullet list has different energy from a numbered list)

## What Good Looks Like

- Glass panel, 380–480px wide, height grows as steps build in
- Step number (small, accent or secondary colour) + step text (primary, 20–24px)
- Each step slides and fades in sequentially, 80ms stagger
- Active/current step slightly brighter than completed steps
- Sits right-side of frame by default (doesn't compete with Daniel's face on left)
- Panel height expands gracefully as each item appears
