import random

# Mocked data constants for
BUS_ROUTES = [
    {'route_id': '1A', 'route_name': 'Downtown Express'},
    {'route_id': '2B', 'route_name': 'Uptown Local'},
    {'route_id': '3C', 'route_name': 'Cross-town Shuttle'}
]

BUS_SCHEDULES = {
    'B25': {
        'times': ['09:00 AM', '11:30 AM', '02:00 PM']
    },
    'B38': {
        'times': ['10:00 AM', '12:30 PM', '03:00 PM']
    },
    'B45': {
        'times': ['09:45 AM', '01:15 PM', '04:30 PM']
    }
}

BUS_STATIONS = {
    'B25': {
        'latitude': random.uniform(40.6, 40.8),
        'longitude': random.uniform(-74.1, -73.9)
    },
    'B38': {
        'latitude': random.uniform(40.7, 40.9),
        'longitude': random.uniform(-74.0, -73.8)
    },
    'B45': {
        'latitude': random.uniform(40.65, 40.85),
        'longitude': random.uniform(-74.05, -73.85)
    }
}


def get_bus_routes():
    return BUS_ROUTES


def get_bus_schedule(route_id):
    return BUS_SCHEDULES.get(route_id, {})


def get_bus_stations(route_id):
    return BUS_STATIONS.get(route_id, {})


def main():
    routes = get_bus_routes()
    if routes:
        route_id = routes[0]['route_id']  # Assuming the first route for demonstration
        schedule = get_bus_schedule(route_id)
        stations = get_bus_stations(route_id)
        print("Bus Routes:", routes)
        print("Schedule for Route:", schedule)
        print("Bus Stations:", stations)


if __name__ == '__main__':
    main()
