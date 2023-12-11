# """
# endpoint that uses psudeo data to simulate a user's current location using longitude and latitude
# and its setters and getter functions
# """

# from trains import get_train_locations,TRAIN_STOPS, TRAIN_LOCATIONS
# from buses import get_bus_stations,BUS_STOPS, BUS_STATIONS
# import math

# CURRENT_LOCATION =[
# {'location_id': {'latitude': 40.889248, 'longitude': -73.898583}}
# ]

# def get_current_location(location_id):
#     return CURRENT_LOCATION.get(location_id, {})

# def set_current_location(location_id, latitude, longitude):
#     for location in CURRENT_LOCATION:
#         if location['location_id'] == location_id:
#             location['location_id']['latitude'] = latitude
#             location['location_id']['longitude'] = longitude
#             return
#     # current location doesn't exist add a new one
#     new_location = {'location_id': {'latitude': latitude, 'longitude': longitude}}
#     CURRENT_LOCATION.append(new_location)



# def haversine(latitude_1, longitude_1, latitude_2, longitude_2):
#     """
#     function is a formula used to calculate the circle 
#     distance between two points on the surface of a sphere. 
#     """
#     # earth's radius in kilometers
#     R = 6371  
    
#     dlatitude = math.radians(latitude_2 - latitude_1)
#     dlongitude = math.radians(longitude_2 - longitude_1)

#     a = math.sin(dlatitude / 2) ** 2 + math.cos(math.radians(latitude_1)) * math.cos(math.radians(latitude_2)) * math.sin(dlongitude / 2) ** 2
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#     # distance in kilometers
#     distance = R * c  
#     return distance

# def get_nearest_train_stations(max_distance=0.2):
#     """
#     function that gets the nearest train stations to the current location and appends them to a list 
#     of other train stations nearby 
#     """
#     min_distance = float('inf')
#     nearest_stations = []
    
#     for stop in TRAIN_STOPS:
#         stop_name = stop['stop_name']
#         stop_location = TRAIN_LOCATIONS.get(stop_name, {})
#         if stop_location:
#             stop_lat = stop_location['latitude']
#             stop_lon = stop_location['longitude']
            
#             current_lat = CURRENT_LOCATION.get('latitude')
#             current_lon = CURRENT_LOCATION.get('longitude')
            
#             distance = haversine(current_lat, current_lon, stop_lat, stop_lon)

#             if distance < max_distance and distance <= min_distance:
#                 if distance < min_distance:
#                     nearest_stations = [stop_name]
#                     min_distance = distance
#                 else:
#                     nearest_stations.append(stop_name)
#     return nearest_stations

# def get_nearest_bus_stations(max_distance=0.2):
#     """
#     function that gets the nearest bus stations to the current location and appends them to a list 
#     of other bus stations nearby 
#     """
#     min_distance = float('inf')
#     nearest_stations = []
    
#     for stop in BUS_STOPS:
#         stop_name = stop['stop_name']
#         stop_location = BUS_STATIONS.get(stop_name, {})
#         if stop_location:
#             stop_lat = stop_location['latitude']
#             stop_lon = stop_location['longitude']
#             current_lat = CURRENT_LOCATION.get('latitude')
#             current_lon = CURRENT_LOCATION.get('longitude')
#             distance = haversine(current_lat, current_lon, stop_lat, stop_lon)

#             if distance < max_distance and distance <= min_distance:
#                 if distance < min_distance:
#                     nearest_stations = [stop_name]
#                     min_distance = distance
#                 else:
#                     nearest_stations.append(stop_name)
#     return nearest_stations

    
# def main():
#     set_current_location({'latitude': 40.889248, 'longitude': -73.898583}, 42.123, -71.456)
#     print(get_current_location({'latitude': 40.889248, 'longitude': -73.898583}))
    
# if __name__ == '__main__':
#     main()