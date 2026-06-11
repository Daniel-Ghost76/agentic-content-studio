const KEY = localStorage.warroomKey ||
  (localStorage.warroomKey = new URLSearchParams(location.search).get('key') || '');
caches.open('warroom-key').then((c) => c.put('key', new Response(KEY)));
const H = { 'x-warroom-key': KEY, 'Content-Type': 'application/json' };
let day = null;
let view = 'today';                 // 'today' | 'tomorrow' (tomorrow is a read-only preview)
let tomorrowDate = null;

async function api(path, body) {
  const res = await fetch('/api/' + path,
    body ? { method: 'POST', headers: H, body: JSON.stringify(body) } : { headers: H });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
const RO = () => view !== 'today';

/* ---------- living dune line: fine dense grain, ridge + scatter halo, pointer-reactive ---------- */
(function dunes() {
  const cv = document.getElementById('aurora');
  const ctx = cv.getContext('2d');
  const DPR = Math.min(devicePixelRatio || 1, 2);
  let w, h, parts = [];
  const SAMPLES = 240;
  const mouse = { x: -1e6, y: -1e6 };
  addEventListener('pointermove', (e) => { mouse.x = e.clientX * DPR; mouse.y = e.clientY * DPR; }, { passive: true });
  addEventListener('pointerleave', () => { mouse.x = -1e6; mouse.y = -1e6; });
  const g = () => (Math.random() + Math.random() + Math.random() + Math.random() - 2) / 2;
  const RIDGES = [
    { p: [[.72, -.08], [.38, .22], [.95, .55], [.55, 1.08]], n: 40000, spread: 38, alpha: .75 },
    { p: [[-.05, .65], [.30, .38], [.12, .18], [.42, -.05]], n: 14000, spread: 28, alpha: .42 },
  ];
  const DRIFT = RIDGES.map(() => [0, 1, 2, 3].map(() => ({
    ax: .015 + Math.random() * .02, ay: .012 + Math.random() * .018,
    px: Math.random() * 6.28, py: Math.random() * 6.28,
    sx: .00005 + Math.random() * .00004, sy: .00004 + Math.random() * .00004,
  })));
  function setup() {
    w = cv.width = innerWidth * DPR;
    h = cv.height = innerHeight * DPR;
    parts = [];
    const budget = innerWidth < 700 ? .28 : 1;
    RIDGES.forEach((r, ri) => {
      for (let i = 0; i < r.n * budget; i++) {
        const tight = Math.random() < .78;
        const d = g() * r.spread * (tight ? .45 : 2.3);
        let a = tight
          ? r.alpha * (.3 + Math.random() * .7)
          : r.alpha * Math.exp(-Math.abs(d) / (r.spread * 1.15)) * (.1 + Math.random() * .45);
        if (Math.random() < .02) a = Math.min(a * 2.4, .95);
        a = Math.round(Math.min(a, .95) * 18) / 18;
        if (a < .04) continue;
        parts.push({
          ri, idx: Math.floor(Math.random() * SAMPLES),
          d: d * DPR, a,
          s: Math.random() < .98 ? 1 : 2,
          ph: Math.random() * 6.28,
          wob: .4 + Math.random() * 1.1,
          ox: 0, oy: 0,
        });
      }
    });
    parts.sort((p1, p2) => p1.a - p2.a);
  }
  setup();
  addEventListener('resize', () => { clearTimeout(window.__dn); window.__dn = setTimeout(setup, 250); });
  const tableP = RIDGES.map(() => new Float32Array(SAMPLES * 2));
  const tableN = RIDGES.map(() => new Float32Array(SAMPLES * 2));
  function sampleCurves(time) {
    RIDGES.forEach((r, ri) => {
      const cp = r.p.map((pt, ci) => {
        const dr = DRIFT[ri][ci];
        return {
          x: (pt[0] + Math.sin(time * dr.sx + dr.px) * dr.ax) * w,
          y: (pt[1] + Math.cos(time * dr.sy + dr.py) * dr.ay) * h,
        };
      });
      const P = tableP[ri], N = tableN[ri];
      let px = 0, py = 0;
      for (let i = 0; i < SAMPLES; i++) {
        const t = i / (SAMPLES - 1), u = 1 - t;
        const x = u*u*u*cp[0].x + 3*u*u*t*cp[1].x + 3*u*t*t*cp[2].x + t*t*t*cp[3].x;
        const y = u*u*u*cp[0].y + 3*u*u*t*cp[1].y + 3*u*t*t*cp[2].y + t*t*t*cp[3].y;
        P[i * 2] = x; P[i * 2 + 1] = y;
        if (i > 0) {
          let nx = -(y - py), ny = x - px;
          const l = Math.hypot(nx, ny) || 1;
          N[i * 2] = nx / l; N[i * 2 + 1] = ny / l;
          if (i === 1) { N[0] = N[2]; N[1] = N[3]; }
        }
        px = x; py = y;
      }
    });
  }
  const R = 170, FORCE = 30;
  function frame(time) {
    ctx.clearRect(0, 0, w, h);
    sampleCurves(time);
    const rad = R * DPR, rad2 = rad * rad;
    let lastA = -1;
    for (const p of parts) {
      const P = tableP[p.ri], N = tableN[p.ri];
      const i2 = p.idx * 2;
      const wob = Math.sin(time * .00035 + p.ph) * p.wob * DPR;
      const x = P[i2] + N[i2] * (p.d + wob);
      const y = P[i2 + 1] + N[i2 + 1] * (p.d + wob);
      const dx = x - mouse.x, dy = y - mouse.y;
      const dist2 = dx * dx + dy * dy;
      let tx = 0, ty = 0;
      if (dist2 < rad2) {
        const dist = Math.sqrt(dist2) || 1;
        const f = (1 - dist / rad);
        const push = f * f * FORCE * DPR;
        tx = (dx / dist) * push; ty = (dy / dist) * push;
      }
      p.ox += (tx - p.ox) * .07;
      p.oy += (ty - p.oy) * .07;
      if (p.a !== lastA) { ctx.fillStyle = `rgba(255,255,255,${p.a})`; lastA = p.a; }
      ctx.fillRect(x + p.ox, y + p.oy, p.s, p.s);
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();

/* ---------- helpers ---------- */
const PX_PER_MIN = 1.15;
function endtime(t) {
  let [h, m] = t.split(':').map(Number);
  m += 30;
  return String(h + Math.floor(m / 60)).padStart(2, '0') + ':' + String(m % 60).padStart(2, '0');
}
function mins(t) { const [h, m] = t.split(':').map(Number); return h * 60 + m; }

/* ---------- hold-to-set-% ---------- */
function attachHold(el, taskId) {
  let timer = null, raf = null, holding = false, pct = 0, suppressClick = false;
  const fill = el.querySelector('.prog-fill');
  const badge = el.querySelector('.prog-pct');
  function start(e) {
    if (e.button > 0 || RO()) return;
    suppressClick = false;
    timer = setTimeout(() => {
      holding = true; suppressClick = true;
      const t0 = performance.now();
      const loop = (t) => {
        if (!holding) return;
        pct = Math.min(100, Math.round((t - t0) / 30));
        if (fill) fill.style.width = pct + '%';
        if (badge) { badge.textContent = pct + '%'; badge.style.opacity = 1; }
        if (pct < 100) raf = requestAnimationFrame(loop);
      };
      raf = requestAnimationFrame(loop);
    }, 350);
  }
  function finish() {
    clearTimeout(timer);
    if (holding) {
      holding = false;
      cancelAnimationFrame(raf);
      api('progress', { date: day.date, taskId, progress: pct }).then(set);
    }
  }
  el.addEventListener('pointerdown', start);
  el.addEventListener('pointerup', finish);
  el.addEventListener('pointercancel', finish);
  el.addEventListener('pointerleave', finish);
  el.addEventListener('contextmenu', (e) => e.preventDefault());
  el.addEventListener('click', (e) => {
    if (suppressClick) { e.stopImmediatePropagation(); e.preventDefault(); suppressClick = false; }
  }, true);
}

/* ---------- render ---------- */
function render() {
  document.getElementById('date').textContent = new Date(day.date + 'T12:00')
    .toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' });
  document.getElementById('focus').textContent = day.focus;

  const rating = day.score.rating ?? 0;
  document.getElementById('rating').textContent = rating + '%';
  document.getElementById('hours').textContent =
    RO() ? 'planned' : rating === 0 ? "let's go" : (day.score.hours ?? 0) + 'h focused';
  document.getElementById('ring-fill').style.strokeDashoffset = 339.3 * (1 - rating / 100);
  document.getElementById('ring').classList.toggle('complete', rating >= 100);

  // priorities
  const pl = document.getElementById('prio-list');
  pl.innerHTML = '';
  day.priorities.forEach((p) => {
    const prog = p.progress ?? (p.done === true ? 100 : 0);
    const el = document.createElement('div');
    el.className = 'prio' + (prog >= 100 ? ' done' : prog > 0 ? ' partial' : '') + (RO() ? ' ro' : '');
    el.innerHTML = `<div class="prog-fill" style="width:${prog}%"></div>` +
      `<span class="tick"></span><span class="ptext">${p.text}` +
      (p.actual != null ? ` <b>(${p.actual})</b>` : '') + '</span>' +
      `<span class="prog-pct" style="opacity:${prog > 0 && prog < 100 ? 1 : 0}">${prog}%</span>` +
      (p.carryFrom ? `<span class="carry">⟳ ${p.carryFrom}</span>` : '');
    if (!RO()) {
      el.onclick = () => api('tick', { date: day.date, taskId: p.id, done: prog < 100 }).then(set);
      attachHold(el, p.id);
    }
    pl.appendChild(el);
  });

  // timeline — true time-scale
  const entries = [];
  day.slots.forEach((s) => {
    const last = entries[entries.length - 1];
    if (s.taskId) {
      if (last && last.type === 'work' && last.tid === s.taskId && last.end === s.time) {
        last.end = endtime(s.time); last.times.push(s.time);
      } else {
        entries.push({ type: 'work', tid: s.taskId, start: s.time, end: endtime(s.time), times: [s.time] });
      }
    } else if (s.routine) {
      if (last && last.type === 'rest' && last.label === s.routine && last.end === s.time) {
        last.end = endtime(s.time); last.done = last.done && !!s.done; last.times.push(s.time);
      } else {
        entries.push({ type: 'rest', start: s.time, end: endtime(s.time), label: s.routine, done: !!s.done, times: [s.time] });
      }
    } else {
      entries.push({ type: 'empty', start: s.time, end: endtime(s.time) });
    }
  });

  const tl = document.getElementById('tl');
  tl.innerHTML = '';
  entries.forEach((e) => {
    const el = document.createElement('div');
    const minutes = (mins(e.end) - mins(e.start) + 1440) % 1440 || 30;
    if (e.type === 'work') {
      const t = day.priorities.find((p) => p.id === e.tid);
      const prog = t ? (t.progress ?? (t.done === true ? 100 : 0)) : 0;
      el.className = 'tl-row work' + (prog >= 100 ? ' done' : prog > 0 ? ' partial' : '') + (RO() ? ' ro' : '');
      el.style.minHeight = (minutes * PX_PER_MIN) + 'px';
      el.innerHTML = `<div class="prog-fill" style="width:${prog}%"></div>` +
        `<span class="tl-time">${e.start}–${e.end}</span><span class="tl-dot"></span>` +
        `<span class="tick"></span><span class="ttext">${t ? t.text : e.tid}</span>` +
        `<span class="prog-pct" style="opacity:${prog > 0 && prog < 100 ? 1 : 0}">${prog}%</span>`;
      if (!RO()) {
        el.onclick = () => api('tick', { date: day.date, taskId: e.tid, done: prog < 100 }).then(set);
        if (t) attachHold(el, t.id);
      }
    } else if (e.type === 'rest') {
      el.className = 'tl-row rest' + (e.done ? ' done' : '') + (RO() ? ' ro' : '');
      el.style.minHeight = (minutes * PX_PER_MIN) + 'px';
      el.innerHTML = `<span class="tl-time">${e.start}</span><span class="tl-dot"></span>` +
        `<span class="tick"></span><span class="ttext">${e.label}</span>`;
      if (!RO()) {
        el.onclick = async () => {
          for (const time of e.times) await api('tick', { date: day.date, time, done: !e.done });
          set(await api('day/today'));
        };
      }
    } else {
      el.className = 'tl-row empty';
      el.style.height = (minutes * PX_PER_MIN) + 'px';
      el.innerHTML = `<span class="tl-time">${e.start}</span><span class="tl-dash"></span>`;
    }
    el.dataset.start = e.start;
    el.dataset.end = e.end;
    tl.appendChild(el);
  });
  positionNowLine();

  if (!RO()) {
    const imp = document.getElementById('improve');
    const nts = document.getElementById('notes');
    if (document.activeElement !== imp) imp.value = day.improve || '';
    if (document.activeElement !== nts) nts.value = day.notes || '';
  }
}

function positionNowLine() {
  const tl = document.getElementById('tl');
  document.getElementById('now-line')?.remove();
  if (RO()) return;
  const now = new Date();
  const nowM = now.getHours() * 60 + now.getMinutes();
  for (const row of tl.children) {
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

/* ---------- 7-day horizon strip ---------- */
const stripEl = document.getElementById('day-strip');
function ymd(offset) {
  const d = new Date();
  d.setDate(d.getDate() + offset);
  return d.toLocaleDateString('en-CA', { timeZone: 'Europe/London' });
}
let selected = ymd(0);
async function buildStrip() {
  // probe which of the next 7 days have a plan
  const days = [];
  for (let i = 0; i <= 7; i++) {
    const date = ymd(i);
    const exists = i === 0 || await api('day/' + date).then(() => true).catch(() => false);
    days.push({ date, i, exists });
  }
  stripEl.innerHTML = '';
  days.forEach(({ date, i, exists }) => {
    if (!exists) return;
    const b = document.createElement('button');
    const d = new Date(date + 'T12:00');
    b.innerHTML = i === 0 ? 'Today'
      : `<b>${d.toLocaleDateString('en-GB', { weekday: 'short' })}</b><span>${d.getDate()}</span>`;
    b.classList.toggle('active', date === selected);
    b.onclick = () => {
      selected = date;
      view = i === 0 ? 'today' : 'future';
      stripEl.querySelectorAll('button').forEach((x) => x.classList.remove('active'));
      b.classList.add('active');
      api('day/' + date).then(set);
    };
    stripEl.appendChild(b);
  });
}

/* ---------- notes + improve autosave ---------- */
let metaTimer;
function saveMeta() {
  clearTimeout(metaTimer);
  metaTimer = setTimeout(() => api('meta', {
    date: day.date,
    improve: document.getElementById('improve').value,
    notes: document.getElementById('notes').value,
  }).then((d) => { if (view === 'today') day = d; }), 600);
}
document.getElementById('improve').addEventListener('input', saveMeta);
document.getElementById('notes').addEventListener('input', saveMeta);

/* ---------- voice input ---------- */
(function voice() {
  const btn = document.getElementById('mic');
  let rec = null, chunks = [];
  btn.onclick = async () => {
    if (rec && rec.state === 'recording') { rec.stop(); return; }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mime = MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : 'audio/mp4';
      rec = new MediaRecorder(stream, { mimeType: mime });
      chunks = [];
      rec.ondataavailable = (e) => chunks.push(e.data);
      rec.onstop = async () => {
        stream.getTracks().forEach((t) => t.stop());
        btn.classList.remove('recording');
        btn.classList.add('busy');
        try {
          const blob = new Blob(chunks, { type: mime });
          const r = await fetch('/api/transcribe', {
            method: 'POST',
            headers: { 'x-warroom-key': KEY, 'x-audio-type': mime, 'Content-Type': 'application/octet-stream' },
            body: blob,
          });
          if (!r.ok) throw new Error(await r.text());
          const { text } = await r.json();
          if (text) {
            const ta = document.getElementById('improve');
            ta.value = (ta.value ? ta.value.trim() + ' ' : '') + text.trim();
            saveMeta();
          }
        } catch (e) { alert('Transcription failed: ' + e.message); }
        btn.classList.remove('busy');
      };
      rec.start();
      btn.classList.add('recording');
    } catch (e) { alert('Microphone unavailable: ' + e.message); }
  };
})();

/* ---------- Plan tomorrow today ---------- */
const PLAN_CIRC = 213.6;   // 2π × 34
const planBtn = document.getElementById('plan-tmrw');
const planProg = document.getElementById('plan-progress');
const planMsg = document.getElementById('plan-msg');
const planFill = document.getElementById('plan-fill');
const planPct = document.getElementById('plan-pct');
let planTimer = null;

function showPlanProgress(startedAt) {
  planBtn.hidden = true;
  planProg.hidden = false;
  planMsg.hidden = false;
  const t0 = startedAt || Date.now();
  clearInterval(planTimer);
  planTimer = setInterval(async () => {
    const elapsed = (Date.now() - t0) / 1000;
    const est = Math.min(92, Math.round((1 - Math.exp(-elapsed / 140)) * 100));  // smooth estimate
    planFill.style.strokeDashoffset = PLAN_CIRC * (1 - est / 100);
    planPct.textContent = est + '%';
    if (elapsed % 10 < 5) {
      const st = await api('plan-status').catch(() => null);
      if (st && !st.running) {
        clearInterval(planTimer);
        if (st.exists) {
          planFill.style.strokeDashoffset = 0;
          planPct.textContent = '100%';
          await buildStrip();
          setTimeout(() => {
            planProg.hidden = true; planMsg.hidden = true;
            planBtn.hidden = false; planBtn.textContent = 'Re-plan the week';
            const tmrw = [...stripEl.children].find((b) => b.textContent !== 'Today');
            if (tmrw) tmrw.click();
          }, 900);
        } else {
          planProg.hidden = true; planMsg.hidden = true;
          planBtn.hidden = false;
          alert('Planning failed: ' + (st.error || 'unknown — check Telegram for the alert'));
        }
      }
    }
  }, 1000);
}
planBtn.onclick = async () => {
  await api('plan-tomorrow', {});
  showPlanProgress(Date.now());
};

/* ---------- push keepalive ---------- */
(async function pushKeepalive() {
  if (!('Notification' in window) || !('serviceWorker' in navigator)) return;
  const standalone = window.matchMedia('(display-mode: standalone)').matches || navigator.standalone;
  async function subscribe() {
    const reg = await navigator.serviceWorker.ready;
    const { publicKey } = await api('vapid-public-key');
    const sub = await reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: publicKey });
    await api('subscribe', sub.toJSON());
  }
  if (Notification.permission === 'granted') {
    subscribe().catch(() => {});
  } else if (Notification.permission === 'default' && (standalone || !/iPhone|iPad/.test(navigator.userAgent))) {
    const pill = document.createElement('button');
    pill.id = 'bell-pill';
    pill.textContent = '🔔';
    pill.title = 'Enable check-ins on this device';
    pill.onclick = async () => {
      try { await subscribe(); pill.remove(); }
      catch (e) { alert('Could not enable: ' + e.message); }
    };
    document.body.appendChild(pill);
  }
})();

/* ---------- check-in deep link ---------- */
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

/* ---------- init ---------- */
navigator.serviceWorker.register('sw.js');
api('day/today').then((d) => { set(d); maybeFocusTask(); }).catch((e) => {
  if (!KEY || e.message.includes('bad key')) {
    const k = prompt('Enter your Daybreak key:');
    if (k && k.trim()) { localStorage.warroomKey = k.trim(); location.reload(); return; }
  }
  document.body.innerHTML = `<h1 style="padding:40px;font-family:ui-serif,Georgia,serif">No plan for today yet.</h1>`;
});
buildStrip();
api('plan-status').then((st) => {
  if (st.exists) planBtn.textContent = 'Re-plan the week';
  if (st.running) showPlanProgress(st.startedAt || Date.now());
}).catch(() => {});
setInterval(() => { if (view === 'today') api('day/today').then(set).catch(() => {}); }, 60_000);
