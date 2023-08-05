from moto import mock_s3
import boto3
from typing import BinaryIO

class S3ImageUploader:
    def __init__(self, bucket_name: str, folder_name: str, region_name: str) -> None:
        self.bucket_name = bucket_name
        self.folder_name = folder_name
        self.region_name = region_name
        self.s3 = boto3.client('s3', region_name=self.region_name)

    @mock_s3
    def upload_image(self, image_data: BinaryIO, filename: str) -> None:
        object_key = f'{self.folder_name}/{filename}'
        self.s3.create_bucket(Bucket=self.bucket_name)
        self.s3.upload_fileobj(image_data, self.bucket_name, object_key)