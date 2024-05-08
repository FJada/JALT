import random
import data.db_connect as dbc
import logging

log_file_path = './JALT/server/error.log'

# Configure the logger
logging.basicConfig(filename=log_file_path, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

ROUTES_COLLECTION = 'routes'
ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000
ROUTE_ID = 'routeId'
STARTING_POINT = 'startingPoint'
ENDING_POINT = 'endingPoint'


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


def gen_route_id() -> str:
    """
    Returns a unique route ID.
    """
    try:
        route = 'route'
        rand_part = random.randint(0, BIG_NUM)
        return route + str(rand_part)
    except Exception as e:
        logger.error(f"Error generating route ID: {str(e)}")
        raise


def get_routes_as_dict() -> dict:
    """
    Returns a dictionary of all routes in the database.
    """
    try:
        dbc.connect_db()
        return dbc.fetch_all_as_dict(ROUTE_ID, ROUTES_COLLECTION)
    except Exception as e:
        logger.error(f"Error fetching routes from database: {str(e)}")
        raise


def get_route_by_route_id(route_id: str) -> dict:
    """
    Retrieves route information by route ID.
    """
    try:
        dbc.connect_db()
        return dbc.fetch_one(ROUTES_COLLECTION, {ROUTE_ID: route_id})
    except Exception as e:
        logger.error(f"Error fetching route by route ID '{route_id}': {str(e)}")
        raise


def route_exists(route_id: str) -> bool:
    """
    Checks if a route exists in the database based on route ID.
    """
    try:
        return get_route_by_route_id(route_id) is not None
    except Exception as e:
        logger.error(f"Error checking route existence: {str(e)}")
        raise


def add_route(starting_point: str, ending_point: str, route_id: str) -> bool:
    """
    Adds a new route to the database.
    """
    try:
        if route_exists(route_id):
            raise ValueError(f'Duplicate route: {route_id=}, please choose another route ID!')
        if not route_id:
            raise ValueError('Route ID may not be blank')
        route = {STARTING_POINT: starting_point, ENDING_POINT: ending_point, ROUTE_ID: route_id}
        dbc.connect_db()
        _id = dbc.insert_one(ROUTES_COLLECTION, route)
        return _id is not None
    except Exception as e:
        logger.error(f"Error adding route '{route_id}': {str(e)}")
        raise


def update_ending_point(route_id: str, new_ending_point: str):
    """
    Updates the ending point of a route in the database.
    """
    try:
        if not route_exists(route_id):
            raise ValueError(f'Update failure: {route_id} not in database.')
        else:
            dbc.connect_db()
            return dbc.update_doc(ROUTES_COLLECTION, {ROUTE_ID: route_id}, {ENDING_POINT: new_ending_point})
    except Exception as e:
        logger.error(f"Error updating ending point for route '{route_id}': {str(e)}")
        raise


def update_starting_point(route_id: str, new_starting_point: str):
    """
    Updates the starting point of a route in the database.
    """
    try:
        if not route_exists(route_id):
            raise ValueError(f'Update failure: {route_id} not in database.')
        else:
            dbc.connect_db()
            return dbc.update_doc(ROUTES_COLLECTION, {ROUTE_ID: route_id}, {STARTING_POINT: new_starting_point})
    except Exception as e:
        logger.error(f"Error updating starting point for route '{route_id}': {str(e)}")
        raise


def del_route(route_id: str):
    """
    Deletes a route from the database.
    """
    try:
        if route_exists(route_id):
            return dbc.del_one(ROUTES_COLLECTION, {ROUTE_ID: route_id})
        else:
            raise ValueError(f'Delete failure: {route_id} not in database.')
    except Exception as e:
        logger.error(f"Error deleting route '{route_id}': {str(e)}")
        raise


def get_route_id(route: dict) -> str:
    """
    Returns the route ID from a route dictionary.
    """
    try:
        return route.get(ROUTE_ID, '')
    except Exception as e:
        logger.error(f"Error getting route ID from route dictionary: {str(e)}")
        raise


def get_starting_point(route: dict) -> str:
    """
    Returns the starting point from a route dictionary.
    """
    try:
        return route.get(STARTING_POINT, '')
    except Exception as e:
        logger.error(f"Error getting starting point from route dictionary: {str(e)}")
        raise


def get_ending_point(route: dict) -> str:
    """
    Returns the ending point from a route dictionary.
    """
    try:
        return route.get(ENDING_POINT, '')
    except Exception as e:
        logger.error(f"Error getting ending point from route dictionary: {str(e)}")
        raise
