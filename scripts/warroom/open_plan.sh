#!/bin/zsh
set -uo pipefail
WS="/Users/danieldanut/Agentic Workspace"
caffeinate -u -t 5   # light the display (pmset woke the Mac at 03:23)
if [[ ! -f "$WS/Planning/Daily/$(date +%F).json" ]]; then
  "$WS/scripts/warroom/alert.sh" "4am pop: no plan for today — morning build failed?"
  exit 1
fi
KEY=$(cat "$WS/Planning/app-data/secret.txt")
open -na "Google Chrome" --args --profile-directory="Profile 1" \
  --app="http://localhost:8787/?key=$KEY" --start-fullscreen
