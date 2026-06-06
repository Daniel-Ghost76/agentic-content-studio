# Higgsfield Capsule Prompt: Device Scenario

**Sub-library:** `04_higgsfield_visuals`  
**Capsule:** `04g_device_scenario`  
**Tool:** Higgsfield video generation API  
**Status:** draft — seeded from eRS3CmvrOvA

---

## Prompt Template

```
Product scenario mockup. Near-black background (#09090b) with a soft teal ambient 
glow behind the device.

A modern smartphone (iPhone-style, portrait orientation) is centred in the frame, 
slightly left of centre. The phone has a teal glowing outline (2px, rgba(16,185,129,0.85)) 
suggesting it is highlighted or active.

The phone screen shows: {screen_description}. The UI on screen should look like a 
real {app_type} application — dark mode, realistic layout. The key text visible on 
screen is: "{screen_text}".

The device floats gently (subtle 3–5px vertical oscillation over the clip duration). 
The teal glow pulses subtly.

No presenter. Dark, premium, scenario-focused.
Aspect ratio: 16:9. Duration: {duration_s} seconds.
```

---

## Variables

- `{screen_description}` — what's shown on the phone screen (e.g. `"a messaging app conversation thread with a contact named 'Real estate agency'"`)
- `{app_type}` — the type of app being shown (e.g. `"messaging"`, `"CRM"`, `"booking system"`, `"email"`)
- `{screen_text}` — the key readable text on screen (e.g. `"We waste hours every week"`) — keep to 1 short sentence
- `{duration_s}` — clip duration in seconds (default: `4`, range: `3–6`)

---

## DALL-E Reference Images

**First frame prompt:**
```
Smartphone with teal glowing outline on dark near-black background. Phone screen 
shows a {app_type} app in dark mode. Key text visible: "{screen_text}". 
Teal ambient glow behind phone. Portrait orientation, centred-left. Premium, minimal.
```

**Last frame prompt:**
```
Same phone mockup. Glow slightly brighter (pulse peak). Screen text same. 
Subtle downward position (float oscillation bottom position). Clean holdable frame.
```

---

## Anti-list

- No human hands holding the phone — floating device only
- No bright screen backgrounds — dark mode app UI only
- Phone outline must be teal — not white or grey
- Do not show multiple devices — one phone only
- Screen text must be short and legible — do not generate dense paragraph text
