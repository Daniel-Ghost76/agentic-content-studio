# Higgsfield Capsule Prompt: Data Chart

**Sub-library:** `04_higgsfield_visuals`  
**Capsule:** `04i_data_chart`  
**Tool:** Higgsfield video generation API  
**Status:** draft — seeded from eRS3CmvrOvA

---

## Prompt Template

```
Branded data visualization on near-black background. 

Top-left: "{brand_name}" label with "{brand_icon_description}" icon — small, white, 
clean — functions as a source attribution.

A line chart fills most of the frame:
- Y-axis: labeled with units "{y_unit}" at key levels ({y_labels})
- Two descending line curves from top-left to bottom-right:
  - Line 1: teal (#0EA5E9 or #14B8A6), represents "{dataset_1_name}", ends at "{dataset_1_end_value}"
  - Line 2: green (#22C55E), represents "{dataset_2_name}", ends at "{dataset_2_end_value}"
- At the end point of each line: a filled dot, and a bold white label showing the 
  end value ("{dataset_1_end_value}" and "{dataset_2_end_value}")
- A vertical dashed line marks the start of compression/transformation zone

Bottom: two pill-shaped legend items:
  - "{dataset_1_name}" with a teal dot
  - "{dataset_2_name}" with a green dot

Lines animate from left to right (draw-on) over the first 60% of clip duration. 
Data labels fade in when their line reaches the end point.
Final 40%: fully drawn chart holds static.

Aspect ratio: 16:9. Duration: {duration_s} seconds.
```

---

## Variables

- `{brand_name}` — source attribution (e.g. `"Claude benchmark"`, `"Context Mode benchmark"`)
- `{brand_icon_description}` — icon description (e.g. `"Anthropic asterisk icon"`, `"small gear icon"`)
- `{y_unit}` — unit label on y-axis (e.g. `"kb"`, `"bytes"`, `"%"`)
- `{y_labels}` — comma-separated y-axis labels (e.g. `"300kb, 10kb, 500b, 100b, 0b"`)
- `{dataset_1_name}` — label for line 1 (e.g. `"Playwright snapshot"`)
- `{dataset_1_end_value}` — end value label for line 1 (e.g. `"299b"`)
- `{dataset_2_name}` — label for line 2 (e.g. `"Access log"`)
- `{dataset_2_end_value}` — end value label for line 2 (e.g. `"109b"`)
- `{duration_s}` — clip duration in seconds (default: `6`, range: `4–8`)

---

## DALL-E Reference Images

**First frame prompt:**
```
Dark data chart. Near-black background. Two lines beginning to draw from the 
top-left of the chart area. "{brand_name}" label top-left. Y-axis labels visible. 
No data points visible yet (lines just started). Teal and green line colors. 
Minimal, premium dark UI aesthetic.
```

**Last frame prompt:**
```
Fully drawn chart. Both lines complete. Teal line ends with "{dataset_1_end_value}" 
label. Green line ends with "{dataset_2_end_value}" label. Legend pills visible at 
bottom. Clean, readable, holdable frame.
```

---

## Anti-list

- No more than 2 lines on one chart — use separate clips for more datasets
- No colour gridlines — dotted grey only, or none
- No bar charts — line charts only for this capsule
- Brand attribution must be small (top-left corner only, not prominent)
- Do not animate axis labels — they should appear static from the start
