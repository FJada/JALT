"""
addresses.py: the interface to our user data.
"""
import random
import data.db_connect as dbc
import uuid

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
    # Connect to the database if not connected
    if not dbc.is_connected():
        dbc.connect_db()
    return dbc.fetch_all_as_dict(USERNAME, USERS_COLLECTION)


def get_all_users():
    # Connect to the database if not connected
    if not dbc.is_connected():
        dbc.connect_db()
    return dbc.fetch_all(USERS_COLLECTION)


def user_exists(username):
    filt = {USERNAME: username}
    # Connect to the database if not connected
    if not dbc.is_connected():
        dbc.connect_db()
    return dbc.fetch_one(dbc.get_collection(USERS_COLLECTION), filt) is not None


# Use this function to delete a user
def del_user(username):
    if user_exists(username):
        user_collection = dbc.get_collection(USERS_COLLECTION)
        dbc.del_one(user_collection, {USERNAME: username})


def add_address(username, address_type, new_address):
    user_collection = dbc.get_collection(USERS_COLLECTION)
    user = dbc.fetch_one(user_collection, {USERNAME: username})

    if user:
        addresses = user.get(ADDRESSES, {})
        addresses[address_type] = new_address

        dbc.update_one(user_collection, {USERNAME: username},
                       {'$set': {ADDRESSES: addresses}})
    else:
        raise ValueError(f'User {username} not found.')


def main():
    print(get_users())


if __name__ == '__main__':
    main()
