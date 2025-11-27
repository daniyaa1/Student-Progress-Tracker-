from tracker import app

def smoke():
    with app.test_client() as c:
        r = c.get('/')
        print('status', r.status_code)
        data = r.get_data(as_text=True)
        print(data[:400])

if __name__ == '__main__':
    smoke()
