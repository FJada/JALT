import pytest
import data.addresses as am

@pytest.fixture(scope='function')
def temp_user():
    username = am._gen_id()
    ret = am.add_user(
        username,
        '123456',
        {'address': '123 Main St, New York, NY 10001', 'nearest_train_station': 'Penn Station'},
        {'address': '456 Broadway, New York, NY 10002', 'nearest_train_station': 'Grand Central Terminal'}
    )
    assert am.user_exists(username), "User should be added successfully."
    yield username
    am.del_user(username)
    assert not am.user_exists(username), "User should be deleted successfully."

def test_get_test_name():
    name = am._gen_id()
    assert isinstance(name, str)
    assert len(name) > 0

def test_add_user_with_blank_username():
    """
    Make sure a blank username raises a ValueError.
    """
    with pytest.raises(ValueError):
        am.add_user(
            '',
            '789012',
            {'address': '789 Broadway, New York, NY 10003', 'nearest_train_station': 'Times Square'},
            {'address': '101 Park Ave, New York, NY 10004', 'nearest_train_station': 'Union Square'}
        )

def test_add_user():
    new_username = am._gen_id()
    ret = am.add_user(
        new_username,
        '789012',
        {'address': '789 Broadway, New York, NY 10003', 'nearest_train_station': 'Times Square'},
        {'address': '101 Park Ave, New York, NY 10004', 'nearest_train_station': 'Union Square'}
    )
    assert am.user_exists(new_username), "User should be added successfully."
    assert isinstance(ret, dict)
    am.del_user(new_username)
    assert not am.user_exists(new_username), "User should be deleted successfully."

def test_del_user_not_there():
    username = am._gen_id()
    with pytest.raises(ValueError):
        am.del_user(username)
