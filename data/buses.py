import random
import data.db_connect as dbc

BUSES_COLLECTION = 'buses'
ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000
BUS_NAME = 'busName'
STATION_NAME = 'stationName'
BOROUGH = 'borough'
FAVORITE = 'favorite'


def _gen_id() -> str:
    """
    Generates an id per entry for mongodb
    """
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def gen_vehicle_id() -> str:
    """
    Returns vehicle12345678987654 to identify each account by unique id
    """
    vehicle = 'vehicle'
    rand_part = random.randint(0, BIG_NUM)
    return vehicle + str(rand_part)


def get_buses_as_dict() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(BUS_NAME, BUSES_COLLECTION)


# def get_buses_by_borough_as_list(bus_borough: str) -> list:
#     dbc.connect_db()
#     buses_by_borough = []
#     all_buses = get_buses_as_dict()
#     for bus in all_buses:
#         new_bus_borough = bus[BOROUGH]
#         if new_bus_borough == bus_borough:
#             buses_by_borough.append(bus)


def get_bus_by_bus_name(bus_name: str) -> dict:
    dbc.connect_db()
    return dbc.fetch_one(BUSES_COLLECTION, {BUS_NAME: bus_name})


def bus_exists(bus_name: str) -> bool:
    return get_bus_by_bus_name(bus_name) is not None


def favorite_bus(bus_name: str):
    if not bus_exists(bus_name):
        raise ValueError(f'Update failure: {bus_name} not in database.')
    else:
        dbc.connect_db()
        return dbc.update_doc(BUSES_COLLECTION, {BUS_NAME: bus_name},
                              {FAVORITE: 1})


def remove_favorite_bus(bus_name: str):
    if not bus_exists(bus_name):
        raise ValueError(f'Update failure: {bus_name} not in database.')
    else:
        dbc.connect_db()
        return dbc.update_doc(BUSES_COLLECTION, {BUS_NAME: bus_name},
                              {FAVORITE: 0})


def add_bus(bus_name: str, borough_name: str, favorite: bool) -> bool:
    if bus_exists(bus_name):
        raise ValueError(f'Duplicate bus: {bus_name=}')
    if not bus_name:
        raise ValueError('Bus name may not be blank')
    bus = {}
    bus[BUS_NAME] = bus_name
    bus[BOROUGH] = borough_name
    bus[FAVORITE] = 0
    dbc.connect_db()
    _id = dbc.insert_one(BUSES_COLLECTION, bus)
    return _id is not None


def del_bus(bus_name: str, delete_flag: bool):
    if delete_flag:
        if bus_exists(bus_name):
            return dbc.del_one(BUSES_COLLECTION, {BUS_NAME: bus_name})
        else:
            raise ValueError(f'Delete failure: {bus_name} not in database.')
    else:
        raise ValueError('Delete skipped')


def get_bus_name(bus: dict):
    return bus.get(BUS_NAME, '')


def get_favorite(bus: dict) -> bool:
    return bool(bus.get(FAVORITE, 0))


def get_bus_borough(bus: dict):
    return bus.get(BOROUGH, '')
