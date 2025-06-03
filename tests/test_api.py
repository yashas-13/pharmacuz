import json
from backend.app import app


def login(client, username, password):
    return client.post('/login', json={'username': username, 'password': password})


def test_login_and_access_manufacturer():
    client = app.test_client()
    resp = login(client, 'admin', 'adminpass')
    assert resp.status_code == 200
    token = resp.get_json()['token']

    # Access manufacturer products
    headers = {'Authorization': f'Bearer {token}'}
    resp = client.get('/manufacturer/products', headers=headers)
    assert resp.status_code == 200


def test_forbidden_access():
    client = app.test_client()
    resp = login(client, 'stockist', 'stockpass')
    assert resp.status_code == 200
    token = resp.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}
    # Super stockist trying to access manufacturer endpoint
    resp = client.get('/manufacturer/products', headers=headers)
    assert resp.status_code == 403
