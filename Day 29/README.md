AI Video Processing History API

A FastAPI backend that accepts video uploads, runs YOLOv8 object detection on them in the background, and stores/retrieves the processing history in a SQLite database via SQLAlchemy.

Table of Contents
Overview
Project Structure
What Information Is Stored in the Database
Database Structure
What SQLAlchemy Does Here
How the API Creates & Retrieves Jobs
API Endpoints
Example API Requests & Responses
Logging
Setup & Installation
Requirements
Conclusion
Overview

This project lets a client upload a video file, which is then processed asynchronously using a YOLOv8n object-detection model (via ultralytics + opencv-python). Every upload is tracked as a job with a unique ID, a status (pending → processing → completed/failed), and metadata about the run (processing time, detection count, output file). Clients can poll job status, list job history, or delete old jobs.

Project Structure
app/
├── core/
│   └── logging_config.py     # Central logging setup (console + file)
├── database/
│   └── video_jobs.db         # SQLite database file (auto-created)
├── logs/
│   └── app.log                # Application log file
├── routes/
│   ├── video.py               # POST /video/process — upload & kick off processing
│   └── jobs.py                 # GET/DELETE /jobs — job history endpoints
├── services/
│   └── video_processor.py     # YOLOv8 inference + video annotation logic
├── database.py                 # SQLAlchemy engine/session/Base setup
├── exceptions.py                # Custom AppException class
├── main.py                      # FastAPI app entrypoint, router registration
├── models.py                    # SQLAlchemy ORM models (VideoJob)
└── schemas.py                    # Pydantic response schemas (JobResponse)
requirements.txt
README.md
What Information Is Stored in the Database

Each row in the database represents one video processing job, capturing everything needed to track and audit that job over its lifecycle:

Data stored	Why it's stored
A unique job identifier	So a client can reference/poll a specific job
The original filename	For display and traceability back to the uploaded file
Current status	Tracks lifecycle: pending, processing, completed, failed
Creation timestamp	When the job was submitted
Completion timestamp	When processing finished (if it did)
Total processing time	Performance/monitoring metric
Total object detections	Result summary from the YOLO model
Output file path	Where the annotated/processed video was saved

No raw video bytes are stored in the database itself — only metadata about the job. The actual video files live on disk under videos/input/ and videos/output/.

Database Structure

Engine: SQLite, stored at app/database/video_jobs.db ORM: SQLAlchemy (declarative model)

Table: video_jobs
Column	Type	Constraints	Description
id	Integer	Primary key, indexed	Internal auto-incrementing row ID
job_id	String	Unique, indexed, not null	Public-facing UUID for the job
filename	String	Not null	Original uploaded filename
status	String	Not null, default "pending"	pending / processing / completed / failed
created_at	DateTime	Not null, default utcnow()	Job creation time
completed_at	DateTime	Nullable	Set once processing finishes
processing_time	Float	Nullable	Time taken to process (seconds)
total_detections	Integer	Default 0	Number of objects detected across frames
output_file	String	Nullable	Relative path to the processed output video

This is defined in models.py as a single ORM class, VideoJob, mapped to the video_jobs table.

What SQLAlchemy Does Here

SQLAlchemy is the ORM (Object-Relational Mapper) that sits between the Python code and the SQLite database. Concretely, in this project it:

Defines the schema in Python — VideoJob (in models.py) is a Python class that SQLAlchemy translates into the video_jobs SQL table, with each Column(...) becoming a real database column.
Manages the connection — database.py creates a SQLAlchemy engine bound to the SQLite file, using check_same_thread=False so SQLite can be safely used from FastAPI's background tasks/threads.
Handles sessions — SessionLocal is a session factory; the get_db() dependency yields a session per-request and guarantees it's closed afterward (try/finally).
Auto-creates tables — Base.metadata.create_all(bind=engine) in main.py creates the video_jobs table on startup if it doesn't already exist.
Lets you query with Python instead of raw SQL — e.g. db.query(VideoJob).filter(VideoJob.job_id == job_id).first() instead of writing SELECT * FROM video_jobs WHERE job_id = ?.
Tracks and commits changes — when a job's status, completed_at, etc. are updated on the Python object, db.commit() persists those changes back to SQLite.

In short: SQLAlchemy lets the rest of the app treat database rows as ordinary Python objects, while it handles the SQL underneath.

How the API Creates & Retrieves Jobs
Creating a job (POST /video/process)
A video file is uploaded via multipart/form-data.
The file extension is validated against an allow-list (.mp4, .avi, .mov, .mkv).
A new job_id (UUID4) is generated, and the uploaded file is saved to videos/input/.
A VideoJob row is inserted into the database with status="pending".
A background task (process_job) is queued via FastAPI's BackgroundTasks — this means the API responds immediately without waiting for the video to finish processing.
In the background task: the job status is flipped to "processing", the video is run through YOLOv8 (process_video()), and once finished, the row is updated with status="completed", completed_at, processing_time, total_detections, and output_file (or status="failed" if an exception occurs).
Retrieving jobs (GET /jobs/ and GET /jobs/{job_id})
List all jobs — queries every VideoJob row, ordered by created_at descending (most recent first).
Get a single job — queries by job_id; returns 404 if no matching job exists.
Delete a job — looks up the job by job_id, deletes the row if found, otherwise returns 404.

All responses are serialized through the JobResponse Pydantic schema (schemas.py), which mirrors the VideoJob model's fields.

API Endpoints
Method	Path	Description
GET	/	Health check / root message
POST	/video/process	Upload a video and start processing
GET	/jobs/	List all jobs (most recent first)
GET	/jobs/{job_id}	Get a single job by ID
DELETE	/jobs/{job_id}	Delete a job by ID
Example API Requests & Responses
1. Upload a video for processing

Request

http
POST /video/process
Content-Type: multipart/form-data

file: running.mp4

Response 200 OK

json
{
  "message": "Video processing started",
  "job_id": "050bd82e-873c-4644-9580-d40dfc55af6a",
  "status": "pending"
}
2. Check a specific job's status

Request

http
GET /jobs/050bd82e-873c-4644-9580-d40dfc55af6a

Response (while processing) 200 OK

json
{
  "job_id": "050bd82e-873c-4644-9580-d40dfc55af6a",
  "filename": "running.mp4",
  "status": "processing",
  "created_at": "2026-09-07T23:19:10.077000",
  "completed_at": null,
  "processing_time": null,
  "total_detections": 0,
  "output_file": null
}

Response (once completed) 200 OK

json
{
  "job_id": "050bd82e-873c-4644-9580-d40dfc55af6a",
  "filename": "running.mp4",
  "status": "completed",
  "created_at": "2026-09-07T23:19:10.077000",
  "completed_at": "2026-09-07T23:19:37.094000",
  "processing_time": 26.98,
  "total_detections": 919,
  "output_file": "videos/output/050bd82e-873c-4644-9580-d40dfc55af6a_processed.mp4"
}
3. List all jobs

Request

http
GET /jobs/

Response 200 OK

json
[
  {
    "job_id": "050bd82e-873c-4644-9580-d40dfc55af6a",
    "filename": "running.mp4",
    "status": "completed",
    "created_at": "2026-09-07T23:19:10.077000",
    "completed_at": "2026-09-07T23:19:37.094000",
    "processing_time": 26.98,
    "total_detections": 919,
    "output_file": "videos/output/050bd82e-873c-4644-9580-d40dfc55af6a_processed.mp4"
  }
]
4. Job not found

Request

http
GET /jobs/does-not-exist

Response 404 Not Found

json
{
  "detail": "Job not found"
}
5. Unsupported file type

Request

http
POST /video/process
Content-Type: multipart/form-data

file: photo.png

Response 400 Bad Request

json
{
  "detail": "Unsupported video format. Allowed: mp4, avi, mov, mkv"
}
6. Delete a job

Request

http
DELETE /jobs/050bd82e-873c-4644-9580-d40dfc55af6a

Response 200 OK

json
{
  "message": "Job deleted successfully",
  "job_id": "050bd82e-873c-4644-9580-d40dfc55af6a"
}
Logging

All application activity (uploads, job creation, processing start/end, errors) is logged to both the console and app/logs/app.log, configured centrally in core/logging_config.py. Log format:

2026-09-07 23:19:37,077 | INFO | app.services.video_processor | Video processing completed | frames=245 | detections=919 | processing_time=26.98 seconds
Setup & Installation
bash
# 1. Clone/enter the project directory
cd app

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the API
uvicorn app.main:app --reload

The API will be available at http://127.0.0.1:8000, with interactive docs at http://127.0.0.1:8000/docs.

Note: On first run, place a YOLOv8n weights file (yolov8n.pt) in a models/ folder at the project root, since video_processor.py loads the model from models/yolov8n.pt.

Requirements

See requirements.txt. Core dependencies:

fastapi — web framework
uvicorn — ASGI server
sqlalchemy — ORM / database layer
pydantic — request/response validation and serialization
python-multipart — required by FastAPI to handle file uploads
opencv-python — video reading/writing and frame manipulation
ultralytics — YOLOv8 model loading and inference
Conclusion

This project demonstrates a clean, production-style pattern for handling long-running media processing in a web API: accept the upload quickly, hand off the heavy work (YOLOv8 inference) to a background task, and let clients track progress through a persistent job record rather than blocking on the request. SQLAlchemy provides a simple, Pythonic way to define that job schema and persist it to SQLite, while FastAPI's BackgroundTasks, dependency injection (get_db), and Pydantic schemas keep the API layer thin, typed, and easy to extend — for example, by adding authentication, swapping SQLite for PostgreSQL, or supporting additional detection models.
