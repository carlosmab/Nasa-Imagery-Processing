from io import BytesIO
import unittest
from unittest.mock import create_autospec, patch, Mock
from src.services.nasa_image_downloader import ImageRequestError, NasaImageDownloader, NasaImageParameters

class TestNasaImageDownloader(unittest.TestCase):
    
    @patch('requests.get')
    def test_get_image_returns_stream_data(self, mock_get):
        mock_response = Mock()
        mock_response.content = b'Simulated Binary Data'
        mock_get.return_value = mock_response

        params = NasaImageParameters(lat=40.7128, lon=-74.0060)
        nasa_downloader = NasaImageDownloader(params)
        image_stream = nasa_downloader.get_image()
        
        expected_content = b'Simulated Binary Data'
        self.assertIsInstance(image_stream, BytesIO)
        self.assertEqual(image_stream.read(), expected_content)
        
        
    @patch('requests.get')
    def test_get_image_handles_error(self, mock_get):
        mock_get.return_value.raise_for_status.side_effect = ImageRequestError("Error fetching image")
        
        params = NasaImageParameters(lat=40.7128, lon=-74.0060)
        nasa_downloader = NasaImageDownloader(params)

        with self.assertRaises(ImageRequestError):
            nasa_downloader.get_image()


    @patch('requests.get')
    def test_get_image_handles_retries(self, mock_get):
        responses = [
            Mock(status_code=500, content=b'Error response 1'),
            Mock(status_code=503, content=b'Error response 2'),
            Mock(status_code=503, content=b'Error response 3'),
            Mock(status_code=200, content=b'Success response')
        ]
        mock_get.side_effect = responses

        params = NasaImageParameters(lat=40.7128, lon=-74.0060)
        nasa_downloader = NasaImageDownloader(params, max_retries=4)
        binary_image_data = nasa_downloader.get_image()

        self.assertIsNotNone(binary_image_data)
        
    
        

