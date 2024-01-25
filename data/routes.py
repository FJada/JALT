import random
import data.db_connect as dbc

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
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def gen_route_id() -> str:
    route = 'route'
    rand_part = random.randint(0, BIG_NUM)
    return route + str(rand_part)


def get_routes_as_dict() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(ROUTE_ID, ROUTES_COLLECTION)


def get_route_by_route_id(route_id: str) -> dict:
    dbc.connect_db()
    return dbc.fetch_one(ROUTES_COLLECTION, {ROUTE_ID: route_id})


def route_exists(route_id: str) -> dict:
    """
    Returns boolean is account user exists
    """
    return get_route_by_route_id(route_id) is not None


def add_route(starting_point: str, ending_point: str, route_id: str) -> bool:
    if route_exists(route_id):
        raise ValueError(f'Duplicate route: {route_id=}, please choose another username!')
    if not route_id:
        raise ValueError('Route Id may not be blank')
    route = {}
    route[STARTING_POINT] = starting_point
    route[ENDING_POINT] = ending_point
    route[ROUTE_ID] = route_id
    dbc.connect_db()
    _id = dbc.insert_one(ROUTES_COLLECTION, route)
    return _id is not None


def update_ending_point(route_id: str, new_ending_point: str):
    if not route_exists(route_id):
        raise ValueError(f'Update failure: {route_id} not in database.')
    else:
        dbc.connect_db()
        return dbc.update_doc(ROUTES_COLLECTION, {ROUTE_ID: route_id},
                              {ENDING_POINT: new_ending_point})


def update_starting_point(route_id: str, new_starting_point: str):
    if not route_exists(route_id):
        raise ValueError(f'Update failure: {route_id} not in database.')
    else:
        dbc.connect_db()
        return dbc.update_doc(ROUTES_COLLECTION, {ROUTE_ID: route_id},
                              {STARTING_POINT: new_starting_point})


def del_route(route_id: str):
    if route_exists(route_id):
        return dbc.del_one(ROUTES_COLLECTION, {ROUTE_ID: route_id})
    else:
        raise ValueError(f'Delete failure: {route_id} not in database.')


def get_route_id(route: dict):
    return route.get(ROUTE_ID, '')


def get_starting_point(route: dict):
    return route.get(STARTING_POINT, '')


def get_ending_point(route: dict):
    return route.get(ENDING_POINT, '')
