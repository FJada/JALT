import random
import data.db_connect as dbc
import logging

# Directly specify the absolute path to the error log file
log_file_path = './server/error.log'

# Configure the logger
logging.basicConfig(filename=log_file_path, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BUSES_COLLECTION = 'buses'
ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000
BUS_NAME = 'busName'
STATION_NAME = 'stationName'
BOROUGH = 'borough'
FAVORITE = 'favorite'


def _gen_id() -> str:
    """
    Generates an id per entry for MongoDB.
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
    Returns vehicle12345678987654 to identify each account by unique id.
    """
    try:
        vehicle = 'vehicle'
        rand_part = random.randint(0, BIG_NUM)
        return vehicle + str(rand_part)
    except Exception as e:
        logger.error(f"Error generating vehicle ID: {str(e)}")
        raise


def get_buses_as_dict() -> dict:
    """
    Returns a dictionary of all buses in the database.
    """
    try:
        dbc.connect_db()
        return dbc.fetch_all_as_dict(BUS_NAME, BUSES_COLLECTION)
    except Exception as e:
        logger.error(f"Error fetching buses from database: {str(e)}")
        raise


def get_bus_by_bus_name(bus_name: str) -> dict:
    """
    Retrieve bus information by bus name.
    """
    try:
        dbc.connect_db()
        return dbc.fetch_one(BUSES_COLLECTION, {BUS_NAME: bus_name})
    except Exception as e:
        logger.error(f"Error fetching bus by bus name '{bus_name}': {str(e)}")
        raise


def bus_exists(bus_name: str) -> bool:
    """
    Checks if a bus exists in the database.
    """
    try:
        return get_bus_by_bus_name(bus_name) is not None
    except Exception as e:
        logger.error(f"Error checking bus existence: {str(e)}")
        raise


def favorite_bus(bus_name: str):
    """
    Set a bus as favorite.
    """
    try:
        if not bus_exists(bus_name):
            raise ValueError(f'Update failure: {bus_name} not in database.')
        else:
            dbc.connect_db()
            return dbc.update_doc(BUSES_COLLECTION, {BUS_NAME: bus_name}, {FAVORITE: 1})
    except Exception as e:
        logger.error(f"Error setting bus '{bus_name}' as favorite: {str(e)}")
        raise


def remove_favorite_bus(bus_name: str):
    """
    Remove a bus from favorites.
    """
    try:
        if not bus_exists(bus_name):
            raise ValueError(f'Update failure: {bus_name} not in database.')
        else:
            dbc.connect_db()
            return dbc.update_doc(BUSES_COLLECTION, {BUS_NAME: bus_name}, {FAVORITE: 0})
    except Exception as e:
        logger.error(f"Error removing bus '{bus_name}' from favorites: {str(e)}")
        raise


def add_bus(bus_name: str, borough_name: str, favorite: bool) -> bool:
    """
    Add a new bus to the database.
    """
    try:
        if bus_exists(bus_name):
            raise ValueError(f'Duplicate bus: {bus_name=}')
        if not bus_name:
            raise ValueError('Bus name may not be blank')
        bus = {BUS_NAME: bus_name, BOROUGH: borough_name, FAVORITE: 0}
        dbc.connect_db()
        _id = dbc.insert_one(BUSES_COLLECTION, bus)
        return _id is not None
    except Exception as e:
        logger.error(f"Error adding bus '{bus_name}': {str(e)}")
        raise


def del_bus(bus_name: str, delete_flag: bool):
    """
    Delete a bus from the database.
    """
    try:
        if delete_flag:
            if bus_exists(bus_name):
                return dbc.del_one(BUSES_COLLECTION, {BUS_NAME: bus_name})
            else:
                raise ValueError(f'Delete failure: {bus_name} not in database.')
        else:
            raise ValueError('Delete skipped')
    except Exception as e:
        logger.error(f"Error deleting bus '{bus_name}': {str(e)}")
        raise


def get_bus_name(bus: dict):
    """
    Get the name of a bus from its dictionary representation.
    """
    return bus.get(BUS_NAME, '')


def get_favorite(bus: dict) -> bool:
    """
    Get the favorite status of a bus from its dictionary representation.
    """
    return bool(bus.get(FAVORITE, 0))


def get_bus_borough(bus: dict):
    """
    Get the borough of a bus from its dictionary representation.
    """
    return bus.get(BOROUGH, '')
