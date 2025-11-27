"""Vercel-compatible entrypoint wrapper.

This file exposes the Flask application object as `app` so hosting
platforms (like Vercel) which look for `app.py` can find the app.

It simply imports `app` from `tracker.py` which defines the app.
"""
from tracker import app

if __name__ == "__main__":
    # Allow running locally with `python app.py`
    app.run(debug=True)
