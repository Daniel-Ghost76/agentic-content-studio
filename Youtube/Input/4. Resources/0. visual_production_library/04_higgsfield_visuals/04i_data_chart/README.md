# 04i — Data Chart

**Sub-library:** `04_higgsfield_visuals`  
**Status:** draft — seeded from eRS3CmvrOvA (Nate Herk)

## What It Is

A Higgsfield clip of a branded data visualization — a line chart or bar chart on a dark background showing benchmark, compression, or comparison data. Used when citing third-party stats or demonstrating a before/after performance result with numbers.

## When To Use

- Daniel cites published benchmark data with specific numbers ("a 56 KB file becomes 299 bytes")
- Showing a before/after metric as a chart rather than a text stat
- Any "here's the proof from their data" moment that benefits from a visual graph

## When Not To Use

- For a single number — use `02b_stat_metric_card` instead
- When the data is Daniel's own result (use a screen recording instead)
- For concepts with no quantitative data — use `04c_abstract_concept`

## What Good Looks Like

- Background: near-black, logo branding top-left (e.g. "Claude benchmark" with Anthropic icon)
- Y-axis: labeled with data units (kb, bytes, %, etc.)
- X-axis: implied (time or categories)
- Lines: 2 teal/green color variations (teal = one dataset, lighter green = another)
- Data point labels: prominent white bold numbers at key points (e.g. "299b", "109b")
- Legend: pill-shaped labels at bottom, matching line colors
- No gridlines or minimal dotted gridlines
- Lines animate in (draw-on effect) during the clip
- Duration: 4–7 seconds (line draw-on takes ~60% of the duration)

## Reference

`eRS3CmvrOvA/screenshots/frame_0534000ms.jpg` — "Claude benchmark" chart, two lines (Playwright snapshot vs Access log) compressing from ~300kb to 299b/109b. Teal and green line colors. Legend pills at bottom.
