import random
import data.db_connect as dbc
import logging

log_file_path = './JALT/server/error.log'

# Configure the logger
logging.basicConfig(filename=log_file_path, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TRAINS_COLLECTION = 'trains'
ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000
TRAIN_NAME = 'trainName'
STATION_NAME = 'stationName'
BOROUGH = 'borough'
FAVORITE = 'favorite'
VEHICLE_ID = 'vehicleId'


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


def gen_vehicle_id() -> str:
    """
    Returns a randomized vehicle id to identify each account by unique id
    """
    try:
        vehicle = 'vehicle'
        rand_part = random.randint(0, BIG_NUM)
        return vehicle + str(rand_part)
    except Exception as e:
        logger.error(f"Error generating vehicle ID: {str(e)}")
        raise


def get_trains_as_dict() -> dict:
    """
    Returns a dictionary of all trains in the database.
    """
    try:
        dbc.connect_db()
        return dbc.fetch_all_as_dict(TRAIN_NAME, TRAINS_COLLECTION)
    except Exception as e:
        logger.error(f"Error fetching trains from database: {str(e)}")
        raise


def get_train_by_train_name(train_name: str) -> dict:
    """
    Retrieve train information by train name.
    """
    try:
        dbc.connect_db()
        return dbc.fetch_one(TRAINS_COLLECTION, {TRAIN_NAME: train_name})
    except Exception as e:
        logger.error(f"Error fetching train by train name '{train_name}': {str(e)}")
        raise


def train_exists(train_name: str) -> bool:
    """
    Check if a train exists by train name.
    """
    try:
        return get_train_by_train_name(train_name) is not None
    except Exception as e:
        logger.error(f"Error checking train existence: {str(e)}")
        raise


def favorite_train(train_name: str):
    """
    Mark a train as favorite.
    """
    try:
        if not train_exists(train_name):
            raise ValueError(f'Update failure: {train_name} not in database.')
        else:
            dbc.connect_db()
            return dbc.update_doc(TRAINS_COLLECTION, {TRAIN_NAME: train_name}, {FAVORITE: 1})
    except Exception as e:
        logger.error(f"Error marking train '{train_name}' as favorite: {str(e)}")
        raise


def remove_favorite_train(train_name: str):
    """
    Remove favorite status from a train by train name.
    """
    try:
        if not train_exists(train_name):
            raise ValueError(f'Update failure: {train_name} not in database.')
        else:
            dbc.connect_db()
            return dbc.update_doc(TRAINS_COLLECTION, {TRAIN_NAME: train_name}, {FAVORITE: 0})
    except Exception as e:
        logger.error(f"Error removing favorite status from train '{train_name}': {str(e)}")
        raise


def add_train(train_name: str, vehicle_id: str, favorite: bool) -> bool:
    """
    Add a new train to the database.
    """
    try:
        if train_exists(train_name):
            raise ValueError(f'Duplicate train: {train_name=}')
        if not train_name:
            raise ValueError('Train name may not be blank')
        train = {TRAIN_NAME: train_name, VEHICLE_ID: vehicle_id, FAVORITE: 0}
        dbc.connect_db()
        _id = dbc.insert_one(TRAINS_COLLECTION, train)
        return _id is not None
    except Exception as e:
        logger.error(f"Error adding train '{train_name}': {str(e)}")
        raise


def del_train(train_name: str, delete_flag: bool):
    """
    Delete a train from the database.
    """
    try:
        if delete_flag:
            if train_exists(train_name):
                return dbc.del_one(TRAINS_COLLECTION, {TRAIN_NAME: train_name})
            else:
                raise ValueError(f'Delete failure: {train_name} not in database.')
        else:
            raise ValueError('Delete skipped')
    except Exception as e:
        logger.error(f"Error deleting train '{train_name}': {str(e)}")
        raise


def get_train_name(train: dict) -> str:
    """
    Get the name of a train from its dictionary representation.
    """
    return train.get(TRAIN_NAME, '')


def get_favorite(train: dict) -> bool:
    """
    Get the favorite status of a train from its dictionary representation.
    """
    return bool(train.get(FAVORITE, 0))
