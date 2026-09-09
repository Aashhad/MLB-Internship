from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime
)

from datetime import datetime, timezone

from database import Base


class ProcessingJob(Base):

    __tablename__ = "processing_jobs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    original_filename = Column(
        String(255),
        nullable=False
    )

    input_path = Column(
        String(500),
        nullable=False
    )

    output_path = Column(
        String(500),
        nullable=True
    )

    status = Column(
        String(30),
        nullable=False,
        default="pending"
    )

    unique_objects = Column(
        Integer,
        default=0
    )

    frames_processed = Column(
        Integer,
        default=0
    )

    processing_time = Column(
        Float,
        default=0.0
    )

    error_message = Column(
        String(1000),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )