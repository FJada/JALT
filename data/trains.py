import random
import data.db_connect as dbc

# Mocked data constants for 
TRAIN_STOPS = [
    {'stop_id': '101', 'stop_name': 'Van Cortlandt Park - 242 St', 'stop_line':'Broadway-Seventh Avenue Local'},
    {'stop_id': 'A49', 'stop_name': 'Nostrand Av' ,'stop_line': 'Eighth Avenue Express'},
    {'stop_id': 'F01', 'stop_name': 'Jamaica - 179 St' ,'stop_line': 'Queens Boulevard Express/Sixth Avenue Local'}
]

TRAIN_SCHEDULES = {
    '1': {
        'times': ['09:00 AM', '11:30 AM', '02:00 PM']
    },
    'A': {
        'times': ['10:00 AM', '12:30 PM', '03:00 PM']
    },
    'F': {
        'times': ['09:45 AM', '01:15 PM', '04:30 PM']
    }
}

TRAIN_STATIONS = {
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

def get_train_stops():
    return TRAIN_STOPS

def get_train_schedule(stop_id):
    return TRAIN_SCHEDULES.get(stop_id, {})

def get_train_locations(stop_id):
    return TRAIN_LOCATIONS.get(stop_id, {})

def main():
    stops = get_train_stops()
    if stops:
        stop_id = stops[0]['stop_id']  # Assuming the first route for demonstration
        schedule = get_train_schedule(stop_id)
        locations = get_train_locations(stop_id)
        print("Train Stops:", stops)
        print("Schedule for Stop:", schedule)
        print("Stop Location:", locations)

if __name__ == '__main__':
    main()