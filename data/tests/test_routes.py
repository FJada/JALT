import pytest

import data.routes as ro

@pytest.fixture(scope='function')
def temp_route():
    route_id = ro.gen_route_id()
    starting_point = 'new york'
    ending_point = 'massachusetts'
    ret = ro.add_route(starting_point, ending_point, route_id)
    yield route_id
    if ro.route_exists(route_id):
        ro.del_route(route_id)


def test_get_route_by_route_id(temp_route):
    route = ro.get_route_by_route_id(temp_route)
    assert isinstance(route, dict)


def test_update_ending_point(temp_route):
    new_ending_point = 'Connecticut'
    ro.update_ending_point(temp_route, new_ending_point)
    updated_route = ro.get_route_by_route_id(temp_route)
    assert ro.get_ending_point(updated_route) == new_ending_point


def test_update_starting_point(temp_route):
    new_starting_point = 'Connecticut'
    ro.update_starting_point(temp_route, new_starting_point)
    updated_route = ro.get_route_by_route_id(temp_route)
    assert ro.get_starting_point(updated_route) == new_starting_point


def test_del_route(temp_route):
    route_id = temp_route
    ro.del_route(route_id)
    assert not ro.route_exists(route_id)


def test_add_dup_route(temp_route):
    route_id = ro.gen_route_id
    with pytest.raises(ValueError):
        ro.add_route('new york', 'boston', route_id)
