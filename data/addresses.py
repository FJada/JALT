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


# returns account id between big_num and 0, used to generate account ids
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
    filt = {str(USERNAME): str(username)}
    # Connect to the database if not connected
    if not dbc.is_connected():
        dbc.connect_db()
    user_collection = str(USERS_COLLECTION)
    return dbc.fetch_one(USERS_COLLECTION, filt) is not None


# Use this function to add a user
def add_user(username, home_address, work_address, account_id=None):
    print(f"Received: username={username}, "
          f"home_address={home_address}, "
          f"work_address={work_address}, account_id={account_id}")

    if not user_exists(username):
        if account_id is None:
            account_id = _gen_id

        # user_collection = dbc.get_collection(USERS_COLLECTION)
        user_doc = {
            USERNAME: username,
            ACCOUNT_ID: account_id,
            ADDRESSES: {}
        }
        if home_address:
            user_doc[ADDRESSES][HOME] = {
                ADDRESS: home_address,
                NEAREST_TRAIN_STATION: "Some Station"
            }
        if work_address:
            user_doc[ADDRESSES][WORK] = {
                ADDRESS: work_address,
                NEAREST_TRAIN_STATION: "Some Station"
            }
        dbc.insert_one(USERS_COLLECTION, user_doc)
        print("User created successfully")
        return {"message": "User created successfully"}
    else:
        raise ValueError(f'User {username} already exists.')
        print(f"User {username} already exists.")
        return {"message": f"User {username} already exists."}


# Use this function to delete a user
def del_user(username):
    if user_exists(username):
        # user_collection = dbc.get_collection(USERS_COLLECTION)
        dbc.del_one(USERS_COLLECTION, {USERNAME: username})


def add_address(username, address_type, new_address):
    user = dbc.fetch_one(USERS_COLLECTION, {USERNAME: username})

    if user:
        addresses = user.get(ADDRESSES, {})
        addresses[address_type] = new_address

        dbc.update_one(USERS_COLLECTION, {USERNAME: username},
                       {'$set': {ADDRESSES: addresses}})
    else:
        raise ValueError(f'User {username} not found.')


def main():
    print(get_users())


if __name__ == '__main__':
    main()
