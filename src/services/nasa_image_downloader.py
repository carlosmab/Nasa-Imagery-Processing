from time import sleep
import os
import requests
from dataclasses import dataclass
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

@dataclass
class NasaImageParameters:
    lat: float
    lon: float
    date: str | None = None
    dim: float = 0.15
    info: bool = False


class ImageRequestError(Exception):
    def __init__(self, message="Image request failed"):
        self.message = message
        super().__init__(self.message)


class NasaImageDownloader:
    RETRY_DELAY_SECS = 1

    def __init__(self, api_key: str, params: NasaImageParameters, max_retries: int = 3):
        self.api_key = api_key
        self.base_url = os.getenv('NASA_BASE_URL', "")
        self.params = params
        self.max_retries = max_retries

    def get_image(self) -> bytes:
        if not self.params.date:
            self.params.date = datetime.now().strftime(r'%Y-%m-%d')

        payload = {
            'lat': self.params.lat,
            'lon': self.params.lon,
            'date': self.params.date,
            'dim': self.params.dim,
            'api_key': self.api_key,
        }

        retries = 0
        while retries < self.max_retries:
            try:
                response = requests.get(self.base_url, params=payload, stream=True)
                response.raise_for_status()
                binary_data = response.content
                return binary_data
            
            except requests.exceptions.RequestException:
                retries += 1
                sleep(self.RETRY_DELAY_SECS)

        raise ImageRequestError("Failed to retrieve image after retries")
