import asyncio
from src.app.app import upload_fields_images_to_s3_async


if __name__ == "__main__":
    results = asyncio.run(upload_fields_images_to_s3_async())
    for result in results:
        if isinstance(result, Exception):
            # Handle the exception here
            print(f"An error occurred: {result}")
        else:
            print(result) 