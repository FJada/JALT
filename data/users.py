import random
import string
import data.db_connect as dbc
import logging

# Directly specify the absolute path to the error log file
log_file_path = './JALT/server/error.log'

# Configure the logger
logging.basicConfig(filename=log_file_path, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# CONSTANTS
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
    try:
        _id = random.randint(0, BIG_NUM)
        _id = str(_id)
        _id = _id.rjust(ID_LEN, '0')
        return _id
    except Exception as e:
        logger.error(f"Error generating ID: {str(e)}")
        raise


def gen_account_id() -> str:
    """
    Returns an account id to identify each account by unique id
    """
    try:
        account = 'acc'
        rand_part = random.randint(0, BIG_NUM)
        return account + str(rand_part)
    except Exception as e:
        logger.error(f"Error generating account ID: {str(e)}")
        raise


def gen_password(length=12):
    """
    Generates a random password 12 characters long.
    """
    try:
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password
    except Exception as e:
        logger.error(f"Error generating password: {str(e)}")
        raise


def get_users_as_dict() -> dict:
    """
    Returns dictionary of all users in database
    """
    try:
        dbc.connect_db()
        return dbc.fetch_all_as_dict(USERNAME, USERS_COLLECTION)
    except Exception as e:
        logger.error(f"Error fetching users from database: {str(e)}")
        raise


def get_user_by_username(username: str) -> dict:
    """
    Retrieve user information by username
    """
    try:
        dbc.connect_db()
        return dbc.fetch_one(USERS_COLLECTION, {USERNAME: username})
    except Exception as e:
        logger.error(f"Error fetching user by username '{username}': {str(e)}")
        raise


def get_user_by_account_id(account_id: str) -> dict:
    """
    Retrieve user information by account id
    """
    try:
        dbc.connect_db()
        return dbc.fetch_one(USERS_COLLECTION, {ACCOUNT_ID: account_id})
    except Exception as e:
        logger.error(f"Error fetching user by account ID '{account_id}': {str(e)}")
        raise


def get_user_by_password(password: str) -> dict:
    """
    Retrieve user information by password
    """
    try:
        dbc.connect_db()
        if not password:
            raise ValueError('Password may not be blank')
        return dbc.fetch_one(USERS_COLLECTION, {PASSWORD: password})
    except Exception as e:
        logger.error(f"Error fetching user by password: {str(e)}")
        raise


def password_exists(password: str) -> bool:
    """
    Returns boolean if account password exists
    """
    try:
        return get_user_by_password(password) is not None
    except Exception as e:
        logger.error(f"Error checking password existence: {str(e)}")


def username_exists(username: str) -> bool:
    """
    Returns boolean if account user exists
    """
    try:
        return get_user_by_username(username) is not None
    except Exception as e:
        logger.error(f"Error checking username existence: {str(e)}")
        raise


def add_user(username: str, account_id: str, password: str) -> bool:
    """
    Adds a new user to the database
    """
    try:
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
    except Exception as e:
        logger.error(f"Error adding user '{username}': {str(e)}")
        raise


def add_home_address(username: str, home_address: str):
    """
    Adds home address to user by username
    """
    try:
        if not username_exists(username):
            raise ValueError(f"Update failure: '{username}' not in database.")
        else:
            dbc.connect_db()
            return dbc.update_doc(USERS_COLLECTION, {USERNAME: username}, {HOME: home_address})
    except Exception as e:
        logger.error(f"Error adding home address for '{username}': {str(e)}")
        raise


def del_user(username: str, delete_flag: bool):
    """
    Deletes user from database
    """
    try:
        if delete_flag:
            if username_exists(username):
                return dbc.del_one(USERS_COLLECTION, {USERNAME: username})
            else:
                raise ValueError(f"Delete failure: '{username}' not in database.")
        else:
            raise ValueError('Delete skipped')
    except Exception as e:
        logger.error(f"Error deleting user '{username}': {str(e)}")
        raise


def update_username(username: str, new_username: str):
    """
    Updates user's username in database
    """
    try:
        # Check if the new username already exists
        if username_exists(new_username):
            return "Username already exists. Please choose a different one."
        if not new_username:
            return "New username cannot be empty."
        elif new_username == username:
            return "New username cannot be the same as the current username."
        user = get_user_by_username(username)
        if user:
            # Update the username in the database
            dbc.connect_db()
            result = dbc.update_doc(USERS_COLLECTION, {USERNAME: username}, {USERNAME: new_username})
            if result.modified_count == 1:
                return "Username updated successfully."
            else:
                return "Failed to update username."
        else:
            return "Username not found."
    except Exception as e:
        logger.error(f"Error updating username '{username}': {str(e)}")
        return "An error occurred while updating the username."


def get_username(user: dict) -> str:
    """
    Retrieves username from user
    """
    return user.get(USERNAME, '')


def get_account_id(user: dict) -> str:
    """
    Retrieves account id from user
    """
    return user.get(ACCOUNT_ID, '')


def get_home_address(user: dict) -> str:
    """
    Retrieves home address from user
    """
    return user.get(HOME, '')


def get_password(user: dict) -> str:
    """
    Retrieves password from user
    """
    return user.get(PASSWORD, '')
