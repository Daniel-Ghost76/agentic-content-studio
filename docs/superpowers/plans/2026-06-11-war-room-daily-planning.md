# War Room Daily Planning System — Implementation Plan (v2)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A self-hosted "War Room" planner app (PWA on iPhone + Mac) that shows Daniel's Daily Planner 1.0 layout on screen every morning at 4:00am, sends phone check-ins at the end of each work block, and — from those ticks — auto-updates the War Map 2026 sheet, its new dashboards, and an Apple Notes mirror, with Claude runs building the plan at 03:30 and scoring the day at 19:00.

**Architecture:** A small Node/Express server on this Mac is the single source of truth (one JSON file per day in `Planning/Daily/`). The PWA frontend replicates the Daily Planner 1.0 PDF (half-hour grid 04:00–19:30, Rating/Hours/Focus/Output header, Priority Tasks, Calls tally, "How can I improve?"). Web Push (VAPID) drives end-of-block check-ins; Tailscale Funnel exposes the server over public HTTPS so the iPhone PWA gets push anywhere (iOS 16.4+, home-screen install required). Headless `claude -p` runs (launchd 03:30 / 19:00 / Sun 18:30) write the day JSON, audit the calendar, and sync the War Map; `pmset` wakes the Mac at 03:23. Apple Notes is a write-only mirror.

**Tech Stack:** Node 18+ (express, web-push — no build step, vanilla JS frontend), launchd + pmset, Tailscale Funnel, Claude Code headless (sonnet), google-workspace MCP (`user_google_email=daniel@ministryflow.co`), AppleScript (Notes mirror), Telegram Bot API (alerts/recaps).

**Decisions locked in the grill (do not re-litigate):**
- Revenue first = (1) building the automated outreach system, (2) YouTube→Skool pipeline velocity. Manual DM sending is never a task; outreach *sends* only ≥13:00 UK.
- Ticks happen ONLY in the PWA (phone or Mac — same app/state). Apple Notes mirror is read-only. A tick in Notes does not count.
- Check-ins: push at end of each scheduled block (✅ / ❌ / enter actual number) + 18:30 day-close sweep; unanswered = unticked.
- Calendar: full autonomy on solo blocks; NEVER edit events with attendees — flag in plan instead.
- Warmap: system-maintained. June objectives set once with Daniel (Task 1). New `Data` tab (a row per day) + `Dashboard 2.0` tab (rating trend, pipeline velocity, outreach engine, streaks — all formula/sparkline-driven). Bot appends, never overwrites Daniel's text.
- Planner format = Daily Planner 1.0 PDF, digitized; "Ministry Flow" title/logo dropped → app is titled **War Room**. Rating % and Hours are computed from ticks, never hand-entered.
- Evening sync 19:00 + auto-rollover of unfinished items (⟳, oldest eats the 04:00 block when chronic).

**Key IDs/paths:**
- War Map 2026 sheet ID: `1zXZmuL8B55lXjrKfQhQt1Tc-tiGujkiKPAk2XS0-jx8`
- Workspace: `/Users/danieldanut/Agentic Workspace` (=`$WS` below)
- Server port: `8787`. App secret: generated in Task 3, stored in `Planning/app-data/secret.txt`.
- Timezone Europe/London. Routine anchors: breakfast 09:00, gym 10:00, dinner 18:00, devotional 18:45, sleep 19:45–03:45.
- Daily Planner 1.0 reference: `.firecrawl/daily-planner-1.0.md` (parsed from Daniel's PDF).

---

## File Structure

```
Planning/
├── goals.yaml                      ← objectives, quotas, ranking, time rules (Task 1)
├── Daily/
│   └── YYYY-MM-DD.json             ← one state file per day — THE source of truth
├── prompts/
│   ├── morning_build.md            ← 03:30 headless run (Task 8)
│   ├── evening_sync.md             ← 19:00 headless run (Task 10)
│   └── weekly_review.md            ← Sun 18:30 run (Task 13)
├── app-data/
│   ├── vapid.json                  ← push keys (Task 5)
│   ├── secret.txt                  ← shared app secret (Task 3)
│   └── subscriptions.json          ← push subscriptions (Task 5)
└── logs/

warroom-app/                        ← the PWA (NEW top-level)
├── package.json
├── server.js                       ← Express + state + push scheduler
└── public/
    ├── index.html                  ← Daily Planner 1.0 layout
    ├── app.js
    ├── style.css
    ├── manifest.json
    ├── sw.js                       ← service worker: push + notification actions
    └── icon-192.png / icon-512.png

scripts/warroom/
├── morning_build.sh  evening_sync.sh  weekly_review.sh   ← claude -p runners
├── open_plan.sh                    ← 4:00 display pop (Chrome app window)
├── alert.sh                        ← Telegram
├── notes_mirror.scpt               ← Apple Notes write-only mirror
└── launchd/                        ← versioned copies of the plists

~/Library/LaunchAgents/
├── com.warroom.server.plist        ← KeepAlive node server
├── com.warroom.morning.plist       ← 03:30
├── com.warroom.display.plist       ← 04:00
├── com.warroom.evening.plist       ← 19:00
└── com.warroom.weekly.plist        ← Sun 18:30
```

## Day JSON schema (used by server, frontend, and both Claude prompts)

```json
{
  "date": "2026-06-12",
  "focus": "Outreach sender v0 fires a dry-run batch",
  "priorities": [
    {"id": "p1", "text": "Build DM sender skeleton + 1 dry-run batch", "done": null, "actual": null, "carryFrom": null},
    {"id": "p2", "text": "02_codex_mobile: Stage 4b cut edit pass", "done": null, "actual": null, "carryFrom": null},
    {"id": "p3", "text": "Post 1 organic short", "done": null, "actual": null, "carryFrom": "2026-06-11"}
  ],
  "slots": [
    {"time": "04:00", "taskId": "p1", "done": false},
    {"time": "04:30", "taskId": "p1", "done": false},
    {"time": "09:00", "routine": "Breakfast"},
    {"time": "13:00", "taskId": "p3", "done": false}
  ],
  "callsConducted": null, "callsBooked": null,
  "improve": "",
  "score": {"rating": null, "hours": null, "output": ""},
  "conflicts": ["Call with Ana 14:00 collides with planned edit block — block moved to 15:00"]
}
```

Rules: `slots` covers 04:00–19:30 in 30-min steps; work slots have `taskId`+`done`; routine slots have `routine` only (not tickable, excluded from Rating). **Rating % = done work slots ÷ total work slots. Hours = done work slots × 0.5.** Task `done` flips true when a check-in answers ✅ or all its slots are ticked; `actual` stores a number answer ("sent 40 not 80").

---

### Task 1: Setup session — June objectives into goals.yaml + War Map

**Interactive** (main session, AskUserQuestion — not a subagent).

**Files:**
- Create: `Planning/goals.yaml`
- Modify: War Map 2026 `Jun` tab (google-workspace MCP)

- [ ] **Step 1: Create folders**

```bash
mkdir -p "$WS/Planning/Daily" "$WS/Planning/prompts" "$WS/Planning/app-data" "$WS/Planning/logs" "$WS/scripts/warroom/launchd" "$WS/warroom-app/public"
```

- [ ] **Step 2: Interview Daniel (one AskUserQuestion at a time)**

1. June's 2–4 objectives? (recommend: ① outreach system v1 sends first automated batch, ② N videos published, ③ Skool funnel live)
2. Weekly video quota? (recommend: 2)
3. Outreach system June milestone? (recommend: first automated DM batch before June 30)
4. Daily organic post quota? (recommend: 1)

- [ ] **Step 3: Write `Planning/goals.yaml`**

```yaml
# Machine-readable mirror of War Map 2026 — morning build reads this first.
warmap_sheet_id: 1zXZmuL8B55lXjrKfQhQt1Tc-tiGujkiKPAk2XS0-jx8
user_google_email: daniel@ministryflow.co
timezone: Europe/London

year_goals:
  - 50 paying clients by end of 2026
  - First 10k/mo
  - 5-10 appointments/day consistently
  - Consistent organic content (1+ post/day)

month:
  id: 2026-06
  objectives: []        # ← from Step 2
  quotas: {}            # ← from Step 2, e.g. {videos_per_week: 2, posts_per_day: 1}

priority_ranking:
  - outreach_system_build    # building the automated DM machine (NOT manual DMs)
  - youtube_pipeline         # next stage action for the active project(s)
  - distribution
  - skool_community
  - admin

time_rules:
  deep_work: "04:00-08:00"        # creative + build only; no sends, no admin
  outreach_sends_after: "13:00"   # US avatar awake
  work_end: "18:00"
calendar_rules:
  never_touch: "events with attendees other than Daniel"
  editable: "solo blocks; meals/gym may shift max ±30min"
  conflicts_go_to: "conflicts array of the day JSON"
```

- [ ] **Step 4: Write June objectives into War Map `Jun` tab** — `read_sheet_values` to find the `Main Objectives:` cell, `modify_sheet_values` to fill the cells beneath, matching the Jan tab's layout.

- [ ] **Step 5: Verify** — re-read `Jun` tab; validate YAML: `python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" "$WS/Planning/goals.yaml"`

- [ ] **Step 6: Commit**

```bash
cd "$WS" && git add Planning/goals.yaml && git commit -m "feat(warroom): goals.yaml — June objectives + planning rules"
```

---

### Task 2: CLAUDE.md registration + .gitignore

**Files:**
- Modify: `.claude/CLAUDE.md`
- Modify: `.gitignore`

- [ ] **Step 1: Append to `.claude/CLAUDE.md`** (after "Shared Tools (MCP)"; keep lean):

```markdown
## War Room (daily planning)

Source of truth: `Planning/Daily/YYYY-MM-DD.json`, served by `warroom-app/` (PWA, port 8787, Tailscale Funnel for phone).
Automation: launchd — 03:30 build · 04:00 screen-pop · 19:00 evening sync · Sun 18:30 weekly review (`scripts/warroom/`).
Rules: ranking in `Planning/goals.yaml`; ticks ONLY in the app (Apple Notes is a read-only mirror); never edit calendar events with attendees; outreach sends ≥13:00 UK; bot appends to War Map after " | ", never overwrites.
```

- [ ] **Step 2: Append to `.gitignore`:**

```
Planning/logs/
Planning/app-data/
warroom-app/node_modules/
.firecrawl/
```

- [ ] **Step 3: Commit**

```bash
cd "$WS" && git add .claude/CLAUDE.md .gitignore && git commit -m "feat(warroom): register War Room system in CLAUDE.md"
```

---

### Task 3: Server — state + tick API

**Files:**
- Create: `warroom-app/package.json`, `warroom-app/server.js`

- [ ] **Step 1: Scaffold**

```bash
cd "$WS/warroom-app" && cat > package.json <<'EOF'
{ "name": "warroom", "private": true, "main": "server.js",
  "dependencies": { "express": "^4.19.0", "web-push": "^3.6.7" } }
EOF
npm install
openssl rand -hex 16 > "$WS/Planning/app-data/secret.txt"
echo '[]' > "$WS/Planning/app-data/subscriptions.json"
```

- [ ] **Step 2: Write `warroom-app/server.js`**

```js
const express = require('express');
const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');

const WS = '/Users/danieldanut/Agentic Workspace';
const DAILY = path.join(WS, 'Planning/Daily');
const APPDATA = path.join(WS, 'Planning/app-data');
const SECRET = fs.readFileSync(path.join(APPDATA, 'secret.txt'), 'utf8').trim();
const PORT = 8787;

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// --- auth: ?key= once, then x-warroom-key header (frontend stores it) ---
app.use('/api', (req, res, next) => {
  const k = req.headers['x-warroom-key'] || req.query.key;
  if (k !== SECRET) return res.status(401).json({ error: 'bad key' });
  next();
});

const todayStr = () =>
  new Date().toLocaleDateString('en-CA', { timeZone: 'Europe/London' });
const dayFile = (d) => path.join(DAILY, `${d}.json`);
const loadDay = (d) =>
  fs.existsSync(dayFile(d)) ? JSON.parse(fs.readFileSync(dayFile(d), 'utf8')) : null;

function computeScore(day) {
  const work = day.slots.filter((s) => s.taskId);
  const done = work.filter((s) => s.done);
  day.score = day.score || {};
  day.score.rating = work.length ? Math.round((done.length / work.length) * 100) : 0;
  day.score.hours = done.length * 0.5;
  return day;
}

function saveDay(day) {
  computeScore(day);
  fs.writeFileSync(dayFile(day.date), JSON.stringify(day, null, 2));
  mirrorToNotes(day.date); // fire-and-forget
}

function mirrorToNotes(date) {
  execFile('/usr/bin/osascript',
    [path.join(WS, 'scripts/warroom/notes_mirror.scpt'), dayFile(date)],
    (err) => { if (err) console.error('notes mirror:', err.message); });
}

app.get('/api/day/:date', (req, res) => {
  const day = loadDay(req.params.date === 'today' ? todayStr() : req.params.date);
  if (!day) return res.status(404).json({ error: 'no plan for that day' });
  res.json(day);
});

// tick a slot; cascades: task.done=true when all its slots done
app.post('/api/tick', (req, res) => {
  const { date, time, taskId, done, actual } = req.body;
  const day = loadDay(date || todayStr());
  if (!day) return res.status(404).json({ error: 'no plan' });
  if (time) {
    const slot = day.slots.find((s) => s.time === time && s.taskId);
    if (!slot) return res.status(400).json({ error: 'no work slot at ' + time });
    slot.done = !!done;
  }
  if (taskId) {
    const t = day.priorities.find((p) => p.id === taskId);
    if (t) {
      t.done = !!done;
      if (actual !== undefined) t.actual = actual;
      day.slots.filter((s) => s.taskId === taskId).forEach((s) => (s.done = !!done));
    }
  }
  day.priorities.forEach((p) => {
    const ss = day.slots.filter((s) => s.taskId === p.id);
    if (ss.length && ss.every((s) => s.done) && p.done === null) p.done = true;
  });
  saveDay(day);
  res.json(day);
});

// calls tally / improve text / focus etc.
app.post('/api/meta', (req, res) => {
  const day = loadDay(req.body.date || todayStr());
  if (!day) return res.status(404).json({ error: 'no plan' });
  ['callsConducted', 'callsBooked', 'improve'].forEach((k) => {
    if (req.body[k] !== undefined) day[k] = req.body[k];
  });
  saveDay(day);
  res.json(day);
});

// history for dashboards/weekly review
app.get('/api/history', (req, res) => {
  const files = fs.readdirSync(DAILY).filter((f) => f.endsWith('.json')).sort();
  res.json(files.slice(-31).map((f) => JSON.parse(fs.readFileSync(path.join(DAILY, f), 'utf8'))));
});

require('./push')(app, { loadDay, saveDay, todayStr, APPDATA, SECRET }); // Task 5

app.listen(PORT, () => console.log(`War Room on :${PORT}`));
```

- [ ] **Step 3: Create a fixture day + test the API**

```bash
cat > "$WS/Planning/Daily/$(date +%F).json" <<'EOF'
{ "date": "REPLACE", "focus": "API smoke test",
  "priorities": [{"id":"p1","text":"Test task","done":null,"actual":null,"carryFrom":null}],
  "slots": [{"time":"04:00","taskId":"p1","done":false},{"time":"09:00","routine":"Breakfast"}],
  "callsConducted": null, "callsBooked": null, "improve": "",
  "score": {"rating":null,"hours":null,"output":""}, "conflicts": [] }
EOF
sed -i '' "s/REPLACE/$(date +%F)/" "$WS/Planning/Daily/$(date +%F).json"
# push.js does not exist yet — stub it so the server starts:
echo 'module.exports = () => {};' > "$WS/warroom-app/push.js"
node "$WS/warroom-app/server.js" &
sleep 1
KEY=$(cat "$WS/Planning/app-data/secret.txt")
curl -s -H "x-warroom-key: $KEY" localhost:8787/api/day/today | python3 -m json.tool
curl -s -H "x-warroom-key: $KEY" -H 'Content-Type: application/json' \
  -d '{"time":"04:00","done":true}' localhost:8787/api/tick | python3 -m json.tool
kill %1
```

Expected: second call returns `"rating": 100, "hours": 0.5` and `p1.done: true` (its only slot is done). The `notes mirror` error in the server log is expected until Task 7.

- [ ] **Step 4: Commit**

```bash
cd "$WS" && git add warroom-app/package.json warroom-app/server.js warroom-app/push.js && git commit -m "feat(warroom): server — day state + tick API"
```

---

### Task 4: Frontend — Daily Planner 1.0, digitized

**Files:**
- Create: `warroom-app/public/index.html`, `public/style.css`, `public/app.js`, `public/manifest.json`, icons

- [ ] **Step 1: Write `public/index.html`**

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>War Room</title>
<link rel="manifest" href="manifest.json">
<link rel="stylesheet" href="style.css">
<link rel="apple-touch-icon" href="icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
</head>
<body>
<header>
  <h1>⚔️ WAR ROOM</h1>
  <div id="date"></div>
  <div class="scorebar">
    <span>Rating <b id="rating">–%</b></span>
    <span>Hours <b id="hours">–</b></span>
  </div>
  <div class="focus">Focus: <span id="focus"></span></div>
  <div class="output">Output: <span id="output">—</span></div>
</header>

<section id="priorities">
  <h2>Priority Tasks</h2>
  <ul id="prio-list"></ul>
</section>

<section id="schedule">
  <h2>Schedule</h2>
  <div id="grid"></div>
</section>

<section id="meta">
  <label>Calls Conducted / Booked:
    <input id="callsC" type="number" min="0" inputmode="numeric"> /
    <input id="callsB" type="number" min="0" inputmode="numeric">
  </label>
  <label>How can I improve?
    <textarea id="improve" rows="2"></textarea>
  </label>
</section>

<footer>
  <ol>
    <li>No skipping organic posts</li>
    <li>No sugar, no eating outside the meal plan</li>
    <li>No YouTube / Hormozi / courses / random research</li>
    <li>No distractions 4–8am — do not <i>not</i> work on the priority</li>
    <li>No task switching / incompletion (90%+)</li>
  </ol>
  <button id="enable-push">Enable check-ins 🔔</button>
</footer>
<script src="app.js"></script>
</body>
</html>
```

- [ ] **Step 2: Write `public/style.css`** — dark, glanceable at 4am, two-column grid on wide screens:

```css
:root { --bg:#0d1117; --card:#161b22; --line:#30363d; --fg:#e6edf3; --dim:#8b949e; --gold:#d4a72c; --green:#3fb950; }
* { box-sizing: border-box; margin: 0; }
body { background: var(--bg); color: var(--fg); font: 16px/1.45 -apple-system, sans-serif; padding: 12px; max-width: 900px; margin: auto; }
header { text-align: center; padding: 8px 0 14px; }
h1 { font-size: 26px; letter-spacing: 4px; color: var(--gold); }
#date { color: var(--dim); margin: 2px 0 8px; }
.scorebar { display: flex; gap: 24px; justify-content: center; font-size: 18px; }
.scorebar b { color: var(--green); }
.focus, .output { margin-top: 6px; font-size: 15px; color: var(--dim); }
.focus span { color: var(--fg); font-weight: 600; }
h2 { font-size: 13px; text-transform: uppercase; letter-spacing: 2px; color: var(--dim); margin: 18px 0 8px; }
#prio-list { list-style: none; }
#prio-list li { background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; margin-bottom: 6px; display: flex; gap: 10px; align-items: center; }
#prio-list li.done { opacity: .55; text-decoration: line-through; }
#prio-list .carry { color: var(--gold); font-size: 12px; }
#grid { display: grid; grid-template-columns: 1fr; gap: 4px; }
@media (min-width: 700px) { #grid { grid-template-columns: 1fr 1fr; grid-auto-flow: column; grid-template-rows: repeat(16, auto); } }
.slot { display: flex; gap: 10px; align-items: center; padding: 7px 10px; border-radius: 6px; border: 1px solid transparent; }
.slot.work { background: var(--card); border-color: var(--line); cursor: pointer; }
.slot.work.done { opacity: .5; text-decoration: line-through; }
.slot.routine { color: var(--dim); font-size: 14px; }
.slot time { width: 52px; color: var(--dim); font-variant-numeric: tabular-nums; }
.tick { width: 20px; height: 20px; border: 2px solid var(--dim); border-radius: 5px; flex: none; }
.done .tick { background: var(--green); border-color: var(--green); }
#meta label { display: block; margin: 10px 0; color: var(--dim); }
input, textarea { background: var(--card); color: var(--fg); border: 1px solid var(--line); border-radius: 6px; padding: 6px 8px; font: inherit; width: 64px; }
textarea { width: 100%; }
footer { margin: 22px 0 40px; color: var(--dim); font-size: 13px; }
footer ol { padding-left: 18px; }
#enable-push { margin-top: 14px; background: var(--gold); color: #000; border: 0; border-radius: 8px; padding: 10px 16px; font-weight: 700; }
```

- [ ] **Step 3: Write `public/app.js`**

```js
const KEY = localStorage.warroomKey ||
  (localStorage.warroomKey = new URLSearchParams(location.search).get('key') || '');
const H = { 'x-warroom-key': KEY, 'Content-Type': 'application/json' };
let day = null;

async function api(path, body) {
  const res = await fetch('/api/' + path,
    body ? { method: 'POST', headers: H, body: JSON.stringify(body) } : { headers: H });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

function render() {
  document.getElementById('date').textContent = new Date(day.date + 'T12:00')
    .toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' });
  document.getElementById('rating').textContent = (day.score.rating ?? 0) + '%';
  document.getElementById('hours').textContent = day.score.hours ?? 0;
  document.getElementById('focus').textContent = day.focus;
  document.getElementById('output').textContent = day.score.output || '—';

  const ul = document.getElementById('prio-list');
  ul.innerHTML = '';
  day.priorities.forEach((p) => {
    const li = document.createElement('li');
    li.className = p.done ? 'done' : '';
    li.innerHTML = `<span class="tick"></span><span>➢ ${p.text}` +
      (p.actual != null ? ` <b>(${p.actual})</b>` : '') + '</span>' +
      (p.carryFrom ? `<span class="carry">⟳ ${p.carryFrom}</span>` : '');
    li.onclick = () => api('tick', { date: day.date, taskId: p.id, done: !p.done }).then(set);
    ul.appendChild(li);
  });

  const grid = document.getElementById('grid');
  grid.innerHTML = '';
  day.slots.forEach((s) => {
    const div = document.createElement('div');
    if (s.taskId) {
      const t = day.priorities.find((p) => p.id === s.taskId);
      div.className = 'slot work' + (s.done ? ' done' : '');
      div.innerHTML = `<time>${s.time}</time><span class="tick"></span><span>${t ? t.text : s.taskId}</span>`;
      div.onclick = () => api('tick', { date: day.date, time: s.time, done: !s.done }).then(set);
    } else {
      div.className = 'slot routine';
      div.innerHTML = `<time>${s.time}</time><span>${s.routine || '—'}</span>`;
    }
    grid.appendChild(div);
  });

  document.getElementById('callsC').value = day.callsConducted ?? '';
  document.getElementById('callsB').value = day.callsBooked ?? '';
  document.getElementById('improve').value = day.improve || '';
}

function set(d) { day = d; render(); }

let metaTimer;
function metaChanged() {
  clearTimeout(metaTimer);
  metaTimer = setTimeout(() => api('meta', {
    date: day.date,
    callsConducted: +document.getElementById('callsC').value || null,
    callsBooked: +document.getElementById('callsB').value || null,
    improve: document.getElementById('improve').value,
  }).then(set), 600);
}
['callsC', 'callsB', 'improve'].forEach((id) =>
  document.getElementById(id).addEventListener('input', metaChanged));

document.getElementById('enable-push').onclick = async () => {
  const reg = await navigator.serviceWorker.ready;
  const { publicKey } = await api('vapid-public-key');
  const sub = await reg.pushManager.subscribe({
    userVisibleOnly: true, applicationServerKey: publicKey });
  await api('subscribe', sub.toJSON());
  alert('Check-ins enabled on this device ✅');
};

navigator.serviceWorker.register('sw.js');
api('day/today').then(set).catch((e) => {
  document.body.innerHTML = `<h1 style="padding:40px">No plan for today yet.<br><small>${e.message}</small></h1>`;
});
setInterval(() => api('day/today').then(set).catch(() => {}), 60_000); // cross-device refresh
```

- [ ] **Step 4: Write `public/manifest.json` + icons**

```json
{ "name": "War Room", "short_name": "War Room", "start_url": "/",
  "display": "standalone", "background_color": "#0d1117", "theme_color": "#0d1117",
  "icons": [ {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
             {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"} ] }
```

Icons: generate a simple gold ⚔️ on dark tile:

```bash
python3 - <<'EOF'
# zero-dep PNG: solid dark tile (placeholder until a designed icon exists)
import struct, zlib
def png(size, path, rgb=(13,17,23)):
    row = b'\x00' + bytes(rgb) * size
    raw = row * size
    def chunk(t, d): c = t + d; return struct.pack('>I', len(d)) + c + struct.pack('>I', zlib.crc32(c))
    ihdr = struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0)
    open(path, 'wb').write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b''))
png(192, 'public/icon-192.png'); png(512, 'public/icon-512.png')
EOF
```

(Upgrade later via Higgsfield if Daniel wants a real icon — out of scope.)

- [ ] **Step 5: Write a minimal `public/sw.js`** (push handlers land in Task 5; cache nothing — always-online tool):

```js
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => e.waitUntil(clients.claim()));
```

- [ ] **Step 6: Test in browser**

```bash
node "$WS/warroom-app/server.js" &
sleep 1
KEY=$(cat "$WS/Planning/app-data/secret.txt")
open "http://localhost:8787/?key=$KEY"
```

Expected: dark planner page — header with Rating/Hours/Focus, Priority Tasks, half-hour grid, Calls inputs, non-negotiables. Clicking the 04:00 slot toggles it and Rating updates live. Refresh persists state. Then `kill %1`.

- [ ] **Step 7: Commit**

```bash
cd "$WS" && git add warroom-app/public && git commit -m "feat(warroom): PWA frontend — Daily Planner 1.0 digitized"
```

---

### Task 5: Push check-ins (end-of-block + 18:30 sweep)

**Files:**
- Create: `warroom-app/push.js` (replaces the stub)
- Modify: `warroom-app/public/sw.js`

- [ ] **Step 1: Generate VAPID keys**

```bash
cd "$WS/warroom-app" && npx web-push generate-vapid-keys --json > "$WS/Planning/app-data/vapid.json"
```

- [ ] **Step 2: Write `warroom-app/push.js`**

```js
const webpush = require('web-push');
const fs = require('fs');
const path = require('path');

module.exports = (app, { loadDay, saveDay, todayStr, APPDATA, SECRET }) => {
  const vapid = JSON.parse(fs.readFileSync(path.join(APPDATA, 'vapid.json'), 'utf8'));
  webpush.setVapidDetails('mailto:daniel@ministryflow.co', vapid.publicKey, vapid.privateKey);
  const SUBS = path.join(APPDATA, 'subscriptions.json');
  const subs = () => JSON.parse(fs.readFileSync(SUBS, 'utf8'));

  app.get('/api/vapid-public-key', (_q, res) => res.json({ publicKey: vapid.publicKey }));
  app.post('/api/subscribe', (req, res) => {
    const all = subs().filter((s) => s.endpoint !== req.body.endpoint);
    all.push(req.body);
    fs.writeFileSync(SUBS, JSON.stringify(all, null, 2));
    res.json({ ok: all.length });
  });

  async function send(payload) {
    for (const s of subs()) {
      try { await webpush.sendNotification(s, JSON.stringify(payload)); }
      catch (e) { if (e.statusCode === 410) { // expired sub — prune
        fs.writeFileSync(SUBS, JSON.stringify(subs().filter((x) => x.endpoint !== s.endpoint), null, 2));
      } }
    }
  }

  const timers = [];
  function arm() {
    timers.splice(0).forEach(clearTimeout);
    const day = loadDay(todayStr());
    if (!day) return;
    const now = new Date();
    const at = (hhmm, fn) => {
      const [h, m] = hhmm.split(':').map(Number);
      const t = new Date(now); t.setHours(h, m, 0, 0);
      if (t > now) timers.push(setTimeout(fn, t - now));
    };
    // end-of-block check-ins: a block ends where the next slot has a different taskId
    const work = day.slots.filter((s) => s.taskId);
    work.forEach((s, i) => {
      const next = work[i + 1];
      if (!next || next.taskId !== s.taskId) {
        const [h, m] = s.time.split(':').map(Number);
        const end = `${String(m === 30 ? h + 1 : h).padStart(2, '0')}:${m === 30 ? '00' : '30'}`;
        const task = day.priorities.find((p) => p.id === s.taskId);
        at(end, () => {
          const d = loadDay(todayStr());
          const t = d && d.priorities.find((p) => p.id === s.taskId);
          if (t && t.done === null) send({ title: 'Block done?', body: t.text, taskId: t.id, date: d.date });
        });
      }
    });
    // 18:30 day-close sweep
    at('18:30', () => {
      const d = loadDay(todayStr());
      if (!d) return;
      d.priorities.filter((p) => p.done === null)
        .forEach((p) => send({ title: 'Day close — done?', body: p.text, taskId: p.id, date: d.date }));
    });
  }
  arm();
  setInterval(arm, 30 * 60 * 1000); // re-arm half-hourly (cheap; survives plan rewrites + sleep/wake)
  app.post('/api/rearm', (_q, res) => { arm(); res.json({ ok: true }); });
};
```

- [ ] **Step 3: Replace `public/sw.js`** with push + action handling:

```js
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => e.waitUntil(clients.claim()));

self.addEventListener('push', (e) => {
  const d = e.data.json();
  e.waitUntil(self.registration.showNotification(d.title, {
    body: d.body, tag: d.taskId, data: d,
    actions: [{ action: 'done', title: '✅ Done' }, { action: 'miss', title: '❌ Not yet' }],
  }));
});

self.addEventListener('notificationclick', (e) => {
  e.notification.close();
  const d = e.notification.data;
  if (e.action === 'done' || e.action === 'miss') {
    e.waitUntil((async () => {
      const cache = await caches.open('warroom-key');
      const keyRes = await cache.match('key');
      const key = keyRes ? await keyRes.text() : '';
      await fetch('/api/tick', {
        method: 'POST',
        headers: { 'x-warroom-key': key, 'Content-Type': 'application/json' },
        body: JSON.stringify({ date: d.date, taskId: d.taskId, done: e.action === 'done' }),
      });
    })());
  } else {
    e.waitUntil(clients.openWindow('/')); // tap body → open app (enter actual numbers there)
  }
});
```

And in `public/app.js`, persist the key where the service worker can read it — append after the `KEY` line:

```js
caches.open('warroom-key').then((c) => c.put('key', new Response(KEY)));
```

- [ ] **Step 4: Test push on the Mac**

```bash
node "$WS/warroom-app/server.js" &
sleep 1
open "http://localhost:8787/?key=$(cat "$WS/Planning/app-data/secret.txt")"
```

In Chrome: click "Enable check-ins 🔔", allow. Then force a check-in by editing today's JSON: set a work slot block ending 2 minutes from now (e.g. slot time = previous half-hour), `curl -X POST -H "x-warroom-key: $KEY" localhost:8787/api/rearm`, wait for the notification, click **✅ Done**, then `curl .../api/day/today` and confirm the task flipped `done: true`. Kill the server.

- [ ] **Step 5: Commit**

```bash
cd "$WS" && git add warroom-app/push.js warroom-app/public/sw.js warroom-app/public/app.js && git commit -m "feat(warroom): web-push check-ins — end-of-block + day-close sweep"
```

---

### Task 6: Tailscale Funnel + iPhone install (Daniel-assisted)

- [ ] **Step 1: Install + login (Daniel clicks the auth link)**

```bash
brew install --cask tailscale && open -a Tailscale   # Daniel: log in (Google account is fine)
```

- [ ] **Step 2: Funnel the app**

```bash
tailscale funnel --bg 8787
tailscale funnel status   # note the https://<machine>.<tailnet>.ts.net URL
```

- [ ] **Step 3: iPhone install (Daniel, ~2 min):** Safari → `https://<funnel-url>/?key=<secret>` → Share → **Add to Home Screen** → open the installed app → tap "Enable check-ins 🔔" → Allow. (Push only works from the installed app, not the Safari tab — iOS rule.)

- [ ] **Step 4: Verify cross-device:** tick a slot on the iPhone; within 60s the Mac browser shows it ticked (the 60s poll). Trigger a test check-in as in Task 5 Step 4 and confirm it lands on the iPhone lock screen.

---

### Task 7: Apple Notes mirror (write-only)

**Files:**
- Create: `scripts/warroom/notes_mirror.scpt` (compiled from AppleScript source)

- [ ] **Step 1: Write and compile the mirror script**

```bash
cat > /tmp/notes_mirror.applescript <<'EOF'
on run argv
  set jsonPath to item 1 of argv
  set md to do shell script "/usr/bin/python3 -c \"
import json,sys
d=json.load(open(sys.argv[1]))
done=lambda b:'✅' if b else ('⬜' if b is None else '❌')
L=['<h1>⚔️ War Room — '+d['date']+'</h1>']
L.append('<p><b>Focus:</b> '+d.get('focus','')+'</p>')
s=d.get('score') or {}
L.append('<p>Rating '+str(s.get('rating') or 0)+'% · '+str(s.get('hours') or 0)+'h</p>')
L.append('<h2>Priorities</h2><ul>')
for p in d['priorities']:
    L.append('<li>'+done(p['done'])+' '+p['text']+(' ('+str(p['actual'])+')' if p.get('actual') is not None else '')+'</li>')
L.append('</ul><h2>Schedule</h2><ul>')
ts={p['id']:p['text'] for p in d['priorities']}
for sl in d['slots']:
    if sl.get('taskId'): L.append('<li>'+sl['time']+' '+done(sl.get('done'))+' '+ts.get(sl['taskId'],'')+'</li>')
    elif sl.get('routine'): L.append('<li>'+sl['time']+' · '+sl['routine']+'</li>')
L.append('</ul><p><i>Read-only mirror — tick in the War Room app.</i></p>')
print(''.join(L))
\" " & quoted form of jsonPath
  tell application "Notes"
    if not (exists folder "War Room") then make new folder with properties {name:"War Room"}
    tell folder "War Room"
      if exists note "War Room — Today" then
        set body of note "War Room — Today" to md
      else
        make new note with properties {name:"War Room — Today", body:md}
      end if
    end tell
  end tell
end run
EOF
osacompile -o "$WS/scripts/warroom/notes_mirror.scpt" /tmp/notes_mirror.applescript
```

- [ ] **Step 2: Test directly, then via the server**

```bash
osascript "$WS/scripts/warroom/notes_mirror.scpt" "$WS/Planning/Daily/$(date +%F).json"
```

Expected: Notes app has folder "War Room" → note "War Room — Today" with the day's plan. First run triggers a macOS automation consent dialog ("Terminal wants to control Notes") — approve; when run from the launchd server the consenting binary is `node` (approve once when prompted). Then tick a slot in the app and confirm the note updates within a second.

- [ ] **Step 3: Commit**

```bash
cd "$WS" && git add scripts/warroom/notes_mirror.scpt && git commit -m "feat(warroom): Apple Notes read-only mirror"
```

---

### Task 8: Morning build — prompt + runner + alert

**Files:**
- Create: `Planning/prompts/morning_build.md`, `scripts/warroom/morning_build.sh`, `scripts/warroom/alert.sh`

- [ ] **Step 1: Write `scripts/warroom/alert.sh`**

```bash
#!/bin/zsh
# Telegram alert. Usage: alert.sh "message"
set -uo pipefail
source "$HOME/.claude/.env" 2>/dev/null || true
MSG="${1:-War Room alert (no message)}"
if [[ -n "${TELEGRAM_BOT_TOKEN:-}" && -n "${TELEGRAM_CHAT_ID:-}" ]]; then
  curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d chat_id="${TELEGRAM_CHAT_ID}" -d text="⚔️ ${MSG}" >/dev/null
else
  echo "alert.sh: TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID missing; msg was: ${MSG}" >&2
fi
```

If `TELEGRAM_CHAT_ID` is missing from `~/.claude/.env`: Daniel messages the bot once, then `curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates" | python3 -c "import json,sys; print(json.load(sys.stdin)['result'][-1]['message']['chat']['id'])"` and append `TELEGRAM_CHAT_ID=<id>`.

- [ ] **Step 2: Write `Planning/prompts/morning_build.md`** — the system's brain:

```markdown
You are the War Room morning builder running headless at 03:30 in
/Users/danieldanut/Agentic Workspace. Do not ask questions. Today = current
date Europe/London. Google MCP calls: user_google_email=daniel@ministryflow.co.

## Gather
1. Read Planning/goals.yaml. If month.id != current month: write a minimal
   day JSON whose only priority is "Run month-rollover setup session with
   Claude", run scripts/warroom/alert.sh "War Room: month rollover needed",
   and stop.
2. Read yesterday's Planning/Daily/<yesterday>.json. Priorities with
   done != true are carry-overs (keep original carryFrom date, or set it to
   yesterday). Read yesterday's "improve" text — apply it to today's design.
3. Read today's calendar 00:00–23:59 (google-workspace get_events). Events
   with attendees other than Daniel are UNTOUCHABLE.
4. Read the War Map month tab (sheet id in goals.yaml) for objectives and
   anything Daniel typed.
5. Workspace state: `git log --oneline -10` and `ls Youtube/Output/*/` —
   active project_id and its next incomplete stage = the pipeline action.

## Decide
- Ranking from goals.yaml priority_ranking. 04:00–08:00 = deep work ONLY
  (outreach_system_build / youtube_pipeline creative). Outreach sends ≥13:00.
- ≤4 priorities (p1..p4), each with a concrete number in its text
  ("draft sender skeleton + 1 dry-run batch", "Stage 4b: cut full pass on
  <project_id>"). If carry-overs ≥3, the oldest becomes p1 at 04:00.
- Build the slots array 04:00–19:30 in 30-min steps: work slots
  {time, taskId, done:false}; routine slots {time, routine} for breakfast
  09:00, gym 10:00, dinner 18:00, devotional 18:45, and any calendar events;
  unassigned slots {time} bare.

## Write
1. Planning/Daily/<today>.json — EXACTLY the schema in
   docs/superpowers/plans/2026-06-11-war-room-daily-planning.md (date, focus,
   priorities, slots, callsConducted:null, callsBooked:null, improve:"",
   score:{rating:null,hours:null,output:""}, conflicts).
2. Re-arm check-ins: curl -s -X POST -H "x-warroom-key: $(cat
   'Planning/app-data/secret.txt')" localhost:8787/api/rearm
3. Calendar audit: create/move solo events so the calendar mirrors today's
   work slots (summary "⚔️ <task>", colorId 9). Never edit attendee events —
   collisions go into the JSON conflicts array and your block moves instead.
4. War Map month tab: in the cell under today's day number, append
   " | <n> tasks · <p1 short name>" (append after " | " if non-empty; never
   overwrite Daniel's text).

## Output contract
Final message: "PLAN <today> OK: <n> priorities, <m> carry-overs, <k>
calendar edits" — or "FAILED: <why>".
```

- [ ] **Step 3: Write `scripts/warroom/morning_build.sh`**

```bash
#!/bin/zsh
set -uo pipefail
WS="/Users/danieldanut/Agentic Workspace"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
LOG="$WS/Planning/logs/morning_$(date +%F).log"
cd "$WS"
{
  echo "=== morning build $(date) ==="
  claude -p "$(cat "$WS/Planning/prompts/morning_build.md")" \
    --model sonnet --permission-mode bypassPermissions --max-turns 100
} >> "$LOG" 2>&1
RC=$?
if [[ $RC -ne 0 || ! -f "$WS/Planning/Daily/$(date +%F).json" ]]; then
  "$WS/scripts/warroom/alert.sh" "Morning build FAILED (rc=$RC). Log: $LOG"
fi
```

- [ ] **Step 4: Test now**

```bash
chmod +x "$WS/scripts/warroom/"*.sh
"$WS/scripts/warroom/alert.sh" "War Room test alert — ignore"   # arrives on Telegram
"$WS/scripts/warroom/morning_build.sh"
python3 -m json.tool "$WS/Planning/Daily/$(date +%F).json"
```

Expected: valid JSON matching the schema; log ends `PLAN <date> OK`; calendar shows ⚔️ blocks; War Map month cell updated; the app (refresh) renders the real plan. **Prompt quality is the acceptance bar** — if priorities are vague or numbers missing, tighten the prompt and re-run.

- [ ] **Step 5: Commit**

```bash
cd "$WS" && git add Planning/prompts/morning_build.md scripts/warroom/morning_build.sh scripts/warroom/alert.sh && git commit -m "feat(warroom): morning build — plan JSON + calendar audit + warmap note"
```

---

### Task 9: 4:00am screen pop

**Files:**
- Create: `scripts/warroom/open_plan.sh`

- [ ] **Step 1: Write it** — Chrome app-window (no tabs/URL bar), work profile:

```bash
#!/bin/zsh
set -uo pipefail
WS="/Users/danieldanut/Agentic Workspace"
caffeinate -u -t 5   # light the display (pmset woke the Mac at 03:23)
if [[ ! -f "$WS/Planning/Daily/$(date +%F).json" ]]; then
  "$WS/scripts/warroom/alert.sh" "4am pop: no plan for today — morning build failed?"
  exit 1
fi
KEY=$(cat "$WS/Planning/app-data/secret.txt")
open -na "Google Chrome" --args --profile-directory="Profile 1" \
  --app="http://localhost:8787/?key=$KEY" --start-fullscreen
```

- [ ] **Step 2: Test:** `chmod +x` + run it → full-screen War Room planner appears in a chromeless window.

- [ ] **Step 3: Commit**

```bash
cd "$WS" && git add scripts/warroom/open_plan.sh && git commit -m "feat(warroom): 4am screen pop — fullscreen app window"
```

---

### Task 10: Evening sync — score, Warmap Data row, recap

**Files:**
- Create: `Planning/prompts/evening_sync.md`, `scripts/warroom/evening_sync.sh`

- [ ] **Step 1: Write `Planning/prompts/evening_sync.md`**

```markdown
You are the War Room evening scorer running headless at 19:00 in
/Users/danieldanut/Agentic Workspace. No questions. Today = current date
Europe/London. Google MCP: user_google_email=daniel@ministryflow.co.

1. Read Planning/Daily/<today>.json. rating/hours are already computed by
   the server. Compose score.output: one line listing what actually shipped
   (done priorities + their actual numbers). Compose/append "improve": keep
   Daniel's own text first if present, then add ONE observation from the data
   (e.g. "p2 missed two days running — protect 06:00 block"). Write the file.
2. War Map (sheet id from Planning/goals.yaml):
   a. Month tab: cell under today's day number — append " | ✔ <rating>% ·
      <hours>h · <top shipped item>" after " | ". Never overwrite Daniel's text.
   b. Data tab: append one row:
      date, rating, hours, priorities_planned, priorities_done,
      carryovers_count, callsConducted, callsBooked, posts_done (1/0: was an
      organic-post priority done), video_stage_progress (active project's
      current stage number, from ls Youtube/Output/*/), dms_sent (sum of
      actual on outreach tasks, else 0), improve (text).
3. Telegram (scripts/warroom/alert.sh): "Day <rating>% · <hours>h focused ·
   shipped: <output> · tomorrow inherits: <unfinished list or 'nothing'>".
Final message: "SYNC <today> OK <rating>%" or "FAILED: <why>".
```

- [ ] **Step 2: Write `scripts/warroom/evening_sync.sh`**

```bash
#!/bin/zsh
set -uo pipefail
WS="/Users/danieldanut/Agentic Workspace"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
LOG="$WS/Planning/logs/evening_$(date +%F).log"
cd "$WS"
{
  echo "=== evening sync $(date) ==="
  claude -p "$(cat "$WS/Planning/prompts/evening_sync.md")" \
    --model sonnet --permission-mode bypassPermissions --max-turns 60
} >> "$LOG" 2>&1
[[ $? -ne 0 ]] && "$WS/scripts/warroom/alert.sh" "Evening sync FAILED. Log: $LOG"
```

- [ ] **Step 3: Test** — tick a few slots in the app first, then run the script. Expected: log ends `SYNC <date> OK`; Telegram recap arrives; Data tab (created in Task 11 — if running before Task 11, the run creates it with a header row) has today's row; month cell shows `✔ n% · …`.

- [ ] **Step 4: Commit**

```bash
cd "$WS" && git add Planning/prompts/evening_sync.md scripts/warroom/evening_sync.sh && git commit -m "feat(warroom): evening sync — score + warmap data row + recap"
```

---

### Task 11: Warmap 2.0 — Data tab + Dashboard

**Files:** War Map 2026 sheet (via google-workspace MCP, main session)

- [ ] **Step 1: Create `Data` tab** (`create_sheet`) with header row:

```
date | rating | hours | planned | done | carryovers | callsConducted | callsBooked | posts | videoStage | dmsSent | improve
```

- [ ] **Step 2: Create `Dashboard 2.0` tab** with formula-driven sections (write via `modify_sheet_values`; SPARKLINE renders without chart objects, so everything is API-writable):

```
A1: ⚔️ WAR ROOM DASHBOARD
A3: Day Rating trend (30d)      B3: =SPARKLINE(QUERY(Data!A2:B,"select B order by A desc limit 30"),{"charttype","column";"max",100})
A4: 7-day avg rating            B4: =ROUND(AVERAGE(QUERY(Data!A2:B,"select B order by A desc limit 7")),0)&"%"
A6: Focused hours (30d)         B6: =SPARKLINE(QUERY(Data!A2:C,"select C order by A desc limit 30"),{"charttype","column"})
A7: Hours this week             B7: =SUMIFS(Data!C:C,Data!A:A,">="&(TODAY()-WEEKDAY(TODAY(),2)+1))
A9: Pipeline                    B9: ="Active project stage: "&IFERROR(INDEX(Data!J:J,MATCH(MAX(Data!A:A),Data!A:A,0)),"–")&" / 9"
A10: Posts streak               B10: =IFERROR(MATCH(0,SORT(Data!I2:I,Data!A2:A,FALSE),0)-1,COUNTA(Data!I2:I))&" days"
A12: Outreach — DMs sent (30d)  B12: =SPARKLINE(QUERY(Data!A2:K,"select K order by A desc limit 30"),{"charttype","column"})
A13: DMs this month / pace      B13: =SUMIFS(Data!K:K,Data!A:A,">="&EOMONTH(TODAY(),-1)+1)&" / "&ROUND(2460/DAY(EOMONTH(TODAY(),0))*DAY(TODAY()),0)
A15: Calls conducted/booked wk  B15: =SUMIFS(Data!G:G,Data!A:A,">="&(TODAY()-7))&" / "&SUMIFS(Data!H:H,Data!A:A,">="&(TODAY()-7))
A17: Carry-over load (slippage) B17: =SPARKLINE(QUERY(Data!A2:F,"select F order by A desc limit 30"),{"charttype","column";"color","red"})
```

Then `format_sheet_range` on A1 (bold, 18pt) and the label column (bold), and conditional formatting on B4 (red <50%, amber 50–75%, green >75%).

- [ ] **Step 3: Verify** — append a fake Data row, open the Dashboard tab in the browser, confirm sparklines render; delete the fake row.

- [ ] **Step 4:** No commit (sheet-side change only). Note the tab names in `Planning/goals.yaml` under a `warmap_tabs: {data: Data, dashboard: Dashboard 2.0}` key and commit that.

---

### Task 12: launchd + pmset + overnight acceptance

**Files:**
- Create: 5 plists in `~/Library/LaunchAgents/` (+ versioned copies in `scripts/warroom/launchd/`)

- [ ] **Step 1: Server daemon `com.warroom.server.plist`**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.warroom.server</string>
  <key>ProgramArguments</key>
  <array>
    <string>/opt/homebrew/bin/node</string>
    <string>/Users/danieldanut/Agentic Workspace/warroom-app/server.js</string>
  </array>
  <key>KeepAlive</key><true/>
  <key>RunAtLoad</key><true/>
  <key>StandardErrorPath</key><string>/Users/danieldanut/Agentic Workspace/Planning/logs/launchd.server.err</string>
</dict>
</plist>
```

(Verify node path first: `which node` — adjust if not Homebrew.)

- [ ] **Step 2: Schedule plists** — same shape, `StartCalendarInterval` + script via `/bin/zsh`:

| Label | Script | When |
|---|---|---|
| com.warroom.morning | morning_build.sh | Hour 3, Minute 30 |
| com.warroom.display | open_plan.sh | Hour 4, Minute 0 |
| com.warroom.evening | evening_sync.sh | Hour 19, Minute 0 |
| com.warroom.weekly | weekly_review.sh | Weekday 0, Hour 18, Minute 30 |

Each: `<key>ProgramArguments</key><array><string>/bin/zsh</string><string>/Users/danieldanut/Agentic Workspace/scripts/warroom/<script></string></array>` and its own `StandardErrorPath` under `Planning/logs/`.

- [ ] **Step 3: Load everything + kickstart test**

```bash
for p in server morning display evening weekly; do
  launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.warroom.$p.plist
done
launchctl list | grep warroom                       # 5 rows
curl -s -o /dev/null -w '%{http_code}\n' localhost:8787   # 200 — server daemon up
launchctl kickstart gui/$(id -u)/com.warroom.display      # planner pops fullscreen
```

- [ ] **Step 4: pmset wake (Daniel runs — sudo)**

```bash
sudo pmset repeat wakeorpoweron MTWRFSU 03:23:00
pmset -g sched   # expect: wakepoweron at 3:23AM every day
```

- [ ] **Step 5: Overnight acceptance (the real test)** — tonight Mac sleeps plugged in; tomorrow verify: ① 4:00 planner fullscreen with a real plan; ② calendar has ⚔️ blocks, "Call with Ana" untouched; ③ check-ins arrive on iPhone at block ends, ✅ from the lock screen ticks the app + Notes mirror + (after 19:00) Warmap; ④ 19:00 sync → Telegram recap + Data row + dashboards move. Fix-forward from `Planning/logs/*` — accepted after one clean 24h cycle.

- [ ] **Step 6: Commit plist copies**

```bash
cp ~/Library/LaunchAgents/com.warroom.*.plist "$WS/scripts/warroom/launchd/"
cd "$WS" && git add scripts/warroom/launchd && git commit -m "feat(warroom): launchd jobs (server, 03:30, 04:00, 19:00, Sun 18:30)"
```

---

### Task 13: Weekly review + month rollover

**Files:**
- Create: `Planning/prompts/weekly_review.md`, `scripts/warroom/weekly_review.sh`

- [ ] **Step 1: Write `Planning/prompts/weekly_review.md`**

```markdown
You are the War Room weekly reviewer running headless Sunday 18:30 in
/Users/danieldanut/Agentic Workspace. Google MCP:
user_google_email=daniel@ministryflow.co.

1. Read the last 7 Planning/Daily/*.json. Compute: avg rating, total focused
   hours, done/planned, chronic carry-overs (same task 3+ days), calls totals.
2. Compare against Planning/goals.yaml quotas (videos: check
   Youtube/Output/7*/ and git log; posts/dms: from the day files).
3. War Map month tab Notes area: one line —
   "Wk <n>: <avg>% · <hours>h · videos <x>/<quota> · <main win> · <main slip>".
4. Telegram: 5-line scoreboard + ONE concrete recommendation for next week.
Final message: "WEEKLY OK" or "FAILED: <why>".
```

- [ ] **Step 2: Write `scripts/warroom/weekly_review.sh`** — same shape as evening_sync.sh with the weekly prompt, log prefix `weekly_`, `--max-turns 50`:

```bash
#!/bin/zsh
set -uo pipefail
WS="/Users/danieldanut/Agentic Workspace"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
LOG="$WS/Planning/logs/weekly_$(date +%F).log"
cd "$WS"
{
  claude -p "$(cat "$WS/Planning/prompts/weekly_review.md")" \
    --model sonnet --permission-mode bypassPermissions --max-turns 50
} >> "$LOG" 2>&1
[[ $? -ne 0 ]] && "$WS/scripts/warroom/alert.sh" "Weekly review FAILED. Log: $LOG"
```

- [ ] **Step 3: Test** — `chmod +x` + run once now (thin data is fine); expect a Telegram scoreboard.

- [ ] **Step 4: Month rollover is already handled** — morning prompt step 1 degrades to a single-task plan + alert on the 1st until Daniel re-runs the Task 1 interview (15 min). No extra code.

- [ ] **Step 5: Commit**

```bash
cd "$WS" && git add Planning/prompts/weekly_review.md scripts/warroom/weekly_review.sh && git commit -m "feat(warroom): weekly review + month rollover guard"
```

---

## Out of scope (explicitly)

- Building the actual LinkedIn DM sender — a *task the system schedules*, not part of this system.
- Editing/emailing other humans about their calendar events.
- Designed app icon (placeholder tile now; Higgsfield later if wanted).
- Astra/Telegram *interactive* plan editing — v2 if the loop proves itself.
- Native iOS app — the PWA covers notifications + home screen; revisit only if iOS push proves unreliable in practice.

## Failure modes designed for

| Failure | Behavior |
|---|---|
| Morning build crashes | No day JSON → 4:00 pop alerts Telegram instead of opening a blank app |
| Mac asleep overnight | pmset wakes 03:23; server daemon resumes; push scheduler re-arms half-hourly |
| Check-in unanswered | Stays unticked; 18:30 sweep re-asks; evening sync scores it missed |
| Notes mirror breaks | Fire-and-forget — never blocks ticks; error logged in server log |
| iPhone offline / abroad | Funnel URL is public HTTPS; push resumes on reconnect; app poll catches up |
| Month not set up | Degraded single-task plan + alert, never a silent skip |
| Daniel edits Warmap by hand | Bot only appends after " \| ", never overwrites |
| Expired push subscription | 410 responses pruned automatically |
| launchd env ≠ shell | PATH exported in every script; per-job `.err` files under Planning/logs/ |
