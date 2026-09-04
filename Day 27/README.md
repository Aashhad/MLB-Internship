# 🎥 Custom YOLO Video Processing API

A video processing backend built with **FastAPI** and a custom-trained **YOLO model**. The API allows users to upload videos, process them frame-by-frame using YOLO object detection, track the processing status through a Job ID, and retrieve the processed video.

---

## 📌 Project Overview

This project extends the YOLO image prediction API to support **video processing and background jobs**.

Instead of keeping the API request open while a complete video is processed, the system creates a background job and immediately returns a **Job ID**.

The client can then use this Job ID to check the processing status and retrieve the generated video after processing is completed.

### Main Technologies

* Python
* FastAPI
* YOLO / Ultralytics
* OpenCV
* NumPy
* Uvicorn

---

# 🎬 How Video Processing Works

The uploaded video is processed **frame-by-frame**.

The processing workflow is:

```text
User
  |
  | Upload Video
  v
FastAPI
  |
  | Create Job ID
  v
Background Processing
  |
  | Read Video
  v
OpenCV
  |
  | Extract Frames
  v
YOLO Model
  |
  | Detect Objects
  v
Draw Bounding Boxes
  |
  | Write Processed Frames
  v
Processed Video
```

### Processing Steps

1. The client uploads a video through the API.
2. FastAPI validates the uploaded file.
3. A unique Job ID is generated.
4. The video is saved to the input directory.
5. A background task starts processing the video.
6. OpenCV reads the video frame-by-frame.
7. Each frame is passed to the custom YOLO model.
8. YOLO detects objects in the frame.
9. Bounding boxes, class names, and confidence scores are drawn.
10. The processed frame is written to an output video.
11. After all frames are processed, the job status is changed to `completed`.
12. The client can retrieve the processed video.

---

# ⚡ Why Background Processing Is Useful

Video inference can take significantly longer than image inference because a video may contain hundreds or thousands of frames.

If the API processed the entire video inside the original HTTP request, the client would have to wait until the complete video finished processing.

This can cause:

* Long request times
* Request timeouts
* Poor user experience
* Blocked API workers
* Reduced ability to handle multiple requests

Background processing solves this problem by allowing the API to accept the video and return a Job ID immediately.

Instead of:

```text
Upload Video
     ↓
Wait 2 minutes
     ↓
Receive Response
```

the system uses:

```text
Upload Video
     ↓
Receive Job ID
     ↓
Check Status
     ↓
Processing
     ↓
Completed
     ↓
Download Processed Video
```

This makes the API more suitable for longer-running AI tasks.

> **Note:** FastAPI `BackgroundTasks` are useful for basic background processing. For production systems with heavy workloads, dedicated task queues such as Celery, RQ, or distributed workers can provide better scalability.

---

# 🆔 Job and Status Workflow

Each uploaded video receives a unique **Job ID**.

Example:

```text
job_id = 8f7c2a91-3d6b-4e1a-9f21-123456789abc
```

The Job ID is used to identify the processing task.

## Job Lifecycle

```text
QUEUED
   |
   v
PROCESSING
   |
   v
COMPLETED
```

If an error occurs:

```text
PROCESSING
   |
   v
FAILED
```

### Status Values

| Status       | Meaning                                      |
| ------------ | -------------------------------------------- |
| `queued`     | Job has been created and is waiting to start |
| `processing` | Video is currently being processed           |
| `completed`  | Processing finished successfully             |
| `failed`     | Processing failed because of an error        |

The client does not need to keep the original upload request open. It can periodically check the status using the Job ID.

---

# 🔄 Job Workflow Example

### Step 1 — Upload Video

```http
POST /videos
```

The API receives the video and creates a Job ID.

Example response:

```json
{
  "job_id": "12345abc",
  "status": "queued"
}
```

### Step 2 — Check Status

```http
GET /videos/12345abc/status
```

Example response while processing:

```json
{
  "job_id": "12345abc",
  "status": "processing"
}
```

### Step 3 — Processing Completed

```json
{
  "job_id": "12345abc",
  "status": "completed",
  "output_file": "12345abc.mp4"
}
```

The client can then request the processed video.

---

# 🔌 API Endpoints

## 1. Upload Video

```http
POST /videos
```

Uploads a video and starts a background processing job.

### Request

```text
Content-Type: multipart/form-data
```

Example:

```bash
curl -X POST "http://127.0.0.1:8000/videos" \
  -F "file=@input.mp4"
```

### Response

```json
{
  "job_id": "12345abc",
  "status": "queued"
}
```

---

## 2. Check Job Status

```http
GET /videos/{job_id}/status
```

Returns the current status of a video-processing job.

### Example

```http
GET /videos/12345abc/status
```

### Response

```json
{
  "job_id": "12345abc",
  "status": "processing"
}
```

---

## 3. Get Processed Video

```http
GET /videos/{job_id}
```

Returns the generated processed video after successful processing.

Example:

```http
GET /videos/12345abc
```

The endpoint returns the processed video file.

---

# 📦 Request and Response Flow

```text
POST /videos
      |
      v
Upload video
      |
      v
Job ID returned
      |
      v
GET /videos/{job_id}/status
      |
      v
Check status
      |
      +---- processing ----+
      |                    |
      |                    |
      +---- completed <----+
                |
                v
GET /videos/{job_id}
                |
                v
        Processed Video
```

---

# 🚨 Error Handling

The API includes basic validation and error handling to make the video-processing system more reliable.

### Invalid File

If the uploaded file is not a supported video:

```json
{
  "detail": "Invalid video file"
}
```

### Missing Job ID

If the requested Job ID does not exist:

```json
{
  "detail": "Job not found"
}
```

### Video Processing Failure

If an error occurs during YOLO inference or video processing:

```json
{
  "job_id": "12345abc",
  "status": "failed"
}
```

### Output File Not Available

If the client requests a video before processing is completed, the API returns an appropriate error instead of returning an incomplete file.

---

# 📊 Average Processing Performance

Video processing performance depends on several factors:

* Video resolution
* Number of frames
* FPS
* YOLO model size
* Image size used for inference
* CPU/GPU availability
* Confidence threshold
* Number of detected objects

For local CPU-based testing, processing is generally slower than real-time video playback because YOLO inference must be performed on every frame.

### Example Performance Format

| Video      | Resolution | Model       | Device | Processing Speed |
| ---------- | ---------- | ----------- | ------ | ---------------- |
| Test Video | 640p       | Custom YOLO | CPU    | ~5–10 FPS        |

For example, a 30-second video at 30 FPS contains approximately:

```text
30 × 30 = 900 frames
```

If the system processes approximately 8 frames per second:

```text
900 ÷ 8 ≈ 113 seconds
```

Therefore, the processing time can be longer than the original video duration when running inference on CPU.

> **Performance should be updated with the actual benchmark from your machine.**

---

# 🛠️ Problems Faced and Solutions

## 1. Long Video Processing Time

### Problem

Processing every frame with YOLO takes time, especially when running inference on CPU.

### Solution

Background processing was implemented so that the API does not make the client wait for the entire inference operation.

The client receives a Job ID immediately and can check the status separately.

---

## 2. Handling Large Video Files

### Problem

Video files are considerably larger than images and can consume significant memory and disk space.

### Solution

The uploaded video is saved to disk and processed frame-by-frame rather than loading the complete video into memory.

This keeps memory usage more manageable.

---

## 3. Tracking Processing Status

### Problem

The client needs to know whether the video is still processing or has completed.

### Solution

A Job ID and status workflow was implemented:

```text
queued
   ↓
processing
   ↓
completed
```

or:

```text
queued
   ↓
processing
   ↓
failed
```

---

## 4. Video Encoding / Browser Compatibility

### Problem

OpenCV's `VideoWriter` can produce videos using codecs that are not supported by some browsers or video players.

For example, an MP4 container does not automatically mean that the video uses browser-friendly H.264 encoding.

### Solution

The generated video can be re-encoded using **FFmpeg** with H.264 when necessary.

This improves compatibility with modern browsers and video players.

---

## 5. Frame-by-Frame Processing

### Problem

Running YOLO directly on a complete video can make it difficult to control the processing pipeline and output video generation.

### Solution

OpenCV is used to:

1. Open the video.
2. Read one frame at a time.
3. Run YOLO inference.
4. Draw detections.
5. Write the processed frame.
6. Continue until the video ends.

This provides better control over video processing.

---

# 📁 Project Structure

```text
Project/
│
├── app/
│   ├── main.py
│   │
│   ├── routes/
│   │   └── video.py
│   │
│   ├── services/
│   │   ├── detector.py
│   │   └── video_processor.py
│   │
│   └── schemas/
│       └── video.py
│
├── models/
│   └── best.pt
│
├── videos/
│   ├── input/
│   └── output/
│
├── requirements.txt
└── README.md
```

---

# ▶️ Running the API

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

---

# 📚 API Documentation

FastAPI automatically generates interactive Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

You can use Swagger UI to:

* Upload videos
* Start processing jobs
* Check Job IDs
* Monitor processing status
* Retrieve processed videos
* Test API endpoints

---

# 🧠 Key Concepts Learned

This project demonstrates several important AI backend concepts:

* FastAPI
* REST APIs
* Video uploads
* OpenCV video processing
* Frame-by-frame inference
* YOLO inference
* Background processing
* Job IDs
* Processing status
* Error handling
* Large file handling
* Video encoding
* Generated file responses
* Swagger/OpenAPI documentation

---

# 🎯 Conclusion

This project demonstrates how a custom YOLO computer vision model can be extended from image inference to **video processing through a FastAPI backend**.

The system processes videos frame-by-frame, applies YOLO object detection, generates a processed video, and uses background processing to prevent long-running AI inference from blocking the initial API request.

The Job ID and status workflow provides a simple asynchronous architecture where clients can upload a video, receive a Job ID, monitor the processing status, and retrieve the final processed video once processing is complete.

Overall, this project provides practical experience in combining **Computer Vision, YOLO, OpenCV, FastAPI, background processing, and REST API development** into a complete AI backend application.

---

# 👨‍💻 Author

**Muhammad Ashhad**

