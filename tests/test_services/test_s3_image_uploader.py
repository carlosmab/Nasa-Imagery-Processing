from io import BytesIO
import unittest
from moto import mock_s3
import boto3
from src.services.s3_image_uploader import S3ImageUploader

class TestS3ImageUploader(unittest.TestCase):
    BUCKET_NAME: str = 'test-bucket'
    FOLDER_NAME: str = 'test-folder'
    REGION_NAME: str = 'us-east-1'
    
    @mock_s3
    def setUp(self) -> None:
        self.s3 = boto3.client('s3', region_name=self.REGION_NAME)
        self.s3.create_bucket(Bucket=self.BUCKET_NAME)
        self.s3_uploader = S3ImageUploader(self.BUCKET_NAME, self.FOLDER_NAME, self.REGION_NAME)
        
    @mock_s3
    def test_upload_image_to_s3(self) -> None:
        
        binary_image_data = b'Simulated Binary Data'
        image_stream = BytesIO(binary_image_data)
        
        self.s3_uploader.upload_image(image_stream, 'image.png')

        s3_objects = self.s3.list_objects_v2(Bucket=self.BUCKET_NAME)['Contents']
        uploaded_object_keys = [obj['Key'] for obj in s3_objects]
        expected_key = f'{self.FOLDER_NAME}/image.png'
        self.assertIn(expected_key, uploaded_object_keys)


