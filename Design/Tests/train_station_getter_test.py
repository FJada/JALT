import unittest
from unittest.mock import patch
from ...Design.Functions.get_Trains_at_Station import get_Train_at_Station

class TestGetTrainAtStation(unittest.TestCase):

    @patch('nyct_gtfs.static.Static')
    def test_get_subway_lines_at_station(self, mock_static):
        # mock data
        mock_static_instance = mock_static.return_value
        mock_static_instance.stops = {
            'stop1': {'stop_id': 'stop1', 'stop_name': 'Station_A', 'stop_lat': 40.123, 'stop_lon': -73.456},
            'stop2': {'stop_id': 'stop2', 'stop_name': 'Station_B', 'stop_lat': 40.789, 'stop_lon': -74.012},
            # Add more stops as needed
        }
        mock_static_instance.routes = {
            'route1': {'route_id': 'route1', 'route_short_name': 'A', 'stop_ids': ['stop1']},
            'route2': {'route_id': 'route2', 'route_short_name': 'B', 'stop_ids': ['stop2']},
        }

        result = get_Train_at_Station('Station_A', '/path/to/your/gtfs/data')
        self.assertEqual(result, ['A'])

if __name__ == '__main__':
    unittest.main()
