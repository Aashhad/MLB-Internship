import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from ..database import get_db
from ..models import VideoJob
from ..schemas import JobResponse


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/jobs",
    tags=["Job History"]
)


# GET ALL JOBS

@router.get(
    "/",
    response_model=list[JobResponse]
)
def get_jobs(
    db: Session = Depends(get_db)
):

    logger.info(
        "Fetching all video processing jobs"
    )

    jobs = (
        db.query(VideoJob)
        .order_by(
            VideoJob.created_at.desc()
        )
        .all()
    )

    return jobs


# GET JOB BY ID

@router.get(
    "/{job_id}",
    response_model=JobResponse
)
def get_job(
    job_id: str,
    db: Session = Depends(get_db)
):

    logger.info(
        "Fetching job | job_id=%s",
        job_id
    )

    job = (
        db.query(VideoJob)
        .filter(
            VideoJob.job_id == job_id
        )
        .first()
    )

    if not job:

        logger.warning(
            "Job not found | job_id=%s",
            job_id
        )

        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job


# DELETE JOB

@router.delete("/{job_id}")
def delete_job(
    job_id: str,
    db: Session = Depends(get_db)
):

    logger.info(
        "Deleting job | job_id=%s",
        job_id
    )

    job = (
        db.query(VideoJob)
        .filter(
            VideoJob.job_id == job_id
        )
        .first()
    )

    if not job:

        logger.warning(
            "Delete failed - job not found | "
            "job_id=%s",
            job_id
        )

        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    db.delete(job)

    db.commit()

    logger.info(
        "Job deleted | job_id=%s",
        job_id
    )

    return {
        "message": "Job deleted successfully",
        "job_id": job_id
    }