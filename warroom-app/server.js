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
app.use(express.static(path.join(__dirname, 'public'), {
  setHeaders: (res) => res.setHeader('Cache-Control', 'no-cache'), // always revalidate — stale PWA assets cost more than the bytes
}));

// auth: ?key= once (frontend stores it), then x-warroom-key header
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

// progress model: each priority has progress 0–100 (tick = 100, hold = partial).
// Rating/Hours are pro-rata: 45% of a 4h block contributes 1.8h and 45% of its weight.
function computeScore(day) {
  const slotsOf = {};
  day.slots.forEach((s) => { if (s.taskId) slotsOf[s.taskId] = (slotsOf[s.taskId] || 0) + 1; });
  let weighted = 0, totalSlots = 0, hours = 0;
  day.priorities.forEach((p) => {
    const n = slotsOf[p.id] || 0;
    if (p.progress == null) p.progress = p.done === true ? 100 : 0;
    if (p.progress >= 100) p.done = true;
    totalSlots += n;
    weighted += n * p.progress;
    hours += n * 0.5 * (p.progress / 100);
  });
  day.score = day.score || {};
  day.score.rating = totalSlots ? Math.round(weighted / totalSlots) : 0;
  day.score.hours = Math.round(hours * 10) / 10;
  return day;
}

// sync a task's slots to its progress (visual fill in the timeline)
function syncSlots(day, taskId) {
  const p = day.priorities.find((x) => x.id === taskId);
  if (!p) return;
  const slots = day.slots.filter((s) => s.taskId === taskId);
  const doneCount = Math.round((p.progress / 100) * slots.length);
  slots.forEach((s, i) => { s.done = i < doneCount; });
}

function saveDay(day) {
  computeScore(day);
  fs.writeFileSync(dayFile(day.date), JSON.stringify(day, null, 2));
  mirrorToNotes(day.date); // glyph glance-note for the Notification Center widget
}

function mirrorToNotes(date) {
  execFile('/usr/bin/osascript',
    [path.join(WS, 'scripts/warroom/notes_mirror.scpt'), dayFile(date)],
    (err) => { if (err) console.error('notes mirror:', err.message); });
}

/* ---- live Google Calendar merge (direct API via the workspace token, every 3 min) ---- */
const { google } = require('googleapis');
const GTOKEN = `${process.env.HOME}/.google_workspace_mcp/credentials/daniel@ministryflow.co.json`;
let calCache = { at: 0, events: [] };
function gcal() {
  const t = JSON.parse(fs.readFileSync(GTOKEN, 'utf8'));
  const o = new google.auth.OAuth2(t.client_id, t.client_secret, t.token_uri);
  o.setCredentials({ refresh_token: t.refresh_token });
  return google.calendar({ version: 'v3', auth: o });
}
async function refreshCal() {
  try {
    const start = new Date(); start.setHours(0, 0, 0, 0);
    const end = new Date(start); end.setDate(end.getDate() + 1);
    const r = await gcal().events.list({
      calendarId: 'daniel@ministryflow.co',
      timeMin: start.toISOString(), timeMax: end.toISOString(),
      singleEvents: true, orderBy: 'startTime', maxResults: 100,
    });
    calCache = {
      at: Date.now(),
      events: (r.data.items || [])
        .filter((ev) => ev.start && ev.start.dateTime && !String(ev.summary || '').startsWith('⚔️'))
        .map((ev) => ({ start: new Date(ev.start.dateTime), end: new Date(ev.end.dateTime), summary: ev.summary || 'Busy' })),
    };
  } catch (e) { console.error('cal refresh:', e.message); }
}
refreshCal();
setInterval(refreshCal, 3 * 60 * 1000);

// read-time merge: live calendar overwrites routine/bare slots; the day FILE stays untouched
function mergeCalendar(day) {
  if (!calCache.events.length) return day;
  const d = JSON.parse(JSON.stringify(day));
  const byTime = {};
  d.slots.forEach((s) => { byTime[s.time] = s; });
  for (const ev of calCache.events) {
    const t = new Date(ev.start);
    t.setMinutes(t.getMinutes() < 30 ? 0 : 30, 0, 0);
    for (let c = new Date(t); c < ev.end; c = new Date(+c + 30 * 60000)) {
      const hh = String(c.getHours()).padStart(2, '0') + ':' + String(c.getMinutes()).padStart(2, '0');
      const s = byTime[hh];
      if (s && !s.taskId) s.routine = ev.summary;
    }
  }
  return d;
}

app.get('/api/day/:date', (req, res) => {
  const wantToday = req.params.date === 'today';
  const day = loadDay(wantToday ? todayStr() : req.params.date);
  if (!day) return res.status(404).json({ error: 'no plan for that day' });
  res.json(wantToday ? mergeCalendar(day) : day);
});

// tick a slot and/or a task; task.done cascades to its slots and vice versa.
// Routine slots are tickable too but NEVER counted (computeScore only counts taskId slots).
app.post('/api/tick', (req, res) => {
  const { date, time, taskId, done, actual } = req.body;
  const day = loadDay(date || todayStr());
  if (!day) return res.status(404).json({ error: 'no plan' });
  if (time) {
    // any slot is tickable (live-merged calendar rows tick onto bare file slots);
    // only taskId slots ever count toward the score
    const slot = day.slots.find((s) => s.time === time);
    if (!slot) return res.status(400).json({ error: 'no slot at ' + time });
    slot.done = !!done;
    if (!slot.taskId) slot.manual = true;   // user's hand beats the auto-tick clock
  }
  if (taskId) {
    const t = day.priorities.find((p) => p.id === taskId);
    if (t) {
      t.done = !!done;
      t.progress = done ? 100 : 0;
      if (actual !== undefined) t.actual = actual;
      syncSlots(day, taskId);
    }
  }
  // slot-level ticks drive their task's progress
  if (time && !taskId) {
    const slot = day.slots.find((s) => s.time === time);
    if (slot && slot.taskId) {
      const t = day.priorities.find((p) => p.id === slot.taskId);
      const ss = day.slots.filter((s) => s.taskId === slot.taskId);
      const dn = ss.filter((s) => s.done).length;
      if (t) {
        t.progress = Math.round((dn / ss.length) * 100);
        t.done = t.progress >= 100 ? true : (t.progress > 0 ? false : t.done === true ? false : t.done);
      }
    }
  }
  saveDay(day);
  res.json(day);
});

// hold-to-set partial progress (0–100); <100 counts as answered (no more nags) and carries tomorrow
app.post('/api/progress', (req, res) => {
  const { date, taskId, progress } = req.body;
  const day = loadDay(date || todayStr());
  if (!day) return res.status(404).json({ error: 'no plan' });
  const t = day.priorities.find((p) => p.id === taskId);
  if (!t) return res.status(404).json({ error: 'no such task' });
  t.progress = Math.max(0, Math.min(100, Math.round(progress)));
  t.done = t.progress >= 100 ? true : (t.progress > 0 ? false : null);
  syncSlots(day, taskId);
  saveDay(day);
  res.json(day);
});

// calls tally / improve text / shipped-output line — never tick state
app.post('/api/meta', (req, res) => {
  const day = loadDay(req.body.date || todayStr());
  if (!day) return res.status(404).json({ error: 'no plan' });
  ['callsConducted', 'callsBooked', 'improve', 'notes'].forEach((k) => {
    if (req.body[k] !== undefined) day[k] = req.body[k];
  });
  if (req.body.output !== undefined) {
    day.score = day.score || {};
    day.score.output = req.body.output;
  }
  saveDay(day);
  res.json(day);
});

// voice → text for the improve field (ElevenLabs Scribe)
function envKey(name) {
  const env = fs.readFileSync(path.join(process.env.HOME, '.claude/.env'), 'utf8');
  const m = env.match(new RegExp('^' + name + '=(.*)$', 'm'));
  return m ? m[1].trim() : null;
}
app.post('/api/transcribe', express.raw({ type: () => true, limit: '25mb' }), async (req, res) => {
  try {
    const key = envKey('ELEVENLABS_API_KEY');
    if (!key) return res.status(500).json({ error: 'no elevenlabs key' });
    const mime = req.headers['x-audio-type'] || 'audio/webm';
    const fd = new FormData();
    fd.append('file', new Blob([req.body], { type: mime }), 'voice.' + (mime.includes('mp4') ? 'mp4' : 'webm'));
    fd.append('model_id', 'scribe_v1');
    const r = await fetch('https://api.elevenlabs.io/v1/speech-to-text', {
      method: 'POST', headers: { 'xi-api-key': key }, body: fd,
    });
    if (!r.ok) return res.status(502).json({ error: 'stt failed: ' + (await r.text()).slice(0, 200) });
    const out = await r.json();
    res.json({ text: out.text || '' });
  } catch (e) { res.status(500).json({ error: e.message }); }
});

/* ---- "Plan tomorrow today": runs the real planning engine for tomorrow, now ---- */
let planJob = null;
const tomorrowStr = () =>
  new Date(Date.now() + 864e5).toLocaleDateString('en-CA', { timeZone: 'Europe/London' });
app.post('/api/plan-tomorrow', (req, res) => {
  if (planJob && planJob.running) return res.json({ running: true, date: planJob.date });
  const target = tomorrowStr();
  planJob = { running: true, startedAt: Date.now(), date: target, error: null };
  execFile('/bin/zsh', [path.join(WS, 'scripts/warroom/horizon.sh')],
    { timeout: 20 * 60 * 1000 }, (err) => {
      planJob.running = false;
      planJob.error = err && !fs.existsSync(dayFile(target)) ? String(err.message).slice(0, 200) : null;
    });
  res.json({ running: true, date: target });
});
app.get('/api/plan-status', (_req, res) => {
  const target = tomorrowStr();
  res.json({
    running: !!(planJob && planJob.running),
    error: (planJob && planJob.error) || null,
    exists: fs.existsSync(dayFile(target)),
    date: target,
    startedAt: planJob ? planJob.startedAt : null,
  });
});

// history for dashboards/weekly review
app.get('/api/history', (_req, res) => {
  const files = fs.readdirSync(DAILY).filter((f) => f.endsWith('.json')).sort();
  res.json(files.slice(-31).map((f) => JSON.parse(fs.readFileSync(path.join(DAILY, f), 'utf8'))));
});

// auto-tick non-work items once their time has passed (manual unticks are respected)
function autoTickRoutine() {
  const day = loadDay(todayStr());
  if (!day) return;
  const now = new Date();
  const nowM = now.getHours() * 60 + now.getMinutes();
  let changed = false;
  for (const s of day.slots) {
    if (s.taskId || !s.routine || s.done || s.manual) continue;
    const [h, m] = s.time.split(':').map(Number);
    if (h * 60 + m + 30 <= nowM) { s.done = true; changed = true; }
  }
  if (changed) saveDay(day);
}
autoTickRoutine();
setInterval(autoTickRoutine, 5 * 60 * 1000);

require('./push')(app, { loadDay, saveDay, todayStr, APPDATA, SECRET });

app.listen(PORT, () => console.log(`War Room on :${PORT}`));
