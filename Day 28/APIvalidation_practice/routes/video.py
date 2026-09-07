import logging
import time
import uuid

from pathlib import Path

from fastapi import (
    APIRouter,
    File,
    Query,
    Request,
    UploadFile
)

from APIvalidation_practice.exceptions import AppException
from APIvalidation_practice.services.video_processor import process_video


logger = logging.getLogger(__name__)


# ROUTER

router = APIRouter(
    prefix="/video",
    tags=["Video Processing"]
)


# PROJECT DIRECTORIES

# APIvalidation_practice/
BASE_DIR = Path(__file__).resolve().parent.parent

# APIvalidation_practice/uploads/
UPLOAD_DIR = BASE_DIR / "uploads"

# APIvalidation_practice/outputs/
OUTPUT_DIR = BASE_DIR / "outputs"


# Create directories if they don't exist
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# CONFIGURATION

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

ALLOWED_EXTENSIONS = {
    ".mp4",
    ".avi",
    ".mov",
    ".mkv"
}

MIN_CONFIDENCE = 0.0
MAX_CONFIDENCE = 1.0


# JOB STORAGE

jobs = {}


# VIDEO PROCESSING

@router.post("/process")
async def process_video_endpoint(
    request: Request,
    file: UploadFile = File(...),
    confidence: float = Query(
        0.25,
        ge=MIN_CONFIDENCE,
        le=MAX_CONFIDENCE,
        description="YOLO confidence threshold"
    )
):

    request_id = request.state.request_id

    # VALIDATE FILE

    if file is None:

        raise AppException(
            "Video file is required.",
            400
        )

    if not file.filename:

        raise AppException(
            "Uploaded file has no filename.",
            400
        )

    # VALIDATE EXTENSION

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:

        raise AppException(
            (
                "Unsupported file format. "
                "Supported formats: "
                "mp4, avi, mov, mkv."
            ),
            415
        )

    # CREATE JOB ID

    job_id = str(
        uuid.uuid4()
    )

    # FILE PATHS

    input_path = (
        UPLOAD_DIR /
        f"{job_id}{extension}"
    )

    output_path = (
        OUTPUT_DIR /
        f"{job_id}_processed.mp4"
    )

    # SAVE UPLOADED FILE

    total_size = 0

    try:

        with input_path.open("wb") as buffer:

            while True:

                chunk = await file.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                total_size += len(chunk)

                # FILE SIZE VALIDATION

                if total_size > MAX_FILE_SIZE:

                    input_path.unlink(
                        missing_ok=True
                    )

                    raise AppException(
                        (
                            "File is too large. "
                            "Maximum allowed size is 50 MB."
                        ),
                        413
                    )

                buffer.write(chunk)

    except AppException:

        raise

    except Exception:

        input_path.unlink(
            missing_ok=True
        )

        logger.exception(
            "Failed to save uploaded file | "
            "request_id=%s | job_id=%s",
            request_id,
            job_id
        )

        raise AppException(
            "Failed to upload video.",
            500
        )

    finally:

        await file.close()

    # EMPTY FILE VALIDATION

    if total_size == 0:

        input_path.unlink(
            missing_ok=True
        )

        raise AppException(
            "Uploaded video is empty.",
            400
        )

    # CREATE JOB

    jobs[job_id] = {
        "status": "processing",
        "request_id": request_id,
        "filename": file.filename,
        "confidence": confidence,
        "created_at": time.time()
    }

    logger.info(
        "Video job created | "
        "request_id=%s | job_id=%s | "
        "filename=%s | size=%s | confidence=%.2f",
        request_id,
        job_id,
        file.filename,
        total_size,
        confidence
    )

    # PROCESS VIDEO

    try:

        result = process_video(
            input_path=input_path,
            output_path=output_path,
            confidence=confidence,
            job_id=job_id
        )

        jobs[job_id].update({
            "status": "completed",
            "result": result
        })

        logger.info(
            "Video processing completed | "
            "request_id=%s | job_id=%s",
            request_id,
            job_id
        )

    except ValueError as exc:

        jobs[job_id].update({
            "status": "failed",
            "error": str(exc)
        })

        logger.warning(
            "Video processing failed | "
            "request_id=%s | job_id=%s | error=%s",
            request_id,
            job_id,
            str(exc)
        )

        raise AppException(
            str(exc),
            422
        )

    except Exception:

        jobs[job_id].update({
            "status": "failed",
            "error": "Video processing failed"
        })

        logger.exception(
            "Unexpected video processing error | "
            "request_id=%s | job_id=%s",
            request_id,
            job_id
        )

        raise AppException(
            "Video processing failed.",
            500
        )

    # RESPONSE

    return {
        "success": True,
        "message": "Video processed successfully.",
        "job_id": job_id,
        "request_id": request_id,
        "status": "completed",
        "processing": result
    }


# JOB STATUS

@router.get("/jobs/{job_id}")
async def get_job_status(
    job_id: str,
    request: Request
):

    request_id = request.state.request_id

    # VALIDATE JOB ID

    if not job_id:

        raise AppException(
            "Job ID is required.",
            400
        )

    # FIND JOB

    job = jobs.get(job_id)

    if job is None:

        logger.warning(
            "Invalid job ID | "
            "request_id=%s | job_id=%s",
            request_id,
            job_id
        )

        raise AppException(
            "Job not found.",
            404
        )

    # RESPONSE

    return {
        "success": True,
        "job_id": job_id,
        "status": job["status"],
        "request_id": job.get("request_id"),
        "error": job.get("error")
    }
