#!/bin/bash
# open_in_antigravity.sh [--external] <url>
# Opens <url> in Antigravity's Simple Browser preview tab when the site allows
# iframe embedding; otherwise (or if the palette automation fails) falls back to
# the system default browser. Localhost URLs always go to the preview.
# --external: skip the Simple Browser entirely and open in the default browser
# (use for heavy pages like video previews that can freeze the editor).
set -uo pipefail

if [ "${1:-}" = "--external" ]; then
  shift
  URL="${1:?usage: open_in_antigravity.sh [--external] <url>}"
  open "${URL}"
  echo "Opened in external browser (forced --external): ${URL}"
  exit 0
fi

URL="${1:?usage: open_in_antigravity.sh [--external] <url>}"

open_in_simple_browser() {
  osascript <<EOF 2>/dev/null
tell application "Antigravity IDE" to activate
delay 0.4
tell application "System Events"
  keystroke "p" using {command down, shift down}   -- command palette
  delay 0.5
  keystroke "Simple Browser: Show"
  delay 0.4
  key code 36                                       -- Return: run command
  delay 0.7
  keystroke "${URL}"
  delay 0.2
  key code 36                                       -- Return: load URL
end tell
EOF
}

# Decide preview vs external. Localhost dev servers are always frameable.
FRAMEABLE=1
case "$URL" in
  http://localhost*|https://localhost*|http://127.0.0.1*|http://0.0.0.0*) FRAMEABLE=1 ;;
  *)
    HEADERS=$(curl -sI -m 6 -L "$URL" 2>/dev/null)
    if echo "$HEADERS" | grep -qiE '^x-frame-options:|frame-ancestors'; then
      FRAMEABLE=0
    fi
    ;;
esac

if [ "$FRAMEABLE" -eq 1 ]; then
  if open_in_simple_browser; then
    echo "Opened in Antigravity Simple Browser preview tab: ${URL}"
  else
    open "${URL}"
    echo "Simple Browser automation failed (grant Accessibility in System Settings > Privacy & Security > Accessibility). Opened in external browser instead: ${URL}"
  fi
else
  open "${URL}"
  echo "This site blocks iframe embedding (X-Frame-Options / frame-ancestors), so it can't render in the in-editor preview. Opened in your external browser instead: ${URL}"
fi
