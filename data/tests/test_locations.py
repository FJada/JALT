# import pytest
# from location import set_current_location, get_current_location, get_nearest_train_stations, get_nearest_bus_stations

# @pytest.fixture(scope='function')
# def temp_location_data():
#     set_current_location({'latitude': 40.889248, 'longitude': -73.898583}, 40.889248, -73.898583)

# def test_set_and_get_current_location(temp_location_data):
#     current_location = get_current_location({'latitude': 40.889248, 'longitude': -73.898583})
#     assert current_location == {'latitude': 40.889248, 'longitude': -73.898583}

# def test_get_nearest_train_stations(temp_location_data):
#     nearest_train_stations = get_nearest_train_stations(max_distance=0.2)
#     assert len(nearest_train_stations) > 0
    

# def test_get_nearest_bus_stations(temp_location_data):
#     nearest_bus_stations = get_nearest_bus_stations(max_distance=0.2)
#     assert len(nearest_bus_stations) > 0
