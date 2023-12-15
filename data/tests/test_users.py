import pytest

import data.users as us


@pytest.fixture(scope='function')
def temp_user():
    username = 'Test'
    account_id = us.gen_account_id()
    ret = us.add_user(username, account_id)
    yield username
    if us.username_exists(username):
        us.del_user(username, 1)


def test_add_home_address(temp_user):
    home_address = '217 Spencer Street'
    us.add_home_address(temp_user, home_address)
    updated_user = us.get_user_by_username(temp_user)
    assert us.get_home_address(updated_user) == home_address


def test_get_user(temp_user):
    user = us.get_user_by_username(temp_user)
    assert isinstance(user, dict)


def test_gen_id():
    _id = us._gen_id()
    assert isinstance(_id, str)
    assert len(_id) == us.ID_LEN


def test_add_dup_user(temp_user):
    account_id = us.gen_account_id
    with pytest.raises(ValueError):
        us.user(temp_user, account_id)


def test_gen_account_id():
    account_id = us.gen_account_id
    assert account_id is not None


def test_add_blank_user():
    with pytest.raises(ValueError):
        us.add_user('', 4)
