"""
addresses.py: the interface to our user data.
"""
import random

from flask_restx import fields

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

ADDRESS_MODEL = fields.Nested(dbc.api.model('UserAddresses', {
    HOME: fields.String(description='Home Address'),
    WORK: fields.String(description='Work Address'),
}), description='User Addresses')


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def get_users() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(USERNAME, USERS_COLLECTION)


# Use this function to check if a user exists
def user_exists(username):
    filt = {USERNAME: username}
    return dbc.fetch_one(dbc.get_collection(USERS_COLLECTION),
                         filt) is not None


# Use this function to add a user
def add_user(username, account_id, home_address, work_address):
    if not user_exists(username):
        user_collection = dbc.get_collection(USERS_COLLECTION)
        user_doc = {
            USERNAME: username,
            ACCOUNT_ID: account_id,
            ADDRESSES: {
                HOME: home_address,
                WORK: work_address
            }
        }
        dbc.insert_one(user_collection, user_doc)


# Use this function to delete a user
def del_user(username):
    if user_exists(username):
        user_collection = dbc.get_collection(USERS_COLLECTION)
        dbc.del_one(user_collection, {USERNAME: username})


def main():
    print(get_users())


if __name__ == '__main__':
    main()
