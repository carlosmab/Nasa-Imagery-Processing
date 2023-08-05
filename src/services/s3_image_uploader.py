from moto import mock_s3
import boto3
from aiobotocore.session import get_session
from typing import BinaryIO

class S3ImageUploader:
    def __init__(self, bucket_name: str, region_name: str) -> None:
        self.bucket_name = bucket_name
        self.region_name = region_name
        self.s3 = boto3.client('s3', region_name=self.region_name)

    def upload_image(self, image_data: BinaryIO, file_path: str) -> None:
        self.s3.upload_fileobj(image_data, self.bucket_name, file_path)
        
    async def upload_image_async(self, image_data: BinaryIO, file_path: str) -> None:
        async_session = get_session()
        async with async_session.create_client('s3') as s3:
            s3.upload_fileobj(image_data, self.bucket_name, file_path)
    