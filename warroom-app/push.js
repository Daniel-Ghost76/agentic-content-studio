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
  setInterval(arm, 30 * 60 * 1000); // re-arm half-hourly (survives plan rewrites + sleep/wake)
  app.post('/api/rearm', (_req, res) => { arm(); res.json({ ok: true }); });
  app.post('/api/test-push', (_req, res) => {
    send({ title: 'War Room test', body: 'Push pipeline works ⚔️', taskId: 'test', date: todayStr() });
    res.json({ ok: true });
  });
};
