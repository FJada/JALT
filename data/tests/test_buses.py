import pytest
import data.buses as bu


@pytest.fixture(scope='function')
def temp_bus():
    bus_name = 'Test'
    vehicle_id = bu.gen_vehicle_id()
    favorite = 0
    ret = bu.add_bus(bus_name, vehicle_id, favorite)
    yield bus_name
    if bu.bus_exists(bus_name):
        bu.del_bus(bus_name, 1)


def test_favorite_bus(temp_bus):
    bu.favorite_bus(temp_bus)
    bus = bu.get_bus_by_bus_name(temp_bus)
    assert bu.get_favorite(bus) is True


def test_remove_favorite(temp_bus):
    bu.favorite_bus(temp_bus)
    bu.remove_favorite_bus(temp_bus)
    bus = bu.get_bus_by_bus_name(temp_bus)
    assert bu.get_favorite(bus) is False


def test_vehicle_id():
    vehicle_id = bu.gen_vehicle_id()
    assert vehicle_id is not None


def test_add_blank_bus():
    with pytest.raises(ValueError):
        bu.add_bus('', 4, 0)


def test_del_bus(temp_bus):
    bus_name = temp_bus
    bu.del_bus(bus_name, 1)
    assert not bu.bus_exists(bus_name)


def test_del_bus_false(temp_bus):
    bus_name = temp_bus
    with pytest.raises(ValueError):
        bu.del_bus(bus_name, 0)
