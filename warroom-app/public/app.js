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

  const cC = document.getElementById('callsC');
  const cB = document.getElementById('callsB');
  const imp = document.getElementById('improve');
  if (document.activeElement !== cC) cC.value = day.callsConducted ?? '';
  if (document.activeElement !== cB) cB.value = day.callsBooked ?? '';
  if (document.activeElement !== imp) imp.value = day.improve || '';
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
  }).then((d) => { day = d; }), 600);
}
['callsC', 'callsB', 'improve'].forEach((id) =>
  document.getElementById(id).addEventListener('input', metaChanged));

document.getElementById('enable-push').onclick = async () => {
  try {
    const reg = await navigator.serviceWorker.ready;
    const { publicKey } = await api('vapid-public-key');
    const sub = await reg.pushManager.subscribe({
      userVisibleOnly: true, applicationServerKey: publicKey });
    await api('subscribe', sub.toJSON());
    alert('Check-ins enabled on this device ✅');
  } catch (e) { alert('Push setup failed: ' + e.message); }
};

navigator.serviceWorker.register('sw.js');
api('day/today').then(set).catch((e) => {
  document.body.innerHTML = `<h1 style="padding:40px">No plan for today yet.<br><small>${e.message}</small></h1>`;
});
setInterval(() => api('day/today').then(set).catch(() => {}), 60_000); // cross-device refresh
