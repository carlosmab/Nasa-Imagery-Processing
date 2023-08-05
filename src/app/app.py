import asyncio
import os
from services.nasa_image_downloader import NasaImageDownloader
from services.s3_image_uploader import S3ImageUploader
from src.services.nasa_image_downloader import ImageRequestError
from src.utils.get_params_from_csv import parse_params_from_csv
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

BUCKET_NAME = os.getenv('BUCKET_NAME', "test-bucket") 
REGION_NAME = os.getenv('REGION_NAME', "us-east-1")


async def process_field(field):
    nasa_downloader = NasaImageDownloader(field.params)
    try:
        image_stream = await nasa_downloader.get_image_async()
        s3_uploader = S3ImageUploader(BUCKET_NAME, REGION_NAME)
        await s3_uploader.upload_image_async(image_stream, field.bucket_path)
        return f'Uploaded: {field.bucket_path}'
    
    except ImageRequestError as e:
        logging.error(f'Error downloading image for {field.bucket_path}: {str(e)}')
        raise e
    
    except Exception as e:
        logging.error(f'Error uploading image for {field.bucket_path}: {str(e)}')
        raise e

    
async def upload_fields_images_to_s3_handler():
    csv_filename = 'fields.csv'
    csv_path = os.path.join('data', csv_filename)
    fields_list = parse_params_from_csv(csv_path)

    tasks = [process_field(field) for field in fields_list]
    return await asyncio.gather(*tasks, return_exceptions=True)

