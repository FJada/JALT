import pytest
import data.buses as bu
import data.db_connect as dbc

@pytest.fixture(scope='function')
def temp_bus():
    bus_name = 'Test'
    borough = 'None'
    favorite = 0
    ret = bu.add_bus(bus_name, borough, favorite)
    yield bus_name
    if bu.bus_exists(bus_name):
        bu.del_bus(bus_name, 1)


def test_get_buses_as_dict():
    buses = bu.get_buses_as_dict()
    assert isinstance(buses, dict)
    for bus in buses: 
        assert isinstance(bus, str)
        assert isinstance(buses[bus], dict)


def test_favorite_bus(temp_bus):
    bu.favorite_bus(temp_bus)
    bus = bu.get_bus_by_bus_name(temp_bus)
    assert bu.get_favorite(bus) is True


def test_remove_favorite(temp_bus):
    bu.favorite_bus(temp_bus)
    bu.remove_favorite_bus(temp_bus)
    bus = bu.get_bus_by_bus_name(temp_bus)
    assert bu.get_favorite(bus) is False


def test_gen_vehicle_id():
    vehicle_id = bu.gen_vehicle_id()
    assert vehicle_id is not None


def test_add_blank_bus():
    with pytest.raises(ValueError):
        bu.add_bus('', '', 0)


def test_del_bus(temp_bus):
    bus_name = temp_bus
    bu.del_bus(bus_name, 1)
    assert not bu.bus_exists(bus_name)


def test_del_bus_false(temp_bus):
    bus_name = temp_bus
    with pytest.raises(ValueError):
        bu.del_bus(bus_name, 0)


def test_get_bus_by_bus_name(temp_bus):
    bus = bu.get_bus_by_bus_name(temp_bus)
    assert isinstance(bus, dict)
