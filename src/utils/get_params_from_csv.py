import csv
from datetime import datetime

from aiohttp_retry import dataclass
from src.services.nasa_image_downloader import NasaImageParameters


@dataclass
class FieldInfo:
    field_id: str
    params: NasaImageParameters
    bucket_path: str

def parse_params_from_csv(csv_file_path: str) -> list[FieldInfo]:
    parsed_params = []

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            field_id = row['field_id']
            lon = float(row['lon'])
            lat = float(row['lat'])
            dim = float(row['dim'])

            params = NasaImageParameters(lat=lat, lon=lon, dim=dim)

            parsed_params.append(FieldInfo(
                field_id=field_id, 
                params=params, 
                bucket_path=f"{field_id}/{datetime.now().strftime(r'%Y-%m-%d')}_imagery.png"
            ))

    return parsed_params