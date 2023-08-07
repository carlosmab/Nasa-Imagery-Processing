from io import BytesIO
import unittest
from asynctest import TestCase
from asynctest.mock import patch

from src.services.s3_image_uploader import S3ImageUploader

class TestS3ImageUploaderAsync(TestCase):
    @patch('aiobotocore.client.AioBaseClient._make_api_call')
    async def test_upload_image_to_s3_async(self, mock_make_api_call):
        bucket_name = 'bucket-fields-imagery'
        
        image_stream = BytesIO(b'Simulated Binary Data')
        expected_call = {
            "Bucket": bucket_name,
            "Key": "dir/image.png",
            "Body": image_stream,
        }
        
        s3_uploader = S3ImageUploader()
        await s3_uploader.upload_image_async(image_stream, "dir/image.png")
        
        mock_make_api_call.assert_called_with('PutObject', expected_call)
        

if __name__ == '__main__':
    unittest.main()