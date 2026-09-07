# Day 29 - FastAPI Video Processing API

## Overview

This project is a **FastAPI video-processing API** that accepts video
uploads, creates a processing job in a database, and processes the video
in the background.

The database is used to keep track of each video-processing job and its
current status.

## Project Structure

``` text
Day 29/
│
├── app/
│   ├── core/
│   ├── database/
│   ├── logs/
│   ├── routes/
│   ├── services/
│   ├── database.py
│   ├── exceptions.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── database/
├── FastAPI_Database_practice/
├── logs/
└── models/
```

### Important folders and files

  -----------------------------------------------------------------------
  File / Folder                       Purpose
  ----------------------------------- -----------------------------------
  `app/main.py`                       Starts and configures the FastAPI
                                      application

  `app/routes/`                       Contains API route/endpoint
                                      definitions

  `app/services/`                     Contains video-processing/business
                                      logic

  `app/models.py`                     Contains SQLAlchemy database models

  `app/schemas.py`                    Contains Pydantic request/response
                                      schemas

  `app/database.py`                   Creates the database connection and
                                      SQLAlchemy session

  `app/exceptions.py`                 Handles application-specific
                                      exceptions

  `app/core/`                         Core configuration or application
                                      utilities

  `app/logs/`                         Application logs

  `database/`                         Stores the SQLite database file
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# Database

## What information is stored?

The database stores information about each video-processing job.

A typical `video_jobs` record contains:

-   `id` - Database primary key
-   `job_id` - Unique ID generated for each processing job
-   `filename` - Original uploaded video filename
-   `status` - Current processing status, such as `pending`,
    `processing`, `completed`, or `failed`
-   `total_detections` - Number of detections found during video
    processing

Example record:

``` text
id:               1
job_id:           550e8400-e29b-41d4-a716-446655440000
filename:         crowd.mp4
status:            pending
total_detections: 0
```

The SQLite database used by this project is:

``` text
Day 29/database/video_jobs.db
```

------------------------------------------------------------------------

# Database Structure

The main database table is:

``` text
video_jobs
│
├── id
├── job_id
├── filename
├── status
└── total_detections
```

Conceptually:

``` text
+------------------------------------------------+
|                  video_jobs                    |
+------------------------------------------------+
| id                | Primary Key                |
| job_id            | Unique Job ID              |
| filename          | Uploaded video name       |
| status            | Processing status         |
| total_detections  | Number of detections      |
+------------------------------------------------+
```

The `job_id` is especially useful because it allows the API and client
to identify a processing job without relying on the database's internal
numeric ID.

------------------------------------------------------------------------

# What SQLAlchemy Does

**SQLAlchemy** is the ORM (Object Relational Mapper) used by this
project.

It allows Python code to communicate with the SQL database without
writing every SQL statement manually.

For example, the `VideoJob` model can represent the `video_jobs` table:

``` python
from sqlalchemy import Column, Integer, String
from .database import Base


class VideoJob(Base):
    __tablename__ = "video_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    filename = Column(String, nullable=False)
    status = Column(String, default="pending")
    total_detections = Column(Integer, default=0)
```

Instead of manually writing:

``` sql
INSERT INTO video_jobs (...);
```

SQLAlchemy allows the application to do:

``` python
job = VideoJob(
    job_id=job_id,
    filename=file.filename,
    status="pending",
    total_detections=0
)

db.add(job)
db.commit()
```

SQLAlchemy converts these Python operations into the appropriate SQL
operations.

------------------------------------------------------------------------

# How the API Creates a Processing Job

The main endpoint is:

``` http
POST /video/process
```

The client uploads a video file.

The API performs the following steps:

``` text
Client uploads video
        ↓
FastAPI receives UploadFile
        ↓
Validate filename and extension
        ↓
Generate unique UUID job_id
        ↓
Save video to uploads/
        ↓
Create VideoJob database record
        ↓
Save record with status = "pending"
        ↓
Start background video processing
        ↓
Return job_id to client
```

Supported video formats are:

``` text
.mp4
.avi
.mov
.mkv
```

The uploaded file is saved using the generated job ID, which avoids
filename conflicts.

For example:

``` text
uploads/
└── 550e8400-e29b-41d4-a716-446655440000.mp4
```

The processed output can be stored separately:

``` text
outputs/
└── 550e8400-e29b-41d4-a716-446655440000_processed.mp4
```

------------------------------------------------------------------------

# Example API Request

## Create a Processing Job

### Request

``` http
POST /video/process
Content-Type: multipart/form-data
```

Upload:

``` text
crowd.mp4
```

### Example response

``` json
{
  "message": "Video processing started",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending"
}
```

The important value is the `job_id`.

The client can use this ID to identify the processing job.

------------------------------------------------------------------------

# Processing Status

A processing job normally moves through statuses such as:

``` text
pending
   ↓
processing
   ↓
completed
```

If an error occurs:

``` text
pending
   ↓
processing
   ↓
failed
```

Example database record while processing:

``` json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "crowd.mp4",
  "status": "processing",
  "total_detections": 0
}
```

After processing:

``` json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "crowd.mp4",
  "status": "completed",
  "total_detections": 25
}
```

> The exact status/retrieval endpoint depends on the GET route
> implemented in `app/routes/`. If a job-status endpoint is implemented,
> the client should use the returned `job_id` to retrieve the
> corresponding database record.

------------------------------------------------------------------------

# Retrieving Processing Jobs

Retrieving a job means reading the corresponding record from the
`video_jobs` table.

Using SQLAlchemy, a route can retrieve a job like this:

``` python
job = db.query(VideoJob).filter(
    VideoJob.job_id == job_id
).first()
```

If the job exists, the API can return information such as:

``` json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "crowd.mp4",
  "status": "completed",
  "total_detections": 25
}
```

If the job does not exist, the API should return:

``` json
{
  "detail": "Job not found"
}
```

with:

``` text
HTTP 404 Not Found
```

------------------------------------------------------------------------

# Example API Workflow

### 1. Upload video

``` http
POST /video/process
```

Response:

``` json
{
  "message": "Video processing started",
  "job_id": "abc-123",
  "status": "pending"
}
```

### 2. Video processing starts

The background task processes the video:

``` text
pending → processing
```

### 3. Processing completes

The database is updated:

``` text
processing → completed
```

and the detection count is stored:

``` text
total_detections = 25
```

### 4. Client retrieves the job

The client requests the job information using its `job_id`.

Example response:

``` json
{
  "job_id": "abc-123",
  "filename": "crowd.mp4",
  "status": "completed",
  "total_detections": 25
}
```

------------------------------------------------------------------------

# Why Use a Database?

Without a database, the application would have difficulty remembering
processing jobs after the request finishes.

The database allows the application to:

-   Track uploaded videos
-   Store unique job IDs
-   Track processing status
-   Store detection counts
-   Retrieve previous processing jobs
-   Keep job information available after the API request ends

------------------------------------------------------------------------

# Running the Application

From the `Day 29` directory:

``` bash
uvicorn app.main:app --reload
```

The API is available at:

``` text
http://127.0.0.1:8000
```

FastAPI interactive documentation:

``` text
http://127.0.0.1:8000/docs
```

You can use Swagger UI to upload a video and test the API.

------------------------------------------------------------------------


# Requirements

The main dependencies required for the FastAPI API, file uploads, database connection, and development server are:

```text
fastapi
uvicorn
sqlalchemy
python-multipart
```

## Installing Requirements

Create a virtual environment if needed:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

If the video-processing service uses additional libraries (for example, OpenCV or a machine-learning model), add those packages to `requirements.txt` as required by `app/services/video_processor.py`.

# Summary

This project follows a simple architecture:

``` text
                Client
                  │
                  │ POST /video/process
                  ▼
              FastAPI
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
   Save video          SQLAlchemy
        │                   │
        ▼                   ▼
    uploads/           video_jobs
                            │
                            ▼
                    Store job information
                            │
                            ▼
                    Background processing
                            │
                            ▼
                       outputs/
```

### Key concepts

-   **FastAPI** handles API requests and responses.
-   **UploadFile** receives the uploaded video.
-   **UUID** generates a unique processing job ID.
-   **SQLAlchemy** maps Python models to database tables and manages
    database operations.
-   **SQLite** stores the processing job information.
-   **BackgroundTasks** allows video processing to continue after the
    API creates the job.
-   **Pydantic schemas** can be used to validate and format API data.
-   **`video_jobs.db`** stores the processing-job records.


# Conclusion

Day 29 demonstrates how to build a database-backed video-processing API using FastAPI.

The application receives a video through an API endpoint, validates and saves the uploaded file, creates a unique processing job, and stores the job information in a SQLite database. SQLAlchemy provides the connection between the Python application and the database, while background processing allows the video-processing task to run separately from the initial upload request.

The combination of **FastAPI + SQLAlchemy + SQLite + background processing** provides a simple foundation for building APIs that can accept files, track long-running jobs, and store processing results.

The main workflow is:

```text
Upload Video
     ↓
Validate File
     ↓
Generate Job ID
     ↓
Save Video
     ↓
Create Database Job
     ↓
Background Processing
     ↓
Update Job Status
     ↓
Retrieve Job Information
```

This project also provides practical experience with REST APIs, CRUD-style database operations, SQLAlchemy models, file uploads, UUIDs, background tasks, and API testing through FastAPI Swagger documentation.
