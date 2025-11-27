#!/usr/bin/env bash
set -euo pipefail

# Activate .venv if present
if [ -f .venv/bin/activate ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

echo "Starting Student Progress Tracker on http://127.0.0.1:5000"
python tracker.py
