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
NOTES_W=420

# 1. type today's checklist into the Notes note (REAL checkboxes; takes ~10s, steals focus)
osascript "$WS/scripts/warroom/notes_checklist.scpt" "$PLAN" || \
  "$WS/scripts/warroom/alert.sh" "4am pop: Notes checklist write failed (Accessibility granted for /usr/bin/osascript?)"

# 2. float the Notes window on the right
osascript -e "tell application \"Notes\" to set bounds of front window to {$((SW - NOTES_W - 10)), 40, $((SW - 10)), $((SH * 7 / 10))}" 2>/dev/null || true

# 3. hide every other app
osascript -e 'tell application "System Events" to set visible of (every process whose visible is true and name is not "Google Chrome" and name is not "Notes" and name is not "Finder") to false' 2>/dev/null || true

# 4. close stale War Room windows, open the planner sized beside the note, bring it FRONT
osascript -e 'tell application "Google Chrome" to close (every window whose URL of active tab contains "8787")' 2>/dev/null || true
open -na "Google Chrome" --args --profile-directory="Profile 1" \
  --app="http://localhost:8787/?key=$KEY" \
  --window-position=0,0 --window-size=$((SW - NOTES_W - 30)),$SH
sleep 4
osascript -e 'tell application "Google Chrome" to activate'
