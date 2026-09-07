from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import VideoJob
from ..schemas import JobCreate, JobUpdate


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


# CREATE

@router.post("/")
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db)
):

    existing_job = (
        db.query(VideoJob)
        .filter(VideoJob.job_id == job.job_id)
        .first()
    )

    if existing_job:
        raise HTTPException(
            status_code=400,
            detail="Job ID already exists"
        )

    new_job = VideoJob(
        job_id=job.job_id,
        video_filename=job.video_filename,
        status=job.status,
        processing_time=job.processing_time,
        detections=job.detections
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


# READ ALL

@router.get("/")
def get_jobs(
    db: Session = Depends(get_db)
):

    jobs = db.query(VideoJob).all()

    return jobs


# SEARCH BY JOB ID

@router.get("/{job_id}")
def get_job(
    job_id: str,
    db: Session = Depends(get_db)
):

    job = (
        db.query(VideoJob)
        .filter(VideoJob.job_id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job


# UPDATE

@router.put("/{job_id}")
def update_job(
    job_id: str,
    job_data: JobUpdate,
    db: Session = Depends(get_db)
):

    job = (
        db.query(VideoJob)
        .filter(VideoJob.job_id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    if job_data.status is not None:
        job.status = job_data.status

    if job_data.processing_time is not None:
        job.processing_time = job_data.processing_time

    if job_data.detections is not None:
        job.detections = job_data.detections

    db.commit()
    db.refresh(job)

    return job


# DELETE

@router.delete("/{job_id}")
def delete_job(
    job_id: str,
    db: Session = Depends(get_db)
):

    job = (
        db.query(VideoJob)
        .filter(VideoJob.job_id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    db.delete(job)
    db.commit()

    return {
        "message": "Job deleted successfully",
        "job_id": job_id
    }