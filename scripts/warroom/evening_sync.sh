#!/bin/zsh
set -uo pipefail
WS="/Users/danieldanut/Agentic Workspace"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
LOG="$WS/Planning/logs/evening_$(date +%F).log"
cd "$WS"
{
  echo "=== evening sync $(date) ==="
  claude -p "$(cat "$WS/Planning/prompts/evening_sync.md")" \
    --model sonnet --permission-mode bypassPermissions --max-turns 60
} >> "$LOG" 2>&1
[[ $? -ne 0 ]] && "$WS/scripts/warroom/alert.sh" "Evening sync FAILED. Log: $LOG"
exit 0
