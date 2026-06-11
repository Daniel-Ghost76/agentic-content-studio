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

app.get('/api/day/:date', (req, res) => {
  const day = loadDay(req.params.date === 'today' ? todayStr() : req.params.date);
  if (!day) return res.status(404).json({ error: 'no plan for that day' });
  res.json(day);
});

// tick a slot and/or a task; task.done cascades to its slots and vice versa
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

require('./push')(app, { loadDay, saveDay, todayStr, APPDATA, SECRET });

app.listen(PORT, () => console.log(`War Room on :${PORT}`));
