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
  mirrorToNotes(day.date); // glyph glance-note for the Notification Center widget
}

function mirrorToNotes(date) {
  execFile('/usr/bin/osascript',
    [path.join(WS, 'scripts/warroom/notes_mirror.scpt'), dayFile(date)],
    (err) => { if (err) console.error('notes mirror:', err.message); });
}

/* ---- live Google Calendar merge (secret iCal URL, polled every 3 min) ---- */
const ical = require('node-ical');
const ICS_PATH = path.join(APPDATA, 'calendar-ics-url.txt');
let calCache = { at: 0, events: [] };
async function refreshCal() {
  if (!fs.existsSync(ICS_PATH)) return;
  const url = fs.readFileSync(ICS_PATH, 'utf8').trim();
  if (!url) return;
  try {
    const data = await ical.async.fromURL(url);
    const start = new Date(); start.setHours(0, 0, 0, 0);
    const end = new Date(start); end.setDate(end.getDate() + 1);
    const evs = [];
    for (const k in data) {
      const ev = data[k];
      if (ev.type !== 'VEVENT') continue;
      const summary = String(ev.summary || '');
      if (summary.startsWith('⚔️')) continue;            // our own blocks — already in the plan
      const push = (s, e) => evs.push({ start: s, end: e, summary });
      if (ev.rrule) {
        const dur = (new Date(ev.end) - new Date(ev.start)) || 30 * 60000;
        ev.rrule.between(start, end, true).forEach((d) => {
          const ex = ev.exdate && Object.values(ev.exdate).some((x) => Math.abs(new Date(x) - d) < 60000);
          if (!ex) push(new Date(d), new Date(+d + dur));
        });
      } else if (ev.start >= start && ev.start < end) {
        push(new Date(ev.start), new Date(ev.end));
      }
    }
    calCache = { at: Date.now(), events: evs };
  } catch (e) { console.error('ics refresh:', e.message); }
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

// calls tally / improve text / shipped-output line — never tick state
app.post('/api/meta', (req, res) => {
  const day = loadDay(req.body.date || todayStr());
  if (!day) return res.status(404).json({ error: 'no plan' });
  ['callsConducted', 'callsBooked', 'improve'].forEach((k) => {
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

// "Send report" — fires the day recap to Telegram immediately, marks day reported
app.post('/api/report', (req, res) => {
  const day = loadDay(req.body.date || todayStr());
  if (!day) return res.status(404).json({ error: 'no plan' });
  const doneP = day.priorities.filter((p) => p.done === true).map((p) => p.text + (p.actual != null ? ` (${p.actual})` : ''));
  const openP = day.priorities.filter((p) => p.done !== true).map((p) => p.text);
  const msg = `Daybreak report — ${day.date}\n` +
    `${day.score.rating ?? 0}% · ${day.score.hours ?? 0}h focused\n` +
    `Shipped: ${doneP.length ? doneP.join(' · ') : 'nothing yet'}\n` +
    `Open: ${openP.length ? openP.join(' · ') : 'nothing'}` +
    (day.improve ? `\nImprove: ${day.improve}` : '');
  execFile(path.join(WS, 'scripts/warroom/alert.sh'), [msg], (err) => {
    if (err) return res.status(500).json({ error: 'telegram failed' });
    day.reported = true;
    saveDay(day);
    res.json(day);
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
