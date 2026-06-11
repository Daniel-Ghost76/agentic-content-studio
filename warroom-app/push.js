const webpush = require('web-push');
const fs = require('fs');
const path = require('path');

module.exports = (app, { loadDay, todayStr, APPDATA }) => {
  const vapid = JSON.parse(fs.readFileSync(path.join(APPDATA, 'vapid.json'), 'utf8'));
  webpush.setVapidDetails('mailto:daniel@ministryflow.co', vapid.publicKey, vapid.privateKey);
  const SUBS = path.join(APPDATA, 'subscriptions.json');
  const subs = () => JSON.parse(fs.readFileSync(SUBS, 'utf8'));

  app.get('/api/vapid-public-key', (_req, res) => res.json({ publicKey: vapid.publicKey }));
  app.post('/api/subscribe', (req, res) => {
    const all = subs().filter((s) => s.endpoint !== req.body.endpoint);
    all.push(req.body);
    fs.writeFileSync(SUBS, JSON.stringify(all, null, 2));
    res.json({ ok: all.length });
  });

  async function send(payload) {
    for (const s of subs()) {
      try { await webpush.sendNotification(s, JSON.stringify(payload)); }
      catch (e) {
        if (e.statusCode === 404 || e.statusCode === 410) { // expired sub — prune
          fs.writeFileSync(SUBS, JSON.stringify(subs().filter((x) => x.endpoint !== s.endpoint), null, 2));
        } else { console.error('push:', e.statusCode || e.message); }
      }
    }
  }

  const timers = [];
  // check-in that NAGS: re-sends every 15 min (max 3 repeats) until the task is answered
  function checkin(taskId, title, attempt = 0) {
    const d = loadDay(todayStr());
    const t = d && d.priorities.find((p) => p.id === taskId);
    if (!t || t.done !== null) return; // answered (✅ or ❌) — stop nagging
    send({
      title: attempt === 0 ? title : `Still open (${attempt + 1}×) — ${title}`,
      body: t.text, taskId: t.id, date: d.date,
    });
    if (attempt < 3) timers.push(setTimeout(() => checkin(taskId, title, attempt + 1), 15 * 60 * 1000));
  }
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
    // end-of-block check-ins: a block ends where the next work slot has a different taskId
    const work = day.slots.filter((s) => s.taskId);
    work.forEach((s, i) => {
      const next = work[i + 1];
      if (!next || next.taskId !== s.taskId) {
        const [h, m] = s.time.split(':').map(Number);
        const end = `${String(m === 30 ? h + 1 : h).padStart(2, '0')}:${m === 30 ? '00' : '30'}`;
        at(end, () => checkin(s.taskId, 'Block done?'));
      }
    });
    // 18:30 day-close sweep (nags too, so nothing dies unanswered before the 19:00 sync)
    at('18:30', () => {
      const d = loadDay(todayStr());
      if (!d) return;
      d.priorities.filter((p) => p.done === null)
        .forEach((p) => checkin(p.id, 'Day close — done?'));
    });
  }
  arm();
  setInterval(arm, 30 * 60 * 1000); // re-arm half-hourly (survives plan rewrites + sleep/wake)
  app.post('/api/rearm', (_req, res) => { arm(); res.json({ ok: true }); });
  // manual nudge — fire a real check-in for a task right now (testing / Astra integration)
  app.post('/api/nudge', (req, res) => {
    const d = loadDay(todayStr());
    const t = d && d.priorities.find((p) => p.id === req.body.taskId);
    if (!t) return res.status(404).json({ error: 'no such task' });
    checkin(t.id, 'Check-in');
    res.json({ ok: true, task: t.text });
  });
  app.post('/api/test-push', (_req, res) => {
    send({ title: 'War Room test', body: 'Push pipeline works ⚔️', taskId: 'test', date: todayStr() });
    res.json({ ok: true });
  });
};
