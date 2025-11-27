"""Helper script to run the Flask app on port 5001 for local testing.

Use this when port 5000 is occupied. This file is not used in production; it's
only for local debugging and testing.
"""
from tracker import app

if __name__ == '__main__':
    # Bind to localhost only for safety
    app.run(debug=True, host='127.0.0.1', port=5001)
