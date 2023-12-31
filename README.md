# NASA Imagery Processing


This project aims to download and process satellite imagery from NASA's Earth Imagery API and upload it to an Amazon S3 bucket. It uses Python and various libraries for asynchronous operations, handling AWS S3, and interacting with the NASA API.

## Autor

Carlos Mario Araújo Berrocal \
carlosm.araujob@gmail.com
## Project Structure

The project has the following folder structure:

```
├── data/
├── src/
|   ├── app/
|   ├── modules/
|   ├── services/
|   └── utils/
└── tests/
```

- `data/`: Contains data files, such as CSV files containing field information.
- `src/`: The main source code of the project.
  - `app/`: The main application logic.
  - `modules/`: Modules and classes for specific tasks.
  - `services/`: Services for interacting with external APIs and services.
  - `utils/`: Utility functions and helper classes.
- `tests/`: Unit tests for the project.

## Setup and Usage

1. Clone the repository:

   ```
   git clone https:github.com/your-username/nasa-imagery-processing.git
   cd nasa-imagery-processing
   ```

2. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the necessary environment variables:

   ```
   NASA_API_KEY=raAuAKYJcwjZ7BOVs1m5mCHISSaIrRQqE6h7DZGw
   NASA_EARTH_IMAGERY_API_URL=https:pi.nasa.gov/planetary/earth/imagery
   BUCKET_NAME=bucket-fields-imagery
   REGION_NAME=us-east-1
   S3_MAX_CONNECTIONS=10
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_ACCESS_KEY_ID=your_access_key
   ```

4. Run the script manually:

   ```
   python src/main.py
   ```

   This will download and process the imagery according to your settings.


## Docker

You can also run the project using Docker:

1. Build the Docker image:

   ```
   docker build -t nasa-imagery-processing .
   ```

2. Run the Docker container:

   ```
   docker run -d nasa-imagery-processing
   ```

   This will run the script daily as specified in the cron job.

## Application description

### Concurrent approach

For the application a Asynchronous programming with asyncio approach was preferred over multithreading and multi-processing. In general this approach is more suitable when dealing with I/O-bound tasks, such as network requests, file I/O, and waiting for external resources, instead of intensive computation. 

Asyncio can execute multiple I/O bound tasks while waiting for the responses in previous executions, at the same time the semaphore option can be used for limiting the number of concurrent uploads and prevent network congestion, especially in scenarios where multiple systems might be trying to access the S3 service concurrently.

### Asynchronous Image Fetching

The get_image_async function fetches satellite imagery data asynchronously from a remote API endpoint. It's a method of a class and is used to retrieve imagery using parameters like longitude, latitude, and date.

The get_image_async function takes input parameters, constructs an API request, handles asynchronous HTTP communication with retries, and finally returns the retrieved image data in a format that's convenient for further usage or storage. 

### Asynchronous S3 uploads

The upload_image_async function is designed to upload binary image data to an Amazon S3 bucket asynchronously. It accepts two main arguments: image_data, which represents the binary image content, and file_path, which specifies the location where the image should be stored within the S3 bucket.

The upload_image_async function encapsulates the process of asynchronously uploading image data to an S3 bucket, leveraging the capabilities of asynchronous programming to efficiently handle I/O-bound operations.

### Process field's image

The process_field_async function is a core component of the image processing pipeline, designed to asynchronously download and upload images while handling potential errors along the way. It operates on a given field object, which represents a specific set of parameters and information required to process an image.

The function takes advantage of an asynchronous semaphore to control concurrent execution and ensure a limited number of tasks are running simultaneously. This mechanism helps manage resource utilization and prevent overloading external services, such as API endpoints and storage systems.


### The application function

The upload_fields_images_to_s3_async function serves as the entry point for processing a list of fields and uploading their images to an Amazon S3 bucket. The function is designed to be asynchronous, leveraging the power of asyncio to efficiently handle multiple tasks concurrently.

The upload_fields_images_to_s3_async function coordinates the asynchronous processing of multiple fields by creating tasks for each field's image upload. It takes advantage of asyncio's capabilities to execute tasks concurrently, improving the overall efficiency and speed of the image processing and upload pipeline.


