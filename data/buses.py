import random
import data.db_connect as dbc

BUSES_COLLECTION = 'buses'
BUS_NAME = 'busName'
STATION_NAME = 'stationName'
BOROUGH = 'borough'


def get_bus_routes():
    return BUS_ROUTES


def add_bus_route():
    bus_route = {}
    bus_route[BUS_NAME] = 'name'
    bus_route[STATION_NAME] = 'station name'
    bus_route[BOROUGH] = 'borough'
    dbc.connect_db()
    _id = dbc.insert_one(BUSES_COLLECTION, bus_route)
    return _id is not None


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
