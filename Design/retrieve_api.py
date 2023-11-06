import os

from underground import metadata, SubwayFeed

API_KEY = os.getenv('MTA_API_KEY')
ROUTE = 'Q'
feed = SubwayFeed.get(ROUTE, api_key=API_KEY)

feed = SubwayFeed.get(ROUTE)

URL = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw'
feed = SubwayFeed.get(URL)

