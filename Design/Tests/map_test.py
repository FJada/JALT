
import unittest
from unittest.mock import patch
from ...Design.Functions.Map import render_subway_map

class TestSubwayMapRendering(unittest.TestCase):

    @patch("folium.Map")
    @patch("folium.GeoJson")
    @patch("json.load")
    def test_render_subway_map(self, mock_json_load, mock_geojson, mock_folium_map):
        geojson_file = 'Design/Functions/Subway Lines.geojson'
        # mock test GeoJSON data
        mock_json_load.return_value = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'properties': {'line': 'Test Line'},
                    'geometry': {'type': 'LineString', 'coordinates': [[-73.9415, 40.7002], [-74.0048, 40.7180]]}
                }
            ]
        }

        render_subway_map(geojson_file)
        # assert that the functions were called properly
        mock_folium_map.assert_called_once_with(location=[40.7128, -74.0060], zoom_start=12)
        mock_json_load.assert_called_once_with(open(geojson_file, 'r'))
        mock_geojson.assert_called_once_with(mock_json_load.return_value['features'][0],
                                             name='Test Line', style_function=unittest.mock.ANY)
