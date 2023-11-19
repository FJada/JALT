import unittest
from unittest.mock import patch, MagicMock

def process_data(data):
    # Replace this with your actual data processing logic
    for entity in data.get('entity', []):
        if 'vehicle' in entity:
            vehicle_id = entity['id']
            vehicle_position = entity['vehicle']['position']
            print(f"Vehicle ID: {vehicle_id}, Position: {vehicle_position}")
