# Student Progress Tracker

A small Flask-based web app to track study tasks, promote milestones, and visualize progress.

This repository contains a working local-development app (Flask + SQLite) and a single-page frontend that uses the API for persistence.

## Highlights / features added
- Task management: add, edit, delete tasks with name, due date, subject
- Notes & priority: tasks store optional notes and priority (low/medium/high)
- Milestones: promote important tasks to milestones (persisted server-side)
- Progress visualization: subject breakdown and 7-day completed trend charts (Chart.js)
- Medals & Streaks: daily medals (🥇/🥈/🥉) and streak computation shown in UI
- API: REST endpoints at `/api/tasks` (GET/POST) and `/api/tasks/<id>` (PUT/DELETE)
- Dev conveniences: small SQLite-friendly dev-time ALTER helper for local schema changes

## Quick start (development)

1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app locally (development):

```bash
# from the project root
python tracker.py
```

Open http://127.0.0.1:5000 in your browser. The UI is served from `templates/index.html` and static assets are in `static/`.

## Run integration tests (local)

```bash
source .venv/bin/activate
python tests/api_integration_test.py
```

## Files of interest
- `tracker.py` — Flask app and REST API
- `templates/index.html` — frontend UI (wired to the Flask API)
- `static/tracker.css` — styles and UI assets
- `tests/api_integration_test.py` — integration tests (create/update/milestone/delete)

Made by Daniya
