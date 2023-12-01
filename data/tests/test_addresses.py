import pytest

import data.addresses as am

@pytest.fixture(scope='function')
def temp_user():
    username = am._get_test_name()
    ret = am.add_user(
        username,
        '123456',
        {'address': '123 Main St, New York, NY 10001', 'nearest_train_station': 'Penn Station'},
        {'address': '456 Broadway, New York, NY 10002', 'nearest_train_station': 'Grand Central Terminal'}
    )
    yield username
    if am.user_exists(username):
        am.del_user(username)


def test_get_test_name():
    name = am._get_test_name()
    assert isinstance(name, str)
    assert len(name) > 0


def test_gen_id():
    _id = am._gen_id()
    assert isinstance(_id, str)
    assert len(_id) == am.ID_LEN


def test_get_test_game():
    assert isinstance(am.get_test_game(), dict)


def test_get_users(temp_user):
    users = am.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0
    for user in users:
        assert isinstance(user, str)
        assert isinstance(users[user], dict)
    assert am.user_exists(temp_user)


def test_add_user_dup_name(temp_user):
    """
    Make sure a duplicate username raises a ValueError.
    `temp_user` is the username of the user that our fixture added.
    """
    with pytest.raises(ValueError):
        am.add_user(
            temp_user,
            '789012',
            {'address': '789 Broadway, New York, NY 10003', 'nearest_train_station': 'Times Square'},
            {'address': '101 Park Ave, New York, NY 10004', 'nearest_train_station': 'Union Square'}
        )


def test_add_user_blank_name():
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


ADD_USERNAME = 'NewUser'


def test_add_user():
    new_username = am._get_test_name()
    ret = am.add_user(
        new_username,
        '789012',
        {'address': '789 Broadway, New York, NY 10003', 'nearest_train_station': 'Times Square'},
        {'address': '101 Park Ave, New York, NY 10004', 'nearest_train_station': 'Union Square'}
    )
    assert am.user_exists(new_username)
    assert isinstance(ret, bool)
    am.del_user(new_username)


def test_del_user(temp_user):
    username = temp_user
    am.del_user(username)
    assert not am.user_exists(username)


def test_del_user_not_there():
    username = am._get_test_name()
    with pytest.raises(ValueError):
        am.del_user(username)
