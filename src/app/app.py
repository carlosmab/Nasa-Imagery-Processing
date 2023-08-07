import asyncio
import os
from src.modules.fields_image_processor import process_field_image_async
from src.utils.get_params_from_csv import parse_params_from_csv


async def upload_fields_images_to_s3_async():
    csv_filename = 'fields_data.csv'
    csv_path = os.path.join('data', csv_filename)
    fields_list = parse_params_from_csv(csv_path)

    tasks = [process_field_image_async(field) for field in fields_list]
    return await asyncio.gather(*tasks, return_exceptions=True)
