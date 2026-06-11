#!/bin/zsh
set -uo pipefail
WS="/Users/danieldanut/Agentic Workspace"
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
LOG="$WS/Planning/logs/morning_$(date +%F).log"
cd "$WS"
{
  echo "=== morning build $(date) ==="
  claude -p "$(cat "$WS/Planning/prompts/morning_build.md")" \
    --model haiku --permission-mode bypassPermissions --max-turns 100
} >> "$LOG" 2>&1
RC=$?
if [[ $RC -ne 0 || ! -f "$WS/Planning/Daily/$(date +%F).json" ]]; then
  "$WS/scripts/warroom/alert.sh" "Morning build FAILED (rc=$RC). Log: $LOG"
fi
