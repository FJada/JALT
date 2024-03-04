import random
import data.db_connect as dbc

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


def get_trains_as_dict() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(TRAIN_NAME, TRAINS_COLLECTION)


def get_train_by_train_name(train_name: str) -> dict:
    dbc.connect_db()
    return dbc.fetch_one(TRAINS_COLLECTION, {TRAIN_NAME: train_name})


def train_exists(train_name: str) -> bool:
    return get_train_by_train_name(train_name) is not None


def favorite_train(train_name: str):
    if not train_exists(train_name):
        raise ValueError(f'Update failure: {train_name} not in database.')
    else:
        dbc.connect_db()
        return dbc.update_doc(TRAINS_COLLECTION, {TRAIN_NAME: train_name},
                              {FAVORITE: 1})


def remove_favorite_train(train_name: str):
    if not train_exists(train_name):
        raise ValueError(f'Update failure: {train_name} not in database.')
    else:
        dbc.connect_db()
        return dbc.update_doc(TRAINS_COLLECTION, {TRAIN_NAME: train_name},
                              {FAVORITE: 0})


def add_train(train_name: str, vehicle_id: str, favorite: bool) -> bool:
    if train_exists(train_name):
        raise ValueError(f'Duplicate train: {train_name=}')
    if not train_name:
        raise ValueError('Train name may not be blank')
    train = {}
    train[TRAIN_NAME] = train_name
    train[VEHICLE_ID] = vehicle_id
    train[FAVORITE] = 0
    dbc.connect_db()
    _id = dbc.insert_one(TRAINS_COLLECTION, train)
    return _id is not None


def del_train(train_name: str, delete_flag: bool):
    if delete_flag:
        if train_exists(train_name):
            return dbc.del_one(TRAINS_COLLECTION, {TRAIN_NAME: train_name})
        else:
            raise ValueError(f'Delete failure: {train_name} not in database.')
    else:
        raise ValueError('Delete skipped')


def get_train_name(train: dict):
    return train.get(TRAIN_NAME, '')


def get_favorite(train: dict) -> bool:
    return bool(train.get(FAVORITE, 0))
