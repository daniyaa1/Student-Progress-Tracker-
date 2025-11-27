import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tracker import app, db
import json

def run_tests():
    print('Starting API integration test...')
    with app.app_context():
        # ensure fresh DB for test
        db.drop_all()
        db.create_all()

    with app.test_client() as c:
        # 1) GET empty
        r = c.get('/api/tasks')
        assert r.status_code == 200
        data = r.get_json()
        assert isinstance(data, list) and len(data) == 0
        print('GET /api/tasks -> OK (empty)')

        # 2) POST create
        payload = {'name':'Test Task','due':'2030-01-01','subj':'Test','notes':'hello','priority':'high'}
        r = c.post('/api/tasks', data=json.dumps(payload), content_type='application/json')
        assert r.status_code == 200
        data = r.get_json()
        assert any(t['name']=='Test Task' for t in data)
        task_id = data[-1]['id']
        print('POST /api/tasks -> OK (created id={})'.format(task_id))

        # 3) PUT update (mark done)
        update = {'name':'Test Task','due':'2030-01-01','subj':'Test','done':True,'notes':'hello','priority':'high'}
        r = c.put(f'/api/tasks/{task_id}', data=json.dumps(update), content_type='application/json')
        assert r.status_code == 200
        r = c.get('/api/tasks')
        data = r.get_json()
        t = next(x for x in data if x['id']==task_id)
        assert t['done'] is True
        print('PUT /api/tasks/{0} -> OK (done=True)'.format(task_id))

        # 3b) PUT set milestone
        update_m = {'milestone': True}
        r = c.put(f'/api/tasks/{task_id}', data=json.dumps(update_m), content_type='application/json')
        assert r.status_code == 200
        r = c.get('/api/tasks')
        data = r.get_json()
        t = next(x for x in data if x['id']==task_id)
        assert t.get('milestone') is True
        print('PUT /api/tasks/{0} -> OK (milestone=True)'.format(task_id))

        # 4) DELETE
        r = c.delete(f'/api/tasks/{task_id}')
        assert r.status_code == 200
        r = c.get('/api/tasks')
        data = r.get_json()
        assert not any(x['id']==task_id for x in data)
        print('DELETE /api/tasks/{0} -> OK (removed)'.format(task_id))

    print('All integration tests passed.')

if __name__ == '__main__':
    run_tests()
