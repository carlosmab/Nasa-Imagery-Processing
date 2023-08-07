from io import BytesIO
from time import sleep
import os
import requests
import aiohttp
from aiohttp_retry import RetryClient, ExponentialRetry
from dataclasses import asdict, dataclass
from datetime import datetime

@dataclass
class NasaImageParameters:
    lat: float = 0.0
    lon: float = 0.0
    date: str = datetime.now().strftime(r'%Y-%m-%d')
    dim: float = 0.15


class ImageRequestError(Exception):
    def __init__(self, message="Image request failed"):
        self.message = message
        super().__init__(self.message)


class NasaImageDownloader:
    RETRY_DELAY_SECS = 1

    def __init__(self, params: NasaImageParameters, api_key: str = "DEMO_KEY", max_retries: int = 3):
        self.api_key = api_key
        self.base_url = os.environ.get('NASA_EARTH_IMAGERY_API_URL', "")
        self.params = params
        self.max_retries = max_retries

    def get_image(self) -> BytesIO:
        if not self.params.date:
            self.params.date = datetime.now().strftime(r'%Y-%m-%d')

        payload = asdict(self.params)
        payload["api_key"] = self.api_key
            
        retries = 0
        while retries < self.max_retries:
            try:
                response = requests.get(self.base_url, params=payload, stream=True)
                response.raise_for_status()
                image_stream = BytesIO(response.content)
                return image_stream
            
            except requests.exceptions.RequestException:
                retries += 1
                sleep(self.RETRY_DELAY_SECS)

        raise ImageRequestError("Failed to retrieve image after retries")
    
    
    async def get_image_async(self) -> BytesIO:
        
        retry_options = ExponentialRetry(
            attempts=self.max_retries,
            statuses={500, 502, 503, 504},
            exceptions={aiohttp.ClientError, },
        )
        
        payload = asdict(self.params)
        payload["api_key"] = self.api_key

        async with RetryClient(retry_options=retry_options) as session:
            async with session.get(self.base_url, params=payload) as response:
                if response.status != 200:
                    raise ImageRequestError(f"Error fetching image: HTTP {response.status}")
                
                content = await response.read()
                return BytesIO(content)
