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

/* ---------- living dune line: real particle flow, pointer-reactive, nothing layered on top ---------- */
(function dunes() {
  const cv = document.getElementById('aurora');
  const ctx = cv.getContext('2d');
  const DPR = Math.min(devicePixelRatio || 1, 2);
  let w, h, parts = [];
  const SAMPLES = 220;
  const mouse = { x: -1e6, y: -1e6 };
  addEventListener('pointermove', (e) => { mouse.x = e.clientX * DPR; mouse.y = e.clientY * DPR; }, { passive: true });
  addEventListener('pointerleave', () => { mouse.x = -1e6; mouse.y = -1e6; });

  // gaussian-ish via central limit
  const g = () => (Math.random() + Math.random() + Math.random() + Math.random() - 2) / 2;

  // ridge definitions in unit space; control points drift slowly → the LINE flows
  const RIDGES = [
    { p: [[.72, -.08], [.38, .22], [.95, .55], [.55, 1.08]], n: 30000, spread: 42, alpha: .85 },
    { p: [[-.05, .65], [.30, .38], [.12, .18], [.42, -.05]], n: 11000, spread: 32, alpha: .5 },
  ];
  // per-control-point drift phases/amplitudes (unit-space, small)
  const DRIFT = RIDGES.map(() => [0, 1, 2, 3].map(() => ({
    ax: .015 + Math.random() * .02, ay: .012 + Math.random() * .018,
    px: Math.random() * 6.28, py: Math.random() * 6.28,
    sx: .00005 + Math.random() * .00004, sy: .00004 + Math.random() * .00004,
  })));

  function setup() {
    w = cv.width = innerWidth * DPR;
    h = cv.height = innerHeight * DPR;
    parts = [];
    const budget = innerWidth < 700 ? .3 : 1;    // lighter sim on phone
    RIDGES.forEach((r, ri) => {
      for (let i = 0; i < r.n * budget; i++) {
        // two-tier dust (Apple-event style): dense velvet core + wide sparse sparkle halo
        const tight = Math.random() < .72;
        const d = g() * r.spread * (tight ? .5 : 2.1);
        let a = tight
          ? r.alpha * (.4 + Math.random() * .6)
          : r.alpha * Math.exp(-Math.abs(d) / (r.spread * 1.1)) * (.12 + Math.random() * .5);
        if (Math.random() < .03) a = Math.min(a * 2.2, .95);   // rare bright sparkles
        a = Math.round(Math.min(a, .95) * 18) / 18;   // quantize → few fillStyle switches per frame
        if (a < .04) continue;
        parts.push({
          ri, idx: Math.floor(Math.random() * SAMPLES),
          d: d * DPR,
          a,
          s: Math.random() < .94 ? 1 : 2,            // single-pixel grain, rare brighter fleck
          ph: Math.random() * 6.28,
          wob: .4 + Math.random() * 1.2,
          ox: 0, oy: 0,                              // pointer displacement (springs back)
        });
      }
    });
    // bucket by alpha so we set fillStyle ~10× per frame, not 9000×
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

  const R = 170, FORCE = 30;                       // hover field (css px)
  function frame(time) {
    ctx.clearRect(0, 0, w, h);
    sampleCurves(time);
    const rad = R * DPR, rad2 = rad * rad;
    let lastA = -1;
    for (const p of parts) {
      const P = tableP[p.ri], N = tableN[p.ri];
      const i2 = p.idx * 2;
      // breathing of the grain itself: soft per-particle wobble across the crest
      const wob = Math.sin(time * .00035 + p.ph) * p.wob * DPR;
      let x = P[i2] + N[i2] * (p.d + wob);
      let y = P[i2 + 1] + N[i2 + 1] * (p.d + wob);
      // pointer field: particles ease away near the cursor, spring back smoothly
      const dx = x - mouse.x, dy = y - mouse.y;
      const dist2 = dx * dx + dy * dy;
      let tx = 0, ty = 0;
      if (dist2 < rad2) {
        const dist = Math.sqrt(dist2) || 1;
        const f = (1 - dist / rad);
        const push = f * f * FORCE * DPR;
        tx = (dx / dist) * push; ty = (dy / dist) * push;
      }
      p.ox += (tx - p.ox) * .07;                  // critically-damped feel
      p.oy += (ty - p.oy) * .07;
      if (p.a !== lastA) { ctx.fillStyle = `rgba(255,255,255,${p.a})`; lastA = p.a; }
      ctx.fillRect(x + p.ox, y + p.oy, p.s, p.s);
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
  document.getElementById('ring-fill').style.strokeDashoffset = 339.3 * (1 - rating / 100);
  document.getElementById('ring').classList.toggle('complete', rating >= 100);

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

  // timeline — FULL day: work runs, routine panels (non-counting), empty hour marks
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
      entries.push({ type: 'rest', start: s.time, label: s.routine, done: !!s.done });
    } else {
      entries.push({ type: 'empty', start: s.time });
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
    } else if (e.type === 'rest') {
      el.className = 'tl-row rest' + (e.done ? ' done' : '');
      el.innerHTML = `<span class="tl-time">${e.start}</span><span class="tl-dot"></span>` +
        `<span class="tick"></span><span class="ttext">${e.label}</span>`;
      el.onclick = () => api('tick', { date: day.date, time: e.start, done: !e.done }).then(set);
    } else {
      el.className = 'tl-row empty';
      el.innerHTML = `<span class="tl-time">${e.start}</span><span class="tl-dash"></span>`;
    }
    el.dataset.start = e.start;
    el.dataset.end = e.end || endtime(e.start);
    tl.appendChild(el);
  });
  positionNowLine();

  const imp = document.getElementById('improve');
  if (document.activeElement !== imp) imp.value = day.improve || '';

  if (day.reported) document.getElementById('report')?.remove();
}

function positionNowLine() {
  const tl = document.getElementById('tl');
  document.getElementById('now-line')?.remove();
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

/* ---------- improve autosave ---------- */
let metaTimer;
function saveImprove() {
  clearTimeout(metaTimer);
  metaTimer = setTimeout(() => api('meta', {
    date: day.date, improve: document.getElementById('improve').value,
  }).then((d) => { day = d; }), 600);
}
document.getElementById('improve').addEventListener('input', saveImprove);

/* ---------- voice input (server-side transcription) ---------- */
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
            saveImprove();
          }
        } catch (e) { alert('Transcription failed: ' + e.message); }
        btn.classList.remove('busy');
      };
      rec.start();
      btn.classList.add('recording');
    } catch (e) { alert('Microphone unavailable: ' + e.message); }
  };
})();

/* ---------- send report ---------- */
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
