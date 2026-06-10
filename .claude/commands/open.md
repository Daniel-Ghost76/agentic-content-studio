Open any workspace tool, URL, or local dev server in Antigravity's Simple Browser preview tab.

Usage:
- `/open <tool>` — a registered tool name (see registry below)
- `/open <url>` — any full URL, e.g. `/open https://example.com`
- `/open <port>` / `/open localhost:<port>` / `/open :<port>` — a local server, e.g. `/open 3000`

## How it works

Everything is opened through the shared helper:
`/Users/danieldanut/Agentic Workspace/.claude/scripts/open_in_antigravity.sh <url>`
The helper auto-routes: localhost and iframe-friendly sites open **in the Simple Browser preview tab**; sites that block embedding (Google, etc.) or any palette-automation failure open in the **external browser** instead, and it tells you which happened. So you can throw any tool or URL at it and it does the sensible thing.

## Tool registry

**Local dev servers** (start a server, then open localhost in the preview):

| arg (aliases) | dir (under `Youtube/Input/5. Tools/5. visuals_tools/`) | start | url |
|---|---|---|---|
| `remotion` | `remotion-visuals` | `npm run dev` (→ `remotion studio`) | `http://localhost:3000` |
| `hyperframes`, `hf` | `hyperframes` | `npx hyperframes preview` | parse `http://localhost:<port>` from its stdout |

**Web tools** (open the URL via the helper, which previews it or falls back to external):

| arg (aliases) | url |
|---|---|
| `higgsfield`, `higgs` | `https://higgsfield.ai` |
| `youtube`, `studio` | `https://studio.youtube.com` |
| `notebooklm`, `nlm` | `https://notebooklm.google.com` |
| `skool` | `https://www.skool.com` |
| `perplexity`, `pplx` | `https://www.perplexity.ai` |
| `chatgpt`, `gpt` | `https://chatgpt.com` |
| `elevenlabs`, `11labs` | `https://elevenlabs.io/app` |
| `miro` | `https://miro.com` |
| `spotify` | `https://open.spotify.com` |
| `drive` | `https://drive.google.com` |
| `docs` | `https://docs.google.com` |
| `sheets` | `https://sheets.google.com` |
| `gmail` | `https://mail.google.com` |
| `calendar` | `https://calendar.google.com` |

## Behavior

1. Parse the argument:
   - **Looks like a URL** (`http://` / `https://`) → call the helper with it directly.
   - **Looks like a port** (`3000`, `:3000`, `localhost:3000`) → call the helper with `http://localhost:<port>`.
   - **Otherwise** → match it (case-insensitive, incl. aliases) against the registry.
   - **No arg or no match** → print the registry tool list and remind the user they can also pass any URL or `localhost:<port>`. Then stop.
2. **Web tool / URL / port:** just call the helper. It decides preview vs external and reports back. Don't second-guess it.
3. **Local dev-server tool (remotion, hyperframes):**
   - Check if the server is already up (`lsof -i :<port>` for Remotion, or curl the port). If listening, skip launching and open the tab.
   - Otherwise `cd` into the tool's directory and start the server with `run_in_background: true` so it survives the turn.
   - Poll briefly until the port responds; for HyperFrames capture the `http://localhost:<port>` it prints (the port can vary).
   - Then call the helper with that URL.
4. Report: which tool/URL, whether the dev server was already running or just started, and whether it landed in the Simple Browser preview or fell back to the external browser (and why).

## Extending

Add a row to the registry above — a URL for web tools, or a dir + start command + port for dev-server tools. Note that nothing extra is needed for one-off tools: `/open <url>` already opens anything. Tools without a web UI (plain Python/CLI scripts) can't be previewed.
