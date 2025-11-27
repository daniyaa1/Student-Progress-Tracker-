"""Run a local test POST to the Flask app using the test client.

This does not require the server to be running and exercises the same
view code that the production server handles.
"""
from tracker import app

with app.app_context():
    client = app.test_client()
    res = client.post('/api/tasks', json={'name':'test-from-script','due':'2025-12-03','subj':'LocalTest'})
    print('STATUS', res.status_code)
    print(res.get_data(as_text=True))
