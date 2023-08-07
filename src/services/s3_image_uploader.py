import os
import boto3
from aiobotocore.session import get_session
from typing import BinaryIO
from dotenv import load_dotenv

load_dotenv()

AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
BUCKET_NAME = os.getenv('BUCKET_NAME', "test-bucket") 
REGION_NAME = os.getenv('REGION_NAME', "us-east-1")

class S3ImageUploader:
    def __init__(self) -> None:
        self.s3 = boto3.client(
            's3', 
            region_name=REGION_NAME,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_access_key_id=AWS_ACCESS_KEY_ID
        )

    def upload_image(self, image_data: BinaryIO, file_path: str) -> None:
        self.s3.upload_fileobj(image_data, BUCKET_NAME, file_path)
        
    async def upload_image_async(self, image_data: BinaryIO, file_path: str) -> None:
        session = get_session()
        async with session.create_client(
                's3',
                region_name=REGION_NAME,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
            ) as client:
        
            return await client.put_object(
                Body=image_data, 
                Bucket=BUCKET_NAME, 
                Key=file_path
            ) # type: ignore
        
            
                
                
            
            
            
            
            
        
            
    