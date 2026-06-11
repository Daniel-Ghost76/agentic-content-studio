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

/* ---------- dune-grain background: black, white particle ridges, breathing + click shimmer ---------- */
(function dunes() {
  const cv = document.getElementById('aurora');
  const ctx = cv.getContext('2d');
  const DPR = Math.min(devicePixelRatio || 1, 2);
  let w, h, layer;

  function bez(p0, p1, p2, p3, t) {
    const u = 1 - t;
    return {
      x: u*u*u*p0.x + 3*u*u*t*p1.x + 3*u*t*t*p2.x + t*t*t*p3.x,
      y: u*u*u*p0.y + 3*u*u*t*p1.y + 3*u*t*t*p2.y + t*t*t*p3.y,
    };
  }
  // gaussian-ish via central limit
  const g = () => (Math.random() + Math.random() + Math.random() + Math.random() - 2) / 2;

  function paintRidge(c, curve, grains, spread, alpha) {
    for (let i = 0; i < grains; i++) {
      const t = Math.random();
      const p = bez(curve[0], curve[1], curve[2], curve[3], t);
      // tangent → normal
      const p2 = bez(curve[0], curve[1], curve[2], curve[3], Math.min(t + .01, 1));
      let nx = -(p2.y - p.y), ny = p2.x - p.x;
      const len = Math.hypot(nx, ny) || 1;
      nx /= len; ny /= len;
      const d = g() * spread;                       // distance from crest
      const fall = Math.exp(-(d * d) / (spread * spread * .5));
      const a = alpha * fall * (0.25 + Math.random() * 0.75);
      c.fillStyle = `rgba(255,255,255,${a})`;
      const s = Math.random() < .92 ? 1 : 2;        // occasional brighter fleck
      c.fillRect(p.x + nx * d, p.y + ny * d, s, s);
    }
  }

  function build() {
    w = cv.width = innerWidth * DPR;
    h = cv.height = innerHeight * DPR;
    layer = document.createElement('canvas');
    layer.width = w * 1.06; layer.height = h * 1.06;   // bleed so breathing never shows edges
    const c = layer.getContext('2d');
    const W = layer.width, Hh = layer.height;
    // main S-ridge, right of center — like the reference photo
    paintRidge(c, [
      { x: W * .72, y: -Hh * .08 }, { x: W * .38, y: Hh * .22 },
      { x: W * .95, y: Hh * .55 }, { x: W * .55, y: Hh * 1.08 },
    ], 26000 * DPR, 60 * DPR, .55);
    // faint companion ridge, upper left
    paintRidge(c, [
      { x: -W * .05, y: Hh * .65 }, { x: W * .30, y: Hh * .38 },
      { x: W * .12, y: Hh * .18 }, { x: W * .42, y: -Hh * .05 },
    ], 9000 * DPR, 46 * DPR, .28);
  }
  build();
  addEventListener('resize', () => { clearTimeout(window.__dn); window.__dn = setTimeout(build, 250); });

  // The LINES move — nothing is layered on top. The pre-rendered ridge image is
  // drawn in horizontal bands, each offset by a slow travelling sine, so the
  // white grain lines undulate like fabric in slow air.
  const BANDS = 36;
  function frame(t) {
    ctx.clearRect(0, 0, w, h);
    const bandH = layer.height / BANDS;
    const ox = (layer.width - w) / 2;
    const oy = (layer.height - h) / 2;
    for (let i = 0; i < BANDS; i++) {
      const y = i * bandH;
      const phase = y * .0016 / DPR;
      const dx = Math.sin(t * .00018 + phase) * 4.5 * DPR
               + Math.sin(t * .00007 + phase * 2.3) * 2.5 * DPR;
      ctx.drawImage(layer, 0, y, layer.width, bandH,
                    dx - ox, y - oy, layer.width, bandH);
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
