# API Validation Practice

A production-ready FastAPI video processing API with file validation, confidence validation, error handling, structured logging, request IDs, job IDs, and video processing.

## Features

* Video file upload
* Maximum file size validation
* Supported video format validation
* Empty file validation
* YOLO confidence threshold validation
* Unique request IDs
* Unique job IDs
* Video processing
* Job status tracking
* Structured logging
* Global application exception handling
* Proper HTTP status codes
* Clear error messages
* Uploaded videos stored in the `uploads/` directory
* Processed videos stored in the `outputs/` directory

---

## Project Structure

```text
├──Day 28
├──APIVallidation_practice/
│
├── app/
├── routes/
│   └── video.py
├── schemas/
│   └── response.py
├── services/
│   ├── detector.py
│   └── video_processor.py
├── exceptions.py
├── logging_config.py
├── main.py
├── middleware.py
├── logs/
│   └── app.log
├── models/
│   ├── best.pt
│   └── yolov8n.pt
├── README.md
└── requirements.txt
```

---

# requirements.txt

fastapi
uvicorn[standard]
python-multipart
ultralytics
opencv-python
pydantic

# Validations Added

## 1. Required Video File

The API checks whether a video file was provided.

If no file is provided, the API raises a `400 Bad Request` error.

```text
Video file is required.
```

---

## 2. Filename Validation

The API checks whether the uploaded file has a valid filename.

```python
if not file.filename:
    raise AppException(
        "Uploaded file has no filename.",
        400
    )
```

This prevents processing files without filenames.

---

## 3. File Format Validation

Only the following video formats are supported:

```text
.mp4
.avi
.mov
.mkv
```

The allowed extensions are defined as:

```python
ALLOWED_EXTENSIONS = {
    ".mp4",
    ".avi",
    ".mov",
    ".mkv"
}
```

If another format is uploaded, the API returns:

```text
415 Unsupported Media Type
```

Example:

```text
Unsupported file format. Supported formats: mp4, avi, mov, mkv.
```

---

## 4. Maximum File Size Validation

The maximum allowed video size is:

```text
50 MB
```

The API reads the uploaded file in chunks instead of loading the entire video into memory.

```python
MAX_FILE_SIZE = 50 * 1024 * 1024
```

If the file exceeds 50 MB, the upload is stopped and the partially saved file is deleted.

The API returns:

```text
413 Payload Too Large
```

---

## 5. Empty File Validation

After uploading the file, the API checks whether the file size is zero.

```python
if total_size == 0:
    raise AppException(
        "Uploaded video is empty.",
        400
    )
```

This prevents empty files from being sent to the video processor.

---

## 6. Confidence Validation

The YOLO confidence threshold is validated using FastAPI's `Query`.

```python
confidence: float = Query(
    0.25,
    ge=0.0,
    le=1.0,
    description="YOLO confidence threshold"
)
```

The allowed range is:

```text
0.0 <= confidence <= 1.0
```

The default value is:

```text
0.25
```

Values below `0.0` or above `1.0` are rejected.

---

# Errors Handled

The API handles different types of errors.

## Validation Errors

Examples:

* Missing video file
* Missing filename
* Unsupported file extension
* File larger than 50 MB
* Empty video file
* Invalid confidence value

---

## Video Processing Errors

`ValueError` exceptions generated during video processing are handled separately.

They are returned as:

```text
422 Unprocessable Entity
```

The error message is also stored in the job information.

---

## Unexpected Errors

Unexpected exceptions are caught using:

```python
except Exception:
```

These errors are logged using:

```python
logger.exception(...)
```

and the API returns:

```text
500 Internal Server Error
```

The user receives a clear message without exposing internal implementation details.

---

# Logging

The API uses Python's built-in `logging` module.

Important information is logged during the upload and processing workflow.

## Request ID

Every request has a unique `request_id`.

It is used to trace a request through the application.

Example:

```text
request_id=7c1a9f...
```

---

## Job ID

Every video processing request receives a unique `job_id`.

Example:

```text
job_id=91b7d2...
```

The job ID can be used to check processing status.

---

## Uploaded Filename

The original uploaded filename is logged.

Example:

```text
filename=traffic.mp4
```

---

## File Size

The uploaded file size is logged.

Example:

```text
size=24567890
```

---

## Confidence Threshold

The YOLO confidence threshold used for processing is logged.

Example:

```text
confidence=0.25
```

---

## Processing Errors

Processing errors are logged with the request ID and job ID.

Example:

```text
Video processing failed |
request_id=... |
job_id=... |
error=...
```

---

## Unexpected Exceptions

Unexpected errors use `logger.exception()` so that the traceback is also recorded.

Example:

```text
Unexpected video processing error |
request_id=... |
job_id=...
```

This makes debugging easier.

---

# HTTP Status Codes

The API uses appropriate HTTP status codes.

| Status Code | Meaning                | Example                           |
| ----------- | ---------------------- | --------------------------------- |
| `200`       | Success                | Video processed successfully      |
| `400`       | Bad Request            | Empty file or missing filename    |
| `413`       | Payload Too Large      | Video exceeds 50 MB               |
| `415`       | Unsupported Media Type | Unsupported video format          |
| `422`       | Unprocessable Entity   | Video processing/validation error |
| `500`       | Internal Server Error  | Unexpected server error           |

FastAPI may also automatically return `422` for invalid query parameter values such as an invalid confidence value.

---

# API Endpoints

## Process Video

```http
POST /video/process
```

This endpoint accepts a video file and processes it using the YOLO model.

### Request

```text
POST /video/process
Content-Type: multipart/form-data
```

Parameters:

```text
file        Video file
confidence  YOLO confidence threshold
```

Example:

```text
confidence=0.25
```

---

## Job Status

```http
GET /video/jobs/{job_id}
```

This endpoint returns the current status of a video processing job.

Example:

```text
GET /video/jobs/91b7d2...
```

Example response:

```json
{
    "success": true,
    "job_id": "91b7d2...",
    "status": "completed",
    "request_id": "7c1a9f...",
    "error": null
}
```

---

# Failed Request Examples

## Example 1 — Unsupported File Format

### Request

```http
POST /video/process
Content-Type: multipart/form-data

file=document.pdf
```

The API only supports:

```text
.mp4
.avi
.mov
.mkv
```

### Response

```json
{
    "success": false,
    "message": "Unsupported file format. Supported formats: mp4, avi, mov, mkv."
}
```

HTTP status:

```text
415 Unsupported Media Type
```

---

# Example 2 — File Too Large

Suppose the uploaded video is:

```text
75 MB
```

while the maximum allowed size is:

```text
50 MB
```

### Request

```http
POST /video/process
Content-Type: multipart/form-data

file=large_video.mp4
```

### Response

```json
{
    "success": false,
    "message": "File is too large. Maximum allowed size is 50 MB."
}
```

HTTP status:

```text
413 Payload Too Large
```

The partially uploaded file is deleted.

---

# Example 3 — Invalid Confidence

Suppose the user sends:

```text
confidence=1.5
```

The valid range is:

```text
0.0 to 1.0
```

### Request

```http
POST /video/process?confidence=1.5
```

### Response

FastAPI returns a validation error similar to:

```json
{
    "detail": [
        {
            "type": "less_than_equal",
            "loc": [
                "query",
                "confidence"
            ],
            "msg": "Input should be less than or equal to 1",
            "input": "1.5"
        }
    ]
}
```

HTTP status:

```text
422 Unprocessable Entity
```

---

# Successful Response

For a successfully processed video, the API returns:

```json
{
    "success": true,
    "message": "Video processed successfully.",
    "job_id": "91b7d2...",
    "request_id": "7c1a9f...",
    "status": "completed",
    "processing": {
        "..."
    }
}
```

The `job_id` uniquely identifies the video processing job, while the `request_id` identifies the API request.

---

# File Storage

Uploaded videos are saved inside:

```text
APIvalidation_practice/uploads/
```

Processed videos are saved inside:

```text
APIvalidation_practice/outputs/
```

Each video uses a unique UUID-based filename to reduce filename conflicts.

Example:

```text
uploads/
└── 91b7d2c1-xxxx-xxxx-xxxx.mp4

outputs/
└── 91b7d2c1-xxxx-xxxx-xxxx_processed.mp4
```

---

# Error Handling Flow

The general validation and processing flow is:

```text
Client
  |
  v
Upload Video
  |
  v
Validate File
  |
  +---- Invalid Format ------> 415
  |
  +---- File Too Large ------> 413
  |
  +---- Empty File ----------> 400
  |
  v
Create Job ID
  |
  v
Save Video
  |
  v
Process Video with YOLO
  |
  +---- Processing Error ----> 422
  |
  +---- Unexpected Error ---> 500
  |
  v
Completed
  |
  v
Return Job ID + Request ID
```

---

# Logging Example

A successful job may generate logs similar to:

```text
INFO Video job created |
request_id=7c1a9f... |
job_id=91b7d2... |
filename=traffic.mp4 |
size=24567890 |
confidence=0.25
```

If processing fails:

```text
WARNING Video processing failed |
request_id=7c1a9f... |
job_id=91b7d2... |
error=Unable to open video
```

Unexpected errors are logged with their traceback:

```text
ERROR Unexpected video processing error |
request_id=7c1a9f... |
job_id=91b7d2...
```

---

# Conclusion

This project improves the reliability of the FastAPI video processing API by validating uploaded files and confidence values, handling expected and unexpected errors, using meaningful HTTP status codes, and logging important request and processing information.

The use of unique `request_id` and `job_id` values also makes it easier to trace individual requests and video-processing jobs during debugging and production monitoring.

```

This version matches the validation features in the code you provided and is suitable as your **Day 28 `README.md`**.
```
