#!/bin/zsh
set -uo pipefail
WS="/Users/danieldanut/Agentic Workspace"
caffeinate -u -t 5   # light the display
PLAN="$WS/Planning/Daily/$(date +%F).json"
if [[ ! -f "$PLAN" ]]; then
  "$WS/scripts/warroom/alert.sh" "4am pop: no plan for today — morning build failed?"
  exit 1
fi
KEY=$(cat "$WS/Planning/app-data/secret.txt")

# screen size
SIZE=$(osascript -e 'tell application "Finder" to get bounds of window of desktop')
SW=$(echo "$SIZE" | awk -F', ' '{print $3}')
SH=$(echo "$SIZE" | awk -F', ' '{print $4}')
NOTE_W=440

# refresh the glance note for the Notification Center widget (silent, no focus steal)
osascript "$WS/scripts/warroom/notes_mirror.scpt" "$PLAN" 2>/dev/null || true

# hide every other app
osascript -e 'tell application "System Events" to set visible of (every process whose visible is true and name is not "Google Chrome" and name is not "Finder") to false' 2>/dev/null || true

# close stale Daybreak windows, open ONE fullscreen-size surface, bring it FRONT
osascript -e 'tell application "Google Chrome" to close (every window whose URL of active tab contains "8787")' 2>/dev/null || true
open -na "Google Chrome" --args --profile-directory="Profile 1" \
  --app="http://localhost:8787/?key=$KEY" \
  --window-position=0,0 --window-size=$SW,$SH
sleep 3
osascript -e 'tell application "Google Chrome" to activate'
