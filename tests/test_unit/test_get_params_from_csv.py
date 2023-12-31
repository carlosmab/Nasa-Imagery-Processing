from datetime import datetime
import unittest
from unittest.mock import patch
from src.services.nasa_image_downloader import NasaImageParameters
from src.utils.get_params_from_csv import FieldInfo, parse_params_from_csv


class TestCSVParser(unittest.TestCase):

    @patch('builtins.open')
    @patch('csv.DictReader')
    def test_read_csv_and_parse_params(self, mock_csv_reader, mock_open):
        csv_content = [
            {'field_id': 'field1', 'lon': '10.0', 'lat': '20.0', 'dim': '0.1'},
            {'field_id': 'field2', 'lon': '15.0', 'lat': '25.0', 'dim': '0.2'},
        ]

        mock_csv_reader.return_value.__iter__.return_value = csv_content
        parsed_params = parse_params_from_csv('test.csv')

        expected_params = [
            FieldInfo(
                field_id='field1',
                params=NasaImageParameters(lat=20.0, lon=10.0, dim=0.1),
                bucket_path=f"field1/{datetime.now().strftime(r'%Y-%m-%d')}_imagery.png"
            ),
            FieldInfo(
                field_id='field2',
                params=NasaImageParameters(lat=25.0, lon=15.0, dim=0.2),
                bucket_path=f"field2/{datetime.now().strftime(r'%Y-%m-%d')}_imagery.png"
            )
        ]
        
        self.assertEqual(parsed_params, expected_params)
