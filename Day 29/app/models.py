from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String
)

from .database import Base


class VideoJob(Base):

    __tablename__ = "video_jobs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    job_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    filename = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        default="pending",
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    completed_at = Column(
        DateTime,
        nullable=True
    )

    processing_time = Column(
        Float,
        nullable=True
    )

    total_detections = Column(
        Integer,
        default=0
    )

    output_file = Column(
        String,
        nullable=True
    )