"""
addresses.py: the interface to our user data.
"""
import random

import data.db_connect as dbc

USERS_COLLECTION = 'Addresses'

ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * ID_LEN
USERNAME = 'username'
ACCOUNT_ID = 'account_id'
ADDRESSES = 'addresses'
HOME = 'home'
WORK = 'work'
ADDRESS = 'address'
NEAREST_TRAIN_STATION = 'nearest_train_station'


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def get_users() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(USERNAME, USERS_COLLECTION)


def user_exists(username: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(USERS_COLLECTION, {USERNAME: username})


def add_user(username: str, account_id: str,
             home_address: dict, work_address: dict) -> bool:
    if user_exists(username):
        raise ValueError(f'Duplicate username: {username=}')
    if not username:
        raise ValueError('Username may not be blank')
    user = {
        USERNAME: username,
        ACCOUNT_ID: account_id,
        ADDRESSES: {
            HOME: home_address,
            WORK: work_address
        }
    }
    dbc.connect_db()
    _id = dbc.insert_one(USERS_COLLECTION, user)
    return _id is not None


def del_user(username: str):
    if user_exists(username):
        return dbc.del_one(USERS_COLLECTION, {USERNAME: username})
    else:
        raise ValueError(f'Delete failure: {username} not in database.')


def main():
    print(get_users())


if __name__ == '__main__':
    main()
