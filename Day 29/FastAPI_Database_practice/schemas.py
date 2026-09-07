from pydantic import BaseModel
from typing import Optional


class JobCreate(BaseModel):

    job_id: str
    video_filename: str
    status: str = "pending"
    processing_time: Optional[float] = None
    detections: int = 0


class JobUpdate(BaseModel):

    status: Optional[str] = None
    processing_time: Optional[float] = None
    detections: Optional[int] = None