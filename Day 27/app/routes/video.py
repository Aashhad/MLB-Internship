from pathlib import Path
from uuid import uuid4
from threading import Lock

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    BackgroundTasks,
    Query
)

from fastapi.responses import FileResponse

from app.utils.file_utils import (
    create_directories,
    validate_video_file,
    save_upload,
    UPLOAD_DIR,
    OUTPUT_DIR
)

from app.services.video_processor import process_video


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/video",
    tags=["Video Processing"]
)


# ============================================================
# JOB STORAGE
# ============================================================

jobs = {}

jobs_lock = Lock()


# ============================================================
# CREATE DIRECTORIES
# ============================================================

create_directories()


# ============================================================
# BACKGROUND PROCESSING FUNCTION
# ============================================================

def run_video_processing(
    job_id: str,
    input_path: Path,
    output_path: Path,
    confidence: float
):

    try:

        # ----------------------------------------------------
        # UPDATE STATUS
        # ----------------------------------------------------

        with jobs_lock:

            jobs[job_id]["status"] = "processing"
            jobs[job_id]["progress"] = 0

        # ----------------------------------------------------
        # PROCESS VIDEO
        # ----------------------------------------------------

        statistics = process_video(
            input_path=input_path,
            output_path=output_path,
            confidence=confidence,
            status_store=jobs,
            job_id=job_id
        )

        # ----------------------------------------------------
        # COMPLETED
        # ----------------------------------------------------

        with jobs_lock:

            jobs[job_id]["status"] = "completed"
            jobs[job_id]["progress"] = 100
            jobs[job_id]["statistics"] = statistics

    except Exception as error:

        # ----------------------------------------------------
        # PROCESSING FAILED
        # ----------------------------------------------------

        with jobs_lock:

            jobs[job_id]["status"] = "failed"
            jobs[job_id]["progress"] = 0
            jobs[job_id]["error"] = str(error)

        # ----------------------------------------------------
        # CLEANUP OUTPUT
        # ----------------------------------------------------

        if output_path.exists():

            try:
                output_path.unlink()

            except OSError:
                pass


# ============================================================
# POST /video/process
# ============================================================

@router.post("/process")
async def process_video_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    confidence: float = Query(
        default=0.25,
        ge=0.0,
        le=1.0
    )
):

    # ========================================================
    # CHECK FILE
    # ========================================================

    if file is None:
        raise HTTPException(
            status_code=400,
            detail="Video file is required."
        )

    # ========================================================
    # VALIDATE FILE
    # ========================================================

    try:

        validate_video_file(
            filename=file.filename,
            content_type=file.content_type
        )

    except ValueError as error:

        raise HTTPException(
            status_code=415,
            detail=str(error)
        )

    # ========================================================
    # CREATE JOB ID
    # ========================================================

    job_id = uuid4().hex

    # ========================================================
    # FILE PATHS
    # ========================================================

    input_extension = (
        Path(file.filename).suffix.lower()
    )

    input_path = (
        UPLOAD_DIR /
        f"{job_id}{input_extension}"
    )

    output_path = (
        OUTPUT_DIR /
        f"{job_id}_processed.mp4"
    )

    # ========================================================
    # SAVE UPLOADED VIDEO
    # ========================================================

    try:

        save_upload(
            upload_file=file,
            destination=input_path
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to save uploaded video: {error}"
        )

    # ========================================================
    # CHECK FILE SIZE
    # ========================================================

    if not input_path.exists() or input_path.stat().st_size == 0:

        if input_path.exists():
            input_path.unlink()

        raise HTTPException(
            status_code=400,
            detail="Uploaded video is empty."
        )

    # ========================================================
    # CREATE JOB
    # ========================================================

    with jobs_lock:

        jobs[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "progress": 0,
            "statistics": None,
            "error": None,
            "input_file": str(input_path),
            "output_file": str(output_path),
            "confidence": confidence
        }

    # ========================================================
    # START BACKGROUND TASK
    # ========================================================

    background_tasks.add_task(
        run_video_processing,
        job_id,
        input_path,
        output_path,
        confidence
    )

    # ========================================================
    # RESPONSE
    # ========================================================

    return {
        "job_id": job_id,
        "status": "processing"
    }


# ============================================================
# GET /video/status/{job_id}
# ============================================================

@router.get("/status/{job_id}")
async def get_video_status(
    job_id: str
):

    # ========================================================
    # CHECK JOB
    # ========================================================

    with jobs_lock:

        job = jobs.get(job_id)

        if job is None:

            raise HTTPException(
                status_code=404,
                detail="Job not found."
            )

        # Make a copy so we don't expose internal dictionary
        job_data = job.copy()

    # ========================================================
    # RESPONSE
    # ========================================================

    response = {
        "job_id": job_data["job_id"],
        "status": job_data["status"],
        "progress": job_data["progress"]
    }

    # ========================================================
    # STATISTICS
    # ========================================================

    if job_data["statistics"] is not None:

        response["statistics"] = (
            job_data["statistics"]
        )

    # ========================================================
    # ERROR
    # ========================================================

    if job_data["error"] is not None:

        response["error"] = job_data["error"]

    return response


# ============================================================
# GET /video/result/{job_id}
# ============================================================

@router.get("/result/{job_id}")
async def get_video_result(
    job_id: str
):

    # ========================================================
    # CHECK JOB
    # ========================================================

    with jobs_lock:

        job = jobs.get(job_id)

        if job is None:

            raise HTTPException(
                status_code=404,
                detail="Job not found."
            )

        job_data = job.copy()

    # ========================================================
    # CHECK STATUS
    # ========================================================

    if job_data["status"] == "queued":

        raise HTTPException(
            status_code=202,
            detail="Video processing has not started yet."
        )

    if job_data["status"] == "processing":

        raise HTTPException(
            status_code=202,
            detail="Video is still being processed."
        )

    if job_data["status"] == "failed":

        raise HTTPException(
            status_code=500,
            detail=job_data["error"] or
            "Video processing failed."
        )

    # ========================================================
    # CHECK OUTPUT FILE
    # ========================================================

    output_path = Path(
        job_data["output_file"]
    )

    if not output_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Processed video file not found."
        )

    # ========================================================
    # RETURN FILE
    # ========================================================

    return FileResponse(
        path=output_path,
        media_type="video/mp4",
        filename=f"{job_id}_processed.mp4"
    )