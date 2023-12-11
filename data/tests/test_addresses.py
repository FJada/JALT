import pytest
import data.addresses as am
import data.db_connect as dbc

@pytest.fixture(scope='function')
def temp_user():
    username = 'John123'
    ret = am.add_user(
        username,
        {'address': '123 Main St, New York, NY 10001', 'nearest_train_station': 'Penn Station'},
        {'address': '456 Broadway, New York, NY 10002', 'nearest_train_station': 'Grand Central Terminal'},
        '123456'
    )
    assert am.user_exists(username), "User should be added successfully."
    yield username
    am.del_user(username)
    assert not am.user_exists(username), "User should be deleted successfully."


def test_gen_id():
    acc_id = am._gen_id()
    assert isinstance(acc_id, str)
    assert len(acc_id) > 0


def test_add_user():
    new_username = 'JohnSmith'
    account_id = am._gen_id()
    ret = am.add_user(
        new_username,
        {'address': '789 Broadway, New York, NY 10003', 'nearest_train_station': 'Times Square'},
        {'address': '101 Park Ave, New York, NY 10004', 'nearest_train_station': 'Union Square'},
        account_id
    )
    assert am.user_exists(new_username), "User should be added successfully."
    assert isinstance(ret, dict)
    am.del_user(new_username)
    assert not am.user_exists(new_username), "User should be deleted successfully."


def test_user_exists():
    username = 'Johnny'
    assert not am.user_exists(username)

