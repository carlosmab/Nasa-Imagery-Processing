from unittest.mock import AsyncMock, patch
from unittest import TestCase
from io import BytesIO
from src.services.nasa_image_downloader import ImageRequestError, NasaImageDownloader, NasaImageParameters

class TestAsyncNasaImageDownloader(TestCase):
    @patch('aiohttp_retry.RetryClient.get')
    async def test_async_get_image_returns_stream_data(self, mock_retry_get: AsyncMock):

        async def mock_response(*args, **kwargs):
            response =  AsyncMock()
            response.status = 200
            response.read.return_value = b'Simulated Image Data'
            return response

        mock_retry_get.side_effect = mock_response
        
        params = NasaImageParameters(lat=40.7128, lon=-74.0060)
        nasa_downloader = NasaImageDownloader(params)
        
        image_stream = await nasa_downloader.get_image_async()

        self.assertIsInstance(image_stream, BytesIO)
        self.assertEqual(image_stream.read(), b'Simulated Image Data')
        image_stream.close() 
        
        
    @patch('aiohttp_retry.RetryClient.get')
    async def test_async_get_image_retries_on_failure(self, mock_retry_get):
        async def mock_response(*args, **kwargs):
            response = AsyncMock()
            response.status = 503 if mock_response.call_count < 4 else 200
            if response.status == 503:
                raise ImageRequestError("Error fetching image")
            content = b'Simulated Image Data'
            response.read.return_value = content
            return response

        mock_retry_get.return_value.get.side_effect = mock_response

        params = NasaImageParameters(lat=40.7128, lon=-74.0060)
        nasa_downloader = NasaImageDownloader(params, max_retries=4)

        image_stream = await nasa_downloader.get_image_async()

        self.assertIsInstance(image_stream, BytesIO)
        self.assertEqual(image_stream.read(), b'Simulated Image Data')
        image_stream.close()

        self.assertEqual(mock_retry_get.call_count, 4)
        
    @patch('aiohttp_retry.RetryClient.get')
    async def test_async_get_image_retries_exhausted(self, mock_retry_get):
        async def mock_response(*args, **kwargs):
            response = AsyncMock()
            response.status = 503
            raise ImageRequestError("Error fetching image")

        mock_retry_get.side_effect = mock_response

        params = NasaImageParameters(lat=40.7128, lon=-74.0060)
        nasa_downloader = NasaImageDownloader(params)

        with self.assertRaises(ImageRequestError):
            await nasa_downloader.get_image_async()
            
        self.assertEqual(mock_retry_get.return_value.get.call_count, 3)