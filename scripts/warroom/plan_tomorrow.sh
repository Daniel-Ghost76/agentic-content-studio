#!/bin/zsh
# Build TOMORROW's plan now (triggered from the app's "Plan tomorrow today" button)
set -uo pipefail
WS="/Users/danieldanut/Agentic Workspace"
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
TARGET="${1:?target date required}"
TODAY=$(date +%F)
LOG="$WS/Planning/logs/plantomorrow_$TARGET.log"
PROMPT_FILE=$(mktemp /tmp/daybreak_plan_XXXX.md)
{
  echo "TARGET DATE OVERRIDE: You are building the plan for $TARGET (tomorrow), triggered manually by Daniel this evening via the 'Plan tomorrow today' button."
  echo "Wherever the instructions below say 'today', use $TARGET. Wherever they say 'yesterday', use $TODAY ($TODAY's file is the carry-over source)."
  echo "Read Planning/Daily/$TODAY.json fields 'improve' AND 'notes' — Daniel's feedback and forward instructions. Advisory only: goals.yaml ranking wins any conflict, but honor reasonable timing/ordering/task requests."
  echo "Carry every priority from $TODAY with progress < 100, noting remaining % in the new task text and sizing blocks for the remainder."
  echo "Calendar work targets $TARGET: read $TARGET 00:00–23:59 and write/move ⚔️ blocks for $TARGET only."
  echo "---"
  cat "$WS/Planning/prompts/morning_build.md"
} > "$PROMPT_FILE"
cd "$WS"
{
  echo "=== plan-tomorrow ($TARGET) started $(date) ==="
  claude -p "$(cat "$PROMPT_FILE")" \
    --model sonnet --permission-mode bypassPermissions --max-turns 100
  echo "=== exit $? $(date) ==="
} >> "$LOG" 2>&1
rm -f "$PROMPT_FILE"
[[ -f "$WS/Planning/Daily/$TARGET.json" ]] || "$WS/scripts/warroom/alert.sh" "Plan-tomorrow FAILED for $TARGET. Log: $LOG"
