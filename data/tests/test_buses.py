import pytest
import data.buses as buses

@pytest.fixture(scope='function')
def temp_bus_data():
    buses.BUS_ROUTES = [
        {'route_id': 'B25', 'route_name': 'Downtown Express'},
        {'route_id': 'B38', 'route_name': 'Uptown Local'},
        {'route_id': 'B45', 'route_name': 'Cross-town Shuttle'}
    ]

    buses.BUS_SCHEDULES = {
        'B25': {'times': ['09:00 AM', '11:30 AM', '02:00 PM']},
        'B38': {'times': ['10:00 AM', '12:30 PM', '03:00 PM']},
        'B45': {'times': ['09:45 AM', '01:15 PM', '04:30 PM']}
    }

    buses.BUS_STATIONS = {
        'B25': {'latitude': 40.7128, 'longitude': -74.0060},
        'B38': {'latitude': 40.7580, 'longitude': -73.9855},
        'B45': {'latitude': 40.7267, 'longitude': -74.0031}
    }

def test_get_bus_routes(temp_bus_data):
    routes = buses.get_bus_routes()
    assert len(routes) == 3
    # Add more assertions to validate the structure and content of the data

def test_get_bus_schedule(temp_bus_data):
    schedule = buses.get_bus_schedule('B25')
    assert 'times' in schedule
    # Add assertions to validate schedule format and content

def test_get_bus_stations(temp_bus_data):
    station = buses.get_bus_stations('B38')
    assert 'latitude' in station
    assert 'longitude' in station
    # Add assertions to validate station format and content



