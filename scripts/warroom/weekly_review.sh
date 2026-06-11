#!/bin/zsh
set -uo pipefail
WS="/Users/danieldanut/Agentic Workspace"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
LOG="$WS/Planning/logs/weekly_$(date +%F).log"
cd "$WS"
{
  echo "=== weekly review $(date) ==="
  claude -p "$(cat "$WS/Planning/prompts/weekly_review.md")" \
    --model sonnet --permission-mode bypassPermissions --max-turns 50
} >> "$LOG" 2>&1
[[ $? -ne 0 ]] && "$WS/scripts/warroom/alert.sh" "Weekly review FAILED. Log: $LOG"
exit 0
