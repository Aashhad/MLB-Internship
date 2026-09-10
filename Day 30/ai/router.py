import shutil
import uuid

from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from database import get_db

from models.user import User

from models.job import ProcessingJob

from schemas.job import JobResponse

from auth.security import (
    get_current_user,
    require_admin
)

from ai.processor import process_video


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/ai",
    tags=["AI Processing"]
)


# ============================================================
# DIRECTORIES
# ============================================================

BASE_DIR = Path(
    __file__
).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"

OUTPUT_DIR = BASE_DIR / "outputs"


UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# ALLOWED VIDEO EXTENSIONS
# ============================================================

ALLOWED_EXTENSIONS = {
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".webm"
}


# ============================================================
# PROCESS VIDEO
# POST /ai/process
# ============================================================

@router.post(
    "/process",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED
)
def process_video_endpoint(

    video: UploadFile = File(...),

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Validate extension
    # --------------------------------------------------------

    original_filename = (
        video.filename
        or "video.mp4"
    )

    extension = Path(
        original_filename
    ).suffix.lower()


    if extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(

            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,

            detail=(
                "Unsupported video format. "
                "Use MP4, AVI, MOV, MKV or WEBM."
            )
        )


    # --------------------------------------------------------
    # Generate safe unique filename
    # --------------------------------------------------------

    unique_name = (
        f"{uuid.uuid4().hex}"
        f"{extension}"
    )


    input_path = (
        UPLOAD_DIR /
        unique_name
    )


    output_name = (
        f"processed_"
        f"{uuid.uuid4().hex}.mp4"
    )


    output_path = (
        OUTPUT_DIR /
        output_name
    )


    # --------------------------------------------------------
    # Save uploaded video
    # --------------------------------------------------------

    try:

        with open(
            input_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                video.file,
                buffer
            )

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=(
                f"Could not save video: {error}"
            )
        )


    # --------------------------------------------------------
    # Create job
    # --------------------------------------------------------

    job = ProcessingJob(

        user_id=current_user.id,

        original_filename=original_filename,

        input_path=str(
            input_path
        ),

        status="processing"
    )


    db.add(job)

    db.commit()

    db.refresh(job)


    # ========================================================
    # PROCESS VIDEO
    # ========================================================

    try:

        result = process_video(

            input_path,

            output_path
        )


        # ----------------------------------------------------
        # Update successful job
        # ----------------------------------------------------

        job.status = "completed"

        job.output_path = str(
            output_path
        )

        job.unique_objects = result[
            "unique_objects"
        ]

        job.frames_processed = result[
            "frames_processed"
        ]

        job.processing_time = result[
            "processing_time"
        ]


        db.commit()

        db.refresh(job)


        return job


    except Exception as error:

        job.status = "failed"

        job.error_message = str(
            error
        )


        db.commit()


        raise HTTPException(

            status_code=500,

            detail=(
                f"Video processing failed: {error}"
            )
        )


# ============================================================
# GET OWN JOBS
# GET /ai/jobs
# ============================================================

@router.get(
    "/jobs",
    response_model=list[JobResponse]
)
def get_my_jobs(

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    jobs = (

        db.query(ProcessingJob)

        .filter(
            ProcessingJob.user_id
            == current_user.id
        )

        .order_by(
            ProcessingJob.created_at.desc()
        )

        .all()
    )


    return jobs


# ============================================================
# GET SINGLE JOB
# GET /ai/jobs/{job_id}
# ============================================================

@router.get(
    "/jobs/{job_id}",
    response_model=JobResponse
)
def get_job(

    job_id: int,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    job = (

        db.query(ProcessingJob)

        .filter(
            ProcessingJob.id == job_id
        )

        .first()
    )


    if not job:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Processing job not found"
        )


    # --------------------------------------------------------
    # Ownership check
    # --------------------------------------------------------

    if job.user_id != current_user.id:

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail=(
                "You are not authorized "
                "to access this job"
            )
        )


    return job


# ============================================================
# DELETE OWN JOB
# DELETE /ai/jobs/{job_id}
# ============================================================

@router.delete(
    "/jobs/{job_id}"
)
def delete_job(

    job_id: int,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    job = (

        db.query(ProcessingJob)

        .filter(
            ProcessingJob.id == job_id
        )

        .first()
    )


    if not job:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Processing job not found"
        )


    # --------------------------------------------------------
    # Ownership check
    # --------------------------------------------------------

    if job.user_id != current_user.id:

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail=(
                "You can only delete "
                "your own jobs"
            )
        )


    # --------------------------------------------------------
    # Delete files
    # --------------------------------------------------------

    input_path = Path(
        job.input_path
    )

    output_path = (
        Path(job.output_path)
        if job.output_path
        else None
    )


    if input_path.exists():

        input_path.unlink()


    if output_path and output_path.exists():

        output_path.unlink()


    # --------------------------------------------------------
    # Delete database record
    # --------------------------------------------------------

    db.delete(job)

    db.commit()


    return {
        "message": "Processing job deleted successfully",
        "job_id": job_id
    }


# ============================================================
# ADMIN - VIEW ALL JOBS
# GET /ai/admin/jobs
# ============================================================

@router.get(
    "/admin/jobs",
    response_model=list[JobResponse]
)
def get_all_jobs(

    admin_user: User = Depends(
        require_admin
    ),

    db: Session = Depends(get_db)
):

    jobs = (

        db.query(ProcessingJob)

        .order_by(
            ProcessingJob.created_at.desc()
        )

        .all()
    )


    return jobs