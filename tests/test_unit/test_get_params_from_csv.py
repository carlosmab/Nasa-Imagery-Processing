from datetime import datetime
import unittest
from unittest.mock import patch
from src.services.nasa_image_downloader import NasaImageParameters
from src.utils.get_params_from_csv import read_csv_and_parse_params

class TestCSVParser(unittest.TestCase):

    @patch('builtins.open')
    @patch('csv.DictReader')
    def test_read_csv_and_parse_params(self, mock_csv_reader, mock_open):
        # Prepare a mock CSV file content
        csv_content = [
            {'field_id': 'field1', 'lon': '10.0', 'lat': '20.0', 'dim': '0.1'},
            {'field_id': 'field2', 'lon': '15.0', 'lat': '25.0', 'dim': '0.2'}
        ]

        # Configure the mock CSV reader
        mock_csv_reader.return_value.__iter__.return_value = csv_content

        # Call the function to parse CSV and get parameters
        parsed_params = read_csv_and_parse_params('test.csv')

        # Assert the expected results
        expected_params = [
            {
                'field_id': 'field1', 
                'params': NasaImageParameters(lat=20.0, lon=10.0, dim=0.1),
                'bucket_folder': f"field1/{datetime.now().strftime(r'%Y-%m-%d')}_imagery.png"
            },
            {
                'field_id': 'field2',
                'params': NasaImageParameters(lat=25.0, lon=15.0, dim=0.2),
                'bucket_folder': f"field2/{datetime.now().strftime(r'%Y-%m-%d')}_imagery.png"
            }
        ]
        self.assertEqual(parsed_params, expected_params)
