from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    r = client.get('/')
    assert r.status_code == 200

def test_register_and_list():
    # create admin first
    client.post('/auth/register', json={'username':'admin','password':'adminpass','role':'admin'})
    login = client.post('/auth/login', json={'username':'admin','password':'adminpass'}).json()
    token = login.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    # register bulk
    r = client.post('/devices/register_bulk', json=[{'name':'t1','type':'temp'}], headers=headers)
    assert r.status_code == 200
    # list
    r2 = client.get('/devices', headers=headers)
    assert r2.status_code == 200
    assert isinstance(r2.json(), list)
