#!/bin/zsh
# Rolling 7-day horizon: detailed accomplishment-based rebuild of tomorrow +
# quota-distributed plans for days +2..+7, all written to the real calendar.
# Runs on Sonnet — it deletes/rebuilds real calendar events.
set -uo pipefail
WS="/Users/danieldanut/Agentic Workspace"
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
LOG="$WS/Planning/logs/horizon_$(date +%F).log"
cd "$WS"
{
  echo "=== horizon $(date) ==="
  claude -p "$(cat "$WS/Planning/prompts/horizon.md")" \
    --model sonnet --permission-mode bypassPermissions --max-turns 200
  echo "=== exit $? $(date) ==="
} >> "$LOG" 2>&1
# success = at least tomorrow's plan exists
TOM=$(date -v+1d +%F 2>/dev/null || date -d "+1 day" +%F)
[[ -f "$WS/Planning/Daily/$TOM.json" ]] || "$WS/scripts/warroom/alert.sh" "Horizon FAILED. Log: $LOG"
