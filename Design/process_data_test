def test_process_data(self, mock_print):
        # Mock data to simulate the expected structure of api 
        mock_data = {'entity': [{'id': 'bus123', 'vehicle': {'position': {'latitude': 40.7128, 'longitude': -74.0060}}}]}
        
        # Call testee function with the mock data
        process_data(mock_data)

        # Verify that the expected print statement was called
        mock_print.assert_called_once_with("Vehicle ID: bus123, Position: {'latitude': 40.7128, 'longitude': -74.0060}")
