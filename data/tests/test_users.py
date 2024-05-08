import pytest

import data.users as us


@pytest.fixture(scope='function')
def temp_user():
    username = 'Test'
    account_id = us.gen_account_id()
    password = us.gen_password()
    ret = us.add_user(username, account_id, password)
    yield username
    if us.username_exists(username):
        us.del_user(username, 1)


def test_add_home_address(temp_user):
    home_address = '217 Spencer Street'
    us.add_home_address(temp_user, home_address)
    updated_user = us.get_user_by_username(temp_user)
    assert us.get_home_address(updated_user) == home_address


def test_get_users_as_dict():
    users = us.get_users_as_dict()
    assert isinstance(users, dict)
    for user in users: 
        assert isinstance(user, str)
        assert isinstance(users[user], dict)
    

def test_get_user(temp_user):
    user = us.get_user_by_username(temp_user)
    assert isinstance(user, dict)


def test_gen_id():
    _id = us._gen_id()
    assert isinstance(_id, str)
    assert len(_id) == us.ID_LEN

def test_gen_password():
    password = us.gen_password()
    assert password is not None
   
    
def test_add_dup_user(temp_user):
    account_id = us.gen_account_id()
    password = us.gen_password()
    with pytest.raises(ValueError):
        us.add_user(temp_user, account_id, password)


def test_gen_account_id():
    account_id = us.gen_account_id()
    assert account_id is not None


def test_add_blank_user():
    with pytest.raises(ValueError):
        us.add_user('', 4, '')


def test_del_user(temp_user):
    username = temp_user
    us.del_user(username, 1)
    assert not us.username_exists(username)


def test_del_user_false(temp_user):
    username = temp_user
    with pytest.raises(ValueError):
        us.del_user(username, 0)


def test_del_user_not_there():
    username = 'arfghbvdfs'
    with pytest.raises(ValueError):
        us.del_user(username, 1)


def test_get_user_by_username(temp_user):
    user = us.get_user_by_username(temp_user)
    assert isinstance(user, dict)


def test_update_username(temp_user):
    new_username = 'NewTestUsername'
    result = us.update_username(temp_user, new_username)
    assert result == "Username updated successfully."


def test_get_user_by_account_id(temp_user):
    user = us.get_user_by_username(temp_user)
    account_id = us.get_account_id(user)
    user = us.get_user_by_account_id(account_id)
    assert isinstance(user, dict)


def test_add_user_blank_username_error():
    with pytest.raises(ValueError):
        us.add_user('', 'test_account_id', 'test_password')
