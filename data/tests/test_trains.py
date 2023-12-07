import pytest
import data.trains as trains

@pytest.fixture(scope='function')
def temp_stop_data():
    trains.TRAIN_STOPS = [
       {'stop_id': '101', 'stop_name': 'Van Cortlandt Park - 242 St', 'stop_line':'Broadway-Seventh Avenue Local'},
       {'stop_id': 'A49', 'stop_name': 'Nostrand Av' ,'stop_line': 'Eighth Avenue Express'},
       {'stop_id': 'F01', 'stop_name': 'Jamaica - 179 St' ,'stop_line': 'Queens Boulevard Express/Sixth Avenue Local'}
    ]

    trains.TRAIN_SCHEDULES = {
       '1': {'times': ['09:00 AM', '11:30 AM', '02:00 PM']},
       'A': {'times': ['10:00 AM', '12:30 PM', '03:00 PM']},
       'F': {'times': ['09:45 AM', '01:15 PM', '04:30 PM']}
    }

    trains.TRAIN_LOCATIONS = {
        'Van Cortlandt Park - 242 St': {
        'latitude': 40.889248,
        'longitude': -73.898583
    },
    'Nostrand Av': {
        'latitude': 40.680438,
        'longitude': -73.950426
    },
    'Jamaica - 179 St': {
        'latitude': 40.712646,
        'longitude': -73.783817
    }
    }

def test_get_train_stops(temp_stop_data):
    stops = trains.get_train_stops()
    assert len(stops) == 3
    # Add more assertions to validate the structure and content of the data

def test_get_train_schedule(temp_stop_data):
    schedule = trains.get_train_schedule('101')
    assert 'times' in schedule
    # Add assertions to validate schedule format and content

def test_get_train_locations(temp_stop_data):
    location = trains.get_train_locations('A49')
    assert 'latitude' in location
    assert 'longitude' in location
    # Add assertions to validate location format and content
