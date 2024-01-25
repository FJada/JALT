# pip install nyct-gtfs
from nyct_gtfs.static import Static
"""
    Get all subway lines at a given station using GTFS data.
    Params:
    - station_name: The name of the station.
    - gtfs_path: The path to the GTFS data directory.

    Returns:
    - list of subway lines at the given station.
"""
def get_Train_at_Station(station_name, gtfs_path):
    static_data = Static(gtfs_path)
    routes_at_station = set()
    for stop in static_data.stops.values():
        if stop.stop_name == station_name:
            for route in static_data.routes.values():
                if stop.stop_id in route.stop_ids:
                    routes_at_station.add(route.route_id)
    return list(routes_at_station)