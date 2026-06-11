#!/usr/bin/env node
/*
 * Deterministic calendar sync for Daybreak.
 * The LLM writes plans (Planning/Daily/<date>.json); THIS code writes the
 * calendar. It ONLY ever touches events whose summary starts with "⚔️" —
 * meetings, "Call with Ana", routine, and every other event are physically
 * unreachable. Idempotent: re-running produces the same calendar, no dupes.
 *
 * Usage:
 *   node calsync.js --days 7        # sync today+1..today+7 from their JSONs
 *   node calsync.js --date 2026-06-12
 *   node calsync.js --purge --days 7   # delete all ⚔️ blocks, create nothing
 */
const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');

const WS = '/Users/danieldanut/Agentic Workspace';
const DAILY = path.join(WS, 'Planning/Daily');
const TOKEN = `${process.env.HOME}/.google_workspace_mcp/credentials/daniel@ministryflow.co.json`;
const TAG = '⚔️';
const CAL = 'daniel@ministryflow.co';
const TZ = 'Europe/London';

const args = process.argv.slice(2);
const purge = args.includes('--purge');
const dateArg = args.includes('--date') ? args[args.indexOf('--date') + 1] : null;
const days = args.includes('--days') ? parseInt(args[args.indexOf('--days') + 1], 10) : 7;

function ldate(offset) {
  const d = new Date();
  d.setDate(d.getDate() + offset);
  return d.toLocaleDateString('en-CA', { timeZone: TZ });
}

function auth() {
  const t = JSON.parse(fs.readFileSync(TOKEN, 'utf8'));
  const o = new google.auth.OAuth2(t.client_id, t.client_secret, t.token_uri);
  o.setCredentials({ refresh_token: t.refresh_token, access_token: t.token, expiry_date: Date.parse(t.expiry) });
  return o;
}

// derive ⚔️ blocks from a day JSON: consecutive same-taskId slots → one event
function blocksFor(date) {
  const f = path.join(DAILY, `${date}.json`);
  if (!fs.existsSync(f)) return null;
  const day = JSON.parse(fs.readFileSync(f, 'utf8'));
  const text = {};
  (day.priorities || []).forEach((p) => { text[p.id] = p.text; });
  const runs = [];
  const add = (t) => { const [h, m] = t.split(':').map(Number); return h * 60 + m; };
  const hhmm = (mins) => `${String(Math.floor(mins / 60) % 24).padStart(2, '0')}:${String(mins % 60).padStart(2, '0')}`;
  (day.slots || []).forEach((s) => {
    if (!s.taskId) return;
    const last = runs[runs.length - 1];
    if (last && last.taskId === s.taskId && last.endM === add(s.time)) last.endM = add(s.time) + 30;
    else runs.push({ taskId: s.taskId, startM: add(s.time), endM: add(s.time) + 30 });
  });
  return runs.map((r) => ({
    summary: `${TAG} ${text[r.taskId] || r.taskId}`,
    start: hhmm(r.startM), end: hhmm(r.endM),
  }));
}

async function syncDay(cal, date) {
  const dayStart = `${date}T00:00:00`;
  const dayEnd = `${date}T23:59:59`;
  // 1. delete every existing ⚔️ event that day
  const existing = await cal.events.list({
    calendarId: CAL, timeMin: new Date(dayStart).toISOString(),
    timeMax: new Date(dayEnd).toISOString(), singleEvents: true, maxResults: 100,
  });
  let deleted = 0;
  for (const ev of existing.data.items || []) {
    if ((ev.summary || '').startsWith(TAG)) {
      await cal.events.delete({ calendarId: CAL, eventId: ev.id });
      deleted++;
    }
  }
  if (purge) return { date, deleted, created: 0 };
  // 2. create fresh ⚔️ blocks from the JSON
  const blocks = blocksFor(date);
  if (!blocks) return { date, deleted, created: 0, note: 'no plan' };
  let created = 0;
  for (const b of blocks) {
    await cal.events.insert({
      calendarId: CAL,
      requestBody: {
        summary: b.summary, colorId: '9',
        start: { dateTime: `${date}T${b.start}:00`, timeZone: TZ },
        end: { dateTime: `${date}T${b.end}:00`, timeZone: TZ },
      },
    });
    created++;
  }
  return { date, deleted, created };
}

(async () => {
  const cal = google.calendar({ version: 'v3', auth: auth() });
  const targets = dateArg ? [dateArg] : Array.from({ length: days }, (_, i) => ldate(i + 1));
  for (const date of targets) {
    try {
      const r = await syncDay(cal, date);
      console.log(`${r.date}: -${r.deleted} ⚔️ +${r.created}${r.note ? ' (' + r.note + ')' : ''}`);
    } catch (e) {
      console.error(`${date}: FAILED ${e.message}`);
      process.exitCode = 1;
    }
  }
})();
