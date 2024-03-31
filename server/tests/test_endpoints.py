import server.endpoints as ep
from http import HTTPStatus
import data.users as us
import pytest

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
    new_user_data = {'username': 'test_user', 'account_id': '123456'}
    resp = TEST_CLIENT.post('/add_user', json=new_user_data)

    assert resp.status_code == HTTPStatus.OK
    resp_json = resp.get_json()
    assert 'message' in resp_json
    assert resp_json['message'] == 'User created successfully'


def test_delete_user():
    username_to_delete = 'test_user'
    resp = TEST_CLIENT.delete(f'/users/delete/{username_to_delete}')

    assert resp.status_code == HTTPStatus.OK
    resp_json = resp.get_json()
    assert username_to_delete in resp_json
    assert resp_json[username_to_delete] == 'Deleted'


def test_add_route():
    resp = TEST_CLIENT.post('/add_route', json={'starting_point': 'A', 'ending_point': 'B'})
    assert resp.status_code == HTTPStatus.OK


def test_add_home_address():
    # Choose a unique username for testing
    test_username = 'test_user_for_home_address'
    
    # Ensure the user doesn't already exist (clean state)
    # You might need to add a delete user endpoint or use a different approach depending on your implementation
    
    # Add a new user to ensure the username is available
    resp_add_user = TEST_CLIENT.post('/add_user', json={'username': test_username, 'account_id': 'test_account_id'})
    assert resp_add_user.status_code == HTTPStatus.OK

    # Send a POST request to add a home address
    resp_add_home_address = TEST_CLIENT.post('/users/home_address', json={'username': test_username, 'home_address': '123 Main St'})
    
    # Assert the response status code
    assert resp_add_home_address.status_code == HTTPStatus.OK

    # Optionally, you can check the response content or server logs for additional information

    # Clean up: Delete the test user after the test
    resp_delete_user = TEST_CLIENT.delete(f'/users/delete/{test_username}')
    assert resp_delete_user.status_code == HTTPStatus.OK

def test_get_all_users():
    # Send a GET request to the /users endpoint
    resp_get_users = TEST_CLIENT.get('/users/get_users')

    # Assert the response status code
    assert resp_get_users.status_code == HTTPStatus.OK
    

def test_get_all_routes():
    # Send a GET request to the /routes endpoint
    resp_get_routes = TEST_CLIENT.get('/routes/get_routes')

    # Assert the response status code
    assert resp_get_routes.status_code == HTTPStatus.OK


@pytest.fixture
def setup_user_with_home_address():
    # Setup logic to add a user with a home address to the system
    test_username = 'test_username'
    test_home_address = '123 Main Street'

    # Call the add_user and add_home_address functions from your application code
    us.add_user(test_username, 'test_account_id')
    us.add_home_address(test_username, test_home_address)

    # Return the username and home address for later use in tests
    return test_username, test_home_address


def test_get_home_address(setup_user_with_home_address):
    # Retrieve the username and home address from the fixture
    test_username, test_home_address = setup_user_with_home_address

    # Send a GET request to the /users/home_address/<username> endpoint
    resp_get_home_address = TEST_CLIENT.get(f'/users/home_address/{test_username}')

    # Print response details for debugging
    print(f"Response status code: {resp_get_home_address.status_code}")
    print(f"Response JSON: {resp_get_home_address.get_json()}")

    # Assert the response status code
    assert resp_get_home_address.status_code == HTTPStatus.OK
    

def test_login_with_username():
    # Add a test user
    test_username = 'test_user'
    test_account_id = 'test_account_id'
    us.add_user(test_username, test_account_id)

    # Send a POST request to login with the username
    login_response = TEST_CLIENT.post('/users/login', json={'username': test_username})

    # Assert the response status code
    assert login_response.status_code == HTTPStatus.OK

    # Clean up: Delete the test user after the test
    us.del_user(test_username, delete_flag=True)


def test_login_with_account_id():
    # Add a test user
    test_username = 'test_user'
    test_account_id = 'test_account_id'
    us.add_user(test_username, test_account_id)

    # Send a POST request to login with the account ID
    login_response = TEST_CLIENT.post('/users/login', json={'account_id': test_account_id})

    # Assert the response status code
    assert login_response.status_code == HTTPStatus.OK

    # Clean up: Delete the test user after the test
    us.del_user(test_username, delete_flag=True)


def test_login_with_invalid_credentials():
    # Send a POST request to login with invalid credentials
    login_response = TEST_CLIENT.post('/users/login', json={'username': 'invalid_username'})

    # Assert the response status code
    assert login_response.status_code == HTTPStatus.NOT_FOUND