import logging
import shutil
import time
import uuid

from pathlib import Path

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    UploadFile
)

from sqlalchemy.orm import Session

from ..database import SessionLocal, get_db
from ..models import VideoJob
from ..services.video_processor import process_video


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/video",
    tags=["Video Processing"]
)


# PATHS

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INPUT_DIR = BASE_DIR / "videos" / "input"
OUTPUT_DIR = BASE_DIR / "videos" / "output"

INPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# BACKGROUND PROCESSING

def process_job(
    job_id: str,
    input_path: Path,
    output_path: Path
):

    db = SessionLocal()

    try:

        logger.info(
            "Background job started | job_id=%s",
            job_id
        )

        # Get job

        job = (
            db.query(VideoJob)
            .filter(
                VideoJob.job_id == job_id
            )
            .first()
        )

        if not job:

            logger.error(
                "Job not found | job_id=%s",
                job_id
            )

            return

        # Update status

        job.status = "processing"

        db.commit()

        # YOLO PROCESSING

        result = process_video(
            input_path,
            output_path
        )

        # Update results

        job.status = "completed"

        job.completed_at = (
            __import__("datetime")
            .datetime.utcnow()
        )

        job.processing_time = (
            result["processing_time"]
        )

        job.total_detections = (
            result["total_detections"]
        )

        job.output_file = str(
            output_path.relative_to(BASE_DIR)
        )

        db.commit()

        logger.info(
            "Job completed | job_id=%s",
            job_id
        )

    except Exception as exc:

        logger.exception(
            "Job failed | job_id=%s | error=%s",
            job_id,
            exc
        )

        job = (
            db.query(VideoJob)
            .filter(
                VideoJob.job_id == job_id
            )
            .first()
        )

        if job:

            job.status = "failed"

            db.commit()

    finally:

        db.close()


# POST /video/process

@router.post("/process")
async def process_video_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    start_time = time.time()

    logger.info(
        "Video upload received | filename=%s",
        file.filename
    )

    # VALIDATION

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    allowed_extensions = {
        ".mp4",
        ".avi",
        ".mov",
        ".mkv"
    }

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in allowed_extensions:

        logger.warning(
            "Invalid video format | filename=%s",
            file.filename
        )

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported video format. "
                "Allowed: mp4, avi, mov, mkv"
            )
        )

    # CREATE JOB ID

    job_id = str(uuid.uuid4())

    input_filename = (
        f"{job_id}{extension}"
    )

    input_path = INPUT_DIR / input_filename

    output_filename = (
        f"{job_id}_processed.mp4"
    )

    output_path = (
        OUTPUT_DIR / output_filename
    )

    # SAVE UPLOADED VIDEO

    try:

        with input_path.open("wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

    except Exception as exc:

        logger.exception(
            "Failed to save uploaded video"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to save video"
        )

    # CREATE DATABASE RECORD

    job = VideoJob(

        job_id=job_id,

        filename=file.filename,

        status="pending",

        total_detections=0
    )

    db.add(job)

    db.commit()

    db.refresh(job)

    logger.info(
        "Job created | job_id=%s",
        job_id
    )

    # ADD BACKGROUND TASK


    background_tasks.add_task(
        process_job,
        job_id,
        input_path,
        output_path
    )

    request_time = (
        time.time() - start_time
    )

    logger.info(
        "Request completed | "
        "job_id=%s | request_time=%.2f",
        job_id,
        request_time
    )

    return {
        "message": "Video processing started",
        "job_id": job_id,
        "status": "pending"
    }