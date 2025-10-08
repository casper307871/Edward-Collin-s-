#!/usr/bin/env bash
# protected_clone.sh
# Usage: ACCESS_TOKEN=xxx LOG_ENDPOINT=https://your.server/clone-log ./protected_clone.sh git@your.git:edward.git destdir
set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: ACCESS_TOKEN=xxx LOG_ENDPOINT=https://server/clone-log ./protected_clone.sh <repo> <dest>"
  exit 1
fi

REPO="$1"
DEST="$2"
TOKEN="${ACCESS_TOKEN:-}"
LOG_ENDPOINT="${LOG_ENDPOINT:-}"

if [ -z "$TOKEN" ] || [ -z "$LOG_ENDPOINT" ]; then
  echo "ACCESS_TOKEN and LOG_ENDPOINT environment variables must be set."
  exit 2
fi

# Optionally call server to validate token before cloning
resp=$(curl -fsS -X POST "$LOG_ENDPOINT/validate" -H "Authorization: Bearer $TOKEN" -d "{\"repo\":\"$REPO\"}" || true)
if [ -z "$resp" ]; then
  echo "Token validation failed or server unreachable."
  exit 3
fi

# Register clone attempt (non-blocking)
curl -s -X POST "$LOG_ENDPOINT/record" -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"repo\":\"$REPO\",\"dest\":\"$DEST\",\"who\":\"$(whoami)\",\"time\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" >/dev/null || true

# Do the clone normally but using a custom SSH wrapper that forces the use of an authorized key (optional)
GIT_SSH_COMMAND='ssh -o BatchMode=yes -o PreferredAuthentications=publickey' git clone "$REPO" "$DEST"
