import server.endpoints as ep
from http import HTTPStatus

TEST_CLIENT = ep.app.test_client()


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.HELLO_RESP in resp_json


def test_list_users():
    resp = TEST_CLIENT.get(ep.USERS_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


def test_endpoints():
    resp = TEST_CLIENT.get(ep.ENDPOINTS_EP)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.OPEN_ENDPOINTS in resp_json


def test_list_routes():
    resp = TEST_CLIENT.get(ep.ROUTE_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


def test_add_user():
    # Assuming you have a TEST_CLIENT for your Flask app
    new_user_data = {'username': 'test_user', 'account_id': '123456'}
    resp = TEST_CLIENT.post('/add_user', json=new_user_data)

    assert resp.status_code == HTTPStatus.OK
    resp_json = resp.get_json()
    assert 'message' in resp_json
    assert resp_json['message'] == 'User created successfully'


def test_delete_user():
    # Assuming you have a TEST_CLIENT for your Flask app
    # Assuming the user 'test_user' exists
    username_to_delete = 'test_user'
    resp = TEST_CLIENT.delete(f'/users/delete/{username_to_delete}')

    assert resp.status_code == HTTPStatus.OK
    resp_json = resp.get_json()
    assert username_to_delete in resp_json
    assert resp_json[username_to_delete] == 'Deleted'
