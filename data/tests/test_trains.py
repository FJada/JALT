import pytest
import data.trains as tr

@pytest.fixture(scope='function')
def temp_train():
    train_name = 'Test'
    vehicle_id = tr.gen_vehicle_id()
    favorite = 0
    ret = tr.add_train(train_name, vehicle_id, favorite)
    yield train_name
    if tr.train_exists(train_name):
        tr.del_train(train_name, 1)


def test_get_trains_as_dict():
    trains = tr.get_trains_as_dict()
    assert isinstance(trains, dict)
    for train in trains: 
        assert isinstance(train, str)
        assert isinstance(trains[train], dict)


def test_favorite_train(temp_train):
    tr.favorite_train(temp_train)
    train = tr.get_train_by_train_name(temp_train)
    assert tr.get_favorite(train) is True


def test_remove_favorite(temp_train):
    tr.favorite_train(temp_train)
    tr.remove_favorite_train(temp_train)
    train = tr.get_train_by_train_name(temp_train)
    assert tr.get_favorite(train) is False


def test_gen_vehicle_id():
    vehicle_id = tr.gen_vehicle_id()
    assert vehicle_id is not None


def test_add_blank_train():
    with pytest.raises(ValueError):
        tr.add_train('', 4, 0)


def test_del_train(temp_train):
    train_name = temp_train
    tr.del_train(train_name, 1)
    assert not tr.train_exists(train_name)


def test_del_train_false(temp_train):
    train_name = temp_train
    with pytest.raises(ValueError):
        tr.del_train(train_name, 0)


def test_get_train_by_train_name(temp_train):
    train = tr.get_train_by_train_name(temp_train)
    assert isinstance(train, dict)
