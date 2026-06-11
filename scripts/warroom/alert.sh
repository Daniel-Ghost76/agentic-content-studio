#!/bin/zsh
# Telegram alert. Usage: alert.sh "message"
set -uo pipefail
source "$HOME/.claude/.env" 2>/dev/null || true
MSG="${1:-War Room alert (no message)}"
if [[ -n "${TELEGRAM_BOT_TOKEN:-}" && -n "${TELEGRAM_CHAT_ID:-}" ]]; then
  curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d chat_id="${TELEGRAM_CHAT_ID}" -d text="⚔️ ${MSG}" >/dev/null
else
  echo "alert.sh: TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID missing; msg was: ${MSG}" >&2
fi
