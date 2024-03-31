"""
users.py: this module interfaces to our user data.
"""

import random
import string
import data.db_connect as dbc

USERS_COLLECTION = 'users'
ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * ID_LEN
USERNAME = 'username'
ACCOUNT_ID = 'accountId'
PASSWORD = 'password'
HOME = 'home'
WORK = 'work'


def _gen_id() -> str:
    """
    Generates an id per entry for mongodb
    """
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def gen_account_id() -> str:
    """
    Returns acc123456789 to identify each account by unique id
    """
    account = 'acc'
    rand_part = random.randint(0, BIG_NUM)
    return account + str(rand_part)

def gen_password(length=12):
    """
    Generate a random password 12 characters long.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    
    return password

def get_users_as_dict() -> dict:
    """
    Returns dictionary of all users in database
    """
    dbc.connect_db()
    return dbc.fetch_all_as_dict(USERNAME, USERS_COLLECTION)


def get_user_by_username(username: str) -> dict:
    """
    Retrieve user information by username
    """
    dbc.connect_db()
    return dbc.fetch_one(USERS_COLLECTION, {USERNAME: username})


def get_user_by_account_id(account_id: str) -> dict:
    """
    Retrieve user information by account id
    """
    dbc.connect_db()
    return dbc.fetch_one(USERS_COLLECTION, {ACCOUNT_ID: account_id})


def username_exists(username: str) -> dict:
    """
    Returns boolean is account user exists
    """
    return get_user_by_username(username) is not None


def add_user(username: str, account_id: str, password: str) -> bool:
    if username_exists(username):
        raise ValueError(f'Duplicate username: {username=}, please choose another username!')
    if not username:
        raise ValueError('Username may not be blank')
    user = {}
    user[USERNAME] = username
    user[ACCOUNT_ID] = account_id
    user[PASSWORD] = password
    dbc.connect_db()
    _id = dbc.insert_one(USERS_COLLECTION, user)
    return _id is not None


def add_home_address(username: str, home_address: str):
    if not username_exists(username):
        raise ValueError(f'Update failure: {username} not in database.')
    else:
        dbc.connect_db()
        return dbc.update_doc(USERS_COLLECTION, {USERNAME: username},
                              {HOME: home_address})


def del_user(username: str, delete_flag: bool):
    if delete_flag:
        if username_exists(username):
            return dbc.del_one(USERS_COLLECTION, {USERNAME: username})
        else:
            raise ValueError(f'Delete failure: {username} not in database.')
    else:
        raise ValueError('Delete skipped')


def get_username(user: dict):
    return user.get(USERNAME, '')


def get_account_id(user: dict):
    return user.get(ACCOUNT_ID, '')


def get_home_address(user: dict):
    return user.get(HOME, '')


def get_password(user: dict):
    return user.get(PASSWORD, '')