import logging

log_filename = 'output.log'
logging.basicConfig(
    filename=log_filename, 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

import asyncio
import os
from src.services.s3_image_uploader import S3ImageUploader
from src.services.nasa_image_downloader import ImageRequestError, NasaImageDownloader


S3_MAX_CONNECTIONS = os.environ.get('S3_MAX_CONNECTIONS', 5)

semaphore = asyncio.Semaphore(int(S3_MAX_CONNECTIONS))

async def process_field_image_async(field):
    async with semaphore:
        try:
            nasa_downloader = NasaImageDownloader(field.params)
            image_stream = await nasa_downloader.get_image_async()
            s3_uploader = S3ImageUploader()
            await s3_uploader.upload_image_async(image_stream, field.bucket_path)
            return f'Uploaded: {field.bucket_path}'
        
        except ImageRequestError as e:
            logging.error(f'Error downloading image for {field.bucket_path}: {str(e)}')
            raise e
        
        except Exception as e:
            logging.error(f'Error uploading image for {field.bucket_path}: {str(e)}')
            raise e
