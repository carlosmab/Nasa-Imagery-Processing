import unittest
from unittest.mock import patch, Mock
from src.services.nasa_image_downloader import ImageRequestError, NasaImageDownloader, NasaImageParameters

class TestNasaImageDownloader(unittest.TestCase):
    
    @patch('requests.get')
    def test_get_image_returns_binary_data(self, mock_get):
        mock_response = Mock()
        mock_response.content = b'Simulated Binary Data'
        mock_get.return_value = mock_response

        api_key = 'your-api-key'
        params = NasaImageParameters(lat=40.7128, lon=-74.0060)
        nasa_downloader = NasaImageDownloader(api_key, params)
        binary_image_data = nasa_downloader.get_image()

        # Ensure that the returned binary data matches the mock response content
        self.assertEqual(binary_image_data, b'Simulated Binary Data')
        
    @patch('requests.get')
    def test_get_image_handles_error(self, mock_get):
        mock_get.return_value.raise_for_status.side_effect = ImageRequestError("Error fetching image")

        api_key = 'your-api-key'
        params = NasaImageParameters(lat=40.7128, lon=-74.0060)
        nasa_downloader = NasaImageDownloader(api_key, params)

        with self.assertRaises(ImageRequestError):
            nasa_downloader.get_image()


    @patch('requests.get')
    def test_get_image_handles_retries(self, mock_get):
        responses = [Mock(status_code=500), Mock(status_code=503), Mock(status_code=200)]
        mock_get.side_effect = responses

        api_key = 'your-api-key'
        params = NasaImageParameters(lat=40.7128, lon=-74.0060)
        nasa_downloader = NasaImageDownloader(api_key, params)
        binary_image_data = nasa_downloader.get_image()

        self.assertIsNotNone(binary_image_data)
        

