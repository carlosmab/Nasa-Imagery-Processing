import unittest
from moto import mock_s3
import boto3
from src.services.s3_image_uploader import S3ImageUploader

class TestS3ImageUploader(unittest.TestCase):
    BUCKET_NAME = 'test-bucket'
    FOLDER_NAME = 'test-folder'

    def setUp(self):
        self.s3 = boto3.client('s3')
        self.s3.create_bucket(Bucket=self.BUCKET_NAME)
        self.s3_uploader = S3ImageUploader(self.BUCKET_NAME, self.FOLDER_NAME)
        
    @mock_s3
    def test_upload_image_to_s3(self):
        
        binary_image_data = b'Simulated Binary Data'
        self.s3_uploader.upload_image(binary_image_data, 'image.png')

        s3_objects = self.s3.list_objects_v2(Bucket=self.BUCKET_NAME)['Contents']
        uploaded_object_keys = [obj['Key'] for obj in s3_objects]
        expected_key = f'{self.FOLDER_NAME}/image.png'
        self.assertIn(expected_key, uploaded_object_keys)


if __name__ == '__main__':
    unittest.main()
