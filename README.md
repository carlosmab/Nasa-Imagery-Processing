# NASA Imagery Processing

This project aims to download and process satellite imagery from NASA's Earth Imagery API and upload it to an Amazon S3 bucket. It uses Python and various libraries for asynchronous operations, handling AWS S3, and interacting with the NASA API.

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
   docker run -d --env-file .env nasa-imagery-processing
   ```

   This will run the script daily as specified in the cron job.

## Main functions

### Asynchronous Image Fetching

The get_image_async function is designed to retrieve image data asynchronously from a remote API endpoint. This function takes several arguments, including self (referring to the instance of the class), and is responsible for fetching satellite imagery using parameters like longitude, latitude, and date.

When the function is called, it constructs the payload for the API request, which includes the parameters required for the API query, such as the API key and other relevant details. It then uses a specialized RetryClient to handle the HTTP request asynchronously. This is particularly useful because it automatically manages retries in the face of certain errors or status codes, like server errors (500 series).

Within the context of the HTTP request, the response content (the actual image data) is asynchronously read using await response.read(). If the HTTP response status indicates an error (not 200 OK), an ImageRequestError is raised to handle the situation.

Once the image content is successfully fetched, it is encapsulated within a BytesIO object. This object allows treating the image data as a stream or file-like object, enabling easy handling and further processing. The function then returns this BytesIO object to the caller, effectively providing access to the fetched image data.

In essence, the get_image_async function takes input parameters, constructs an API request, handles asynchronous HTTP communication with retries, and finally returns the retrieved image data in a format that's convenient for further usage or storage.

### Asynchronous S3 uploads

The upload_image_async function is designed to upload binary image data to an Amazon S3 bucket asynchronously. It accepts two main arguments: image_data, which represents the binary image content, and file_path, which specifies the location where the image should be stored within the S3 bucket.

Upon invocation, the function first initializes an asynchronous session using the get_session function, which is responsible for creating an instance of the AWS S3 client. The session is configured with the necessary access credentials and region information.

Inside an asynchronous context (async with), the function establishes a connection to the S3 service using the session's client. This allows for secure and efficient communication with the S3 bucket. Within this context, the put_object operation is awaited, which uploads the image_data to the specified file_path within the designated S3 bucket (BUCKET_NAME).

The function returns None to indicate the completion of the upload process. Additionally, the # type: ignore comment at the end of the function is used to suppress type checking for cases where the type inference might not capture the exact return type.

In summary, the upload_image_async function encapsulates the process of asynchronously uploading image data to an S3 bucket, leveraging the capabilities of asynchronous programming to efficiently handle I/O-bound operations.

### Process field's image

The process_field_async function is a core component of the image processing pipeline, designed to asynchronously download and upload images while handling potential errors along the way. It operates on a given field object, which represents a specific set of parameters and information required to process an image.

The function takes advantage of an asynchronous semaphore to control concurrent execution and ensure a limited number of tasks are running simultaneously. This mechanism helps manage resource utilization and prevent overloading external services, such as API endpoints and storage systems.

Inside the function, the following steps are taken:

- An instance of NasaImageDownloader is created, initialized with the parameters specific to the given field. This downloader is responsible for retrieving image data from the NASA Earth Imagery API.
- The get_image_async method of the downloader is awaited to fetch the image asynchronously. This method handles retries and error handling for API requests.
The downloaded image data is obtained as an asynchronous stream (image_stream).
An instance of S3ImageUploader is created to manage the uploading of the image to an Amazon S3 bucket.
- The upload_image_async method of the uploader is awaited to perform the asynchronous upload of the image to the S3 bucket. This method handles retries and error handling for the S3 upload.
- Upon successful upload, a log message is generated indicating the successful upload of the image.
- If an ImageRequestError occurs during image download, the function logs an error message specific to the download failure and raises the exception for further handling.
If any other exception occurs during image upload or processing, the function logs an error message specific to the upload failure and raises the exception for further handling.

In summary, the process_field_async function orchestrates the asynchronous download and upload of images while incorporating error handling and logging mechanisms. It leverages asyncio features to efficiently manage the asynchronous tasks and semaphore to control concurrent execution. This function plays a crucial role in the image processing pipeline, ensuring that images are acquired and stored accurately and reliably.


### The application function

The upload_fields_images_to_s3_async function serves as the entry point for processing a list of fields and uploading their images to an Amazon S3 bucket. The function is designed to be asynchronous, leveraging the power of asyncio to efficiently handle multiple tasks concurrently.

Here's a breakdown of how the function works:

- The function starts by defining the name of the CSV file (fields_data.csv) that contains the necessary parameters for processing the fields.
- The full path to the CSV file is constructed using the os.path.join function to join the 'data' directory path with the CSV filename.
- The function then calls the parse_params_from_csv function to extract the parameters for each field from the CSV file. This creates a list of field objects.
- A list comprehension is used to create a list of asynchronous tasks (process_field_image_async(field)) for each field in the fields_list. Each task represents the asynchronous processing of an individual field.
- The asyncio.gather function is used to concurrently execute all the tasks created in the previous step. The return_exceptions=True argument ensures that any exceptions raised within the tasks are captured and returned as part of the result, allowing further inspection.
- The function is awaited, causing it to execute asynchronously. It returns a list of results or exceptions corresponding to the completion of each task.

In summary, the upload_fields_images_to_s3_async function coordinates the asynchronous processing of multiple fields by creating tasks for each field's image upload. It takes advantage of asyncio's capabilities to execute tasks concurrently, improving the overall efficiency and speed of the image processing and upload pipeline.



