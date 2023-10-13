"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""


def fetch_pets():
    """
    A function to return all pets in the data store.
    """
    return {"tigers": 2, "lions": 3, "zebras": 1}



# if we use the MTA subway gateway API, use this python script to use: API KEY tXtRyYztD6591ExrbXw5v7eVqH5RgVSb7rZHkpLP
# import os

# from underground import metadata, SubwayFeed

# API_KEY = os.getenv('MTA_API_KEY')
# ROUTE = 'Q'
# feed = SubwayFeed.get(ROUTE, api_key=API_KEY)

# # request will read from $MTA_API_KEY if a key is not provided
# feed = SubwayFeed.get(ROUTE)

# # under the hood, the Q route is mapped to a URL. This call is equivalent:
# URL = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw'
# feed = SubwayFeed.get(URL)


# https://data.cityofnewyork.us/resource/p937-wjvj.json
# rodent inspection api 

# https://data.cityofnewyork.us/api/views/inra-wqx3/rows.json?accessType=DOWNLOAD
# floodplain of nyc, shows redzones for storm watch 

