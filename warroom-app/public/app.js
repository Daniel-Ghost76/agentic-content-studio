const KEY = localStorage.warroomKey ||
  (localStorage.warroomKey = new URLSearchParams(location.search).get('key') || '');
caches.open('warroom-key').then((c) => c.put('key', new Response(KEY)));
const H = { 'x-warroom-key': KEY, 'Content-Type': 'application/json' };
let day = null;

async function api(path, body) {
  const res = await fetch('/api/' + path,
    body ? { method: 'POST', headers: H, body: JSON.stringify(body) } : { headers: H });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

/* ---------- aurora canvas ---------- */
(function aurora() {
  const cv = document.getElementById('aurora');
  const ctx = cv.getContext('2d');
  let w, h;
  const resize = () => { w = cv.width = innerWidth * devicePixelRatio; h = cv.height = innerHeight * devicePixelRatio; };
  resize(); addEventListener('resize', resize);
  const blobs = [
    { x: .25, y: .12, r: .55, sp: .00009, ph: 0,   amp: .16, op: .16 },
    { x: .78, y: .30, r: .42, sp: .00012, ph: 2.1, amp: .20, op: .11 },
    { x: .50, y: .85, r: .60, sp: .00007, ph: 4.4, amp: .13, op: .08 },
    { x: .10, y: .65, r: .35, sp: .00014, ph: 1.2, amp: .22, op: .09 },
  ];
  function frame(t) {
    ctx.clearRect(0, 0, w, h);
    ctx.globalCompositeOperation = 'lighter';
    for (const b of blobs) {
      const x = (b.x + Math.sin(t * b.sp + b.ph) * b.amp) * w;
      const y = (b.y + Math.cos(t * b.sp * 1.3 + b.ph) * b.amp * .7) * h;
      const r = b.r * Math.max(w, h) * (1 + Math.sin(t * b.sp * .8 + b.ph) * .12);
      const g = ctx.createRadialGradient(x, y, 0, x, y, r);
      g.addColorStop(0, `rgba(255,255,255,${b.op})`);
      g.addColorStop(.4, `rgba(220,225,240,${b.op * .45})`);
      g.addColorStop(1, 'rgba(255,255,255,0)');
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill();
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();

/* ---------- helpers ---------- */
function endtime(t) {
  let [h, m] = t.split(':').map(Number);
  m += 30;
  return String(h + Math.floor(m / 60)).padStart(2, '0') + ':' + String(m % 60).padStart(2, '0');
}
function mins(t) { const [h, m] = t.split(':').map(Number); return h * 60 + m; }

/* ---------- render ---------- */
function render() {
  document.getElementById('date').textContent = new Date(day.date + 'T12:00')
    .toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' });
  document.getElementById('focus').textContent = day.focus;

  const rating = day.score.rating ?? 0;
  document.getElementById('rating').textContent = rating + '%';
  document.getElementById('hours').textContent =
    rating === 0 ? "let's go" : (day.score.hours ?? 0) + 'h focused';
  const ringEl = document.getElementById('ring');
  document.getElementById('ring-fill').style.strokeDashoffset = 339.3 * (1 - rating / 100);
  ringEl.classList.toggle('complete', rating >= 100);

  // priorities
  const pl = document.getElementById('prio-list');
  pl.innerHTML = '';
  day.priorities.forEach((p) => {
    const el = document.createElement('div');
    el.className = 'prio' + (p.done ? ' done' : '');
    el.innerHTML = `<span class="tick"></span><span class="ptext">${p.text}` +
      (p.actual != null ? ` <b>(${p.actual})</b>` : '') + '</span>' +
      (p.carryFrom ? `<span class="carry">⟳ ${p.carryFrom}</span>` : '');
    el.onclick = () => api('tick', { date: day.date, taskId: p.id, done: !p.done }).then(set);
    pl.appendChild(el);
  });

  // timeline: group work slots into runs, keep routine entries
  const entries = [];
  day.slots.forEach((s) => {
    if (s.taskId) {
      const last = entries[entries.length - 1];
      if (last && last.type === 'work' && last.tid === s.taskId && last.end === s.time) {
        last.end = endtime(s.time);
        last.done = last.done && !!s.done;
        last.times.push(s.time);
      } else {
        entries.push({ type: 'work', tid: s.taskId, start: s.time, end: endtime(s.time), done: !!s.done, times: [s.time] });
      }
    } else if (s.routine) {
      entries.push({ type: 'routine', start: s.time, label: s.routine });
    }
  });

  const tl = document.getElementById('tl');
  tl.innerHTML = '';
  entries.forEach((e) => {
    const el = document.createElement('div');
    if (e.type === 'work') {
      const t = day.priorities.find((p) => p.id === e.tid);
      el.className = 'tl-row work' + (e.done ? ' done' : '');
      el.innerHTML = `<span class="tl-time">${e.start}–${e.end}</span><span class="tl-dot"></span>` +
        `<span class="tick"></span><span class="ttext">${t ? t.text : e.tid}</span>`;
      el.onclick = async () => {
        for (const time of e.times) await api('tick', { date: day.date, time, done: !e.done });
        set(await api('day/today'));
      };
    } else {
      el.className = 'tl-row routine';
      el.innerHTML = `<span class="tl-time">${e.start}</span><span class="tl-dot"></span><span>${e.label}</span>`;
    }
    el.dataset.start = e.start;
    el.dataset.end = e.end || endtime(e.start);
    tl.appendChild(el);
  });
  positionNowLine();

  const imp = document.getElementById('improve');
  if (document.activeElement !== imp) imp.value = day.improve || '';

  if (day.reported) hideReport();
}

function positionNowLine() {
  const tl = document.getElementById('tl');
  document.getElementById('now-line')?.remove();
  const now = new Date();
  const nowM = now.getHours() * 60 + now.getMinutes();
  const rows = [...tl.children];
  for (const row of rows) {
    const s = mins(row.dataset.start), e = mins(row.dataset.end);
    if (nowM >= s && nowM < e) {
      const frac = (nowM - s) / (e - s);
      const line = document.createElement('div');
      line.id = 'now-line';
      line.style.top = (row.offsetTop + row.offsetHeight * frac) + 'px';
      tl.appendChild(line);
      return;
    }
  }
}
setInterval(positionNowLine, 60_000);

function set(d) { day = d; render(); }

/* ---------- improve autosave ---------- */
let metaTimer;
document.getElementById('improve').addEventListener('input', () => {
  clearTimeout(metaTimer);
  metaTimer = setTimeout(() => api('meta', {
    date: day.date, improve: document.getElementById('improve').value,
  }).then((d) => { day = d; }), 600);
});

/* ---------- send report ---------- */
function hideReport() {
  const btn = document.getElementById('report');
  if (btn) btn.remove();
}
document.getElementById('report').onclick = async function () {
  this.classList.add('sending');
  this.textContent = 'Sending…';
  try {
    await api('report', { date: day.date });
    const done = document.createElement('div');
    done.id = 'report-done';
    done.innerHTML = '<div class="big-tick"></div><span>Report sent — day recorded</span>';
    this.replaceWith(done);
    setTimeout(() => done.remove(), 4000);
  } catch (e) {
    this.classList.remove('sending');
    this.textContent = 'Send report';
    alert('Failed: ' + e.message);
  }
};

/* ---------- push (only shown if this device hasn't granted) ---------- */
(async function pushSetup() {
  const btn = document.getElementById('enable-push');
  if (!('Notification' in window) || Notification.permission === 'granted') return;
  btn.hidden = false;
  btn.onclick = async () => {
    try {
      const standalone = window.matchMedia('(display-mode: standalone)').matches || navigator.standalone;
      if (!standalone && /iPhone|iPad/.test(navigator.userAgent)) {
        alert('Open Daybreak from the home-screen icon first — iOS only allows notifications from the installed app.');
        return;
      }
      const reg = await navigator.serviceWorker.ready;
      const { publicKey } = await api('vapid-public-key');
      const sub = await reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: publicKey });
      await api('subscribe', sub.toJSON());
      btn.hidden = true;
    } catch (e) { alert('Notification setup failed: ' + e.message); }
  };
})();

/* ---------- check-in deep link (?focus=taskId) ---------- */
function maybeFocusTask() {
  const id = new URLSearchParams(location.search).get('focus');
  if (!id || !day) return;
  const t = day.priorities.find((p) => p.id === id);
  if (!t || t.done !== null) return;
  const ov = document.createElement('div');
  ov.id = 'focus-overlay';
  ov.innerHTML = `
    <div class="sheet">
      <p>${t.text}</p>
      <button class="yes">Done</button>
      <button class="no">Not yet</button>
    </div>`;
  ov.querySelector('.yes').onclick = () => answer(true);
  ov.querySelector('.no').onclick = () => answer(false);
  function answer(done) {
    api('tick', { date: day.date, taskId: id, done }).then((d) => {
      ov.remove();
      history.replaceState(null, '', '/');
      set(d);
    });
  }
  document.body.appendChild(ov);
}

navigator.serviceWorker.register('sw.js');
api('day/today').then((d) => { set(d); maybeFocusTask(); }).catch((e) => {
  if (!KEY || e.message.includes('bad key')) {
    const k = prompt('Enter your Daybreak key:');
    if (k && k.trim()) { localStorage.warroomKey = k.trim(); location.reload(); return; }
  }
  document.body.innerHTML = `<h1 style="padding:40px;font-family:ui-serif,Georgia,serif">No plan for today yet.</h1>`;
});
setInterval(() => api('day/today').then(set).catch(() => {}), 60_000);
