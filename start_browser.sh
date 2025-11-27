#!/usr/bin/env bash
set -euo pipefail

PORT=${1:-5000}
URL="http://127.0.0.1:${PORT}"

# Activate venv if available
if [ -f .venv/bin/activate ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

echo "Starting Student Progress Tracker on ${URL} (background)..."

# Start server in background and redirect logs
nohup python tracker.py > server.log 2>&1 &
sleep 1

echo "Opening browser to ${URL}"
# macOS: open, Linux: xdg-open fallback
if command -v open >/dev/null 2>&1; then
  open "${URL}"
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "${URL}"
else
  echo "Please open ${URL} in your browser"
fi

echo "Server logs are in server.log"
