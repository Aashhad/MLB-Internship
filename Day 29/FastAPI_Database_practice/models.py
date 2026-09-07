from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from .database import Base


class VideoJob(Base):

    __tablename__ = "video_jobs"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    video_filename = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        default="pending"
    )

    processing_time = Column(
        Float,
        nullable=True
    )

    detections = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )