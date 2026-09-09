from datetime import datetime

from pydantic import BaseModel


class JobResponse(BaseModel):

    id: int

    user_id: int

    original_filename: str

    status: str

    unique_objects: int

    frames_processed: int

    processing_time: float

    error_message: str | None

    created_at: datetime

    class Config:
        from_attributes = True