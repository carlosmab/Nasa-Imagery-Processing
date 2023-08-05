import csv
from src.services.nasa_image_downloader import NasaImageParameters

def parse_params_from_csv(csv_file_path: str) -> list[dict]:
    parsed_params = []

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            field_id = row['field_id']
            lon = float(row['lon'])
            lat = float(row['lat'])
            dim = float(row['dim'])

            params = NasaImageParameters(lat=lat, lon=lon, dim=dim)

            parsed_params.append({
                'field_id': field_id,
                'params': params,
                'bucket_folder': f"{field_id}/{params.date}_imagery.png"
            })

    return parsed_params