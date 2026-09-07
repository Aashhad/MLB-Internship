from pydantic import BaseModel
from typing import Optional


class ErrorResponse(BaseModel):

    success: bool
    error: str
    request_id: str


class HealthResponse(BaseModel):

    success: bool
    api_status: str
    model_status: str
    version: str


class JobResponse(BaseModel):

    success: bool
    job_id: str
    request_id: str
    message: str
    status: str


class JobStatusResponse(BaseModel):

    success: bool
    job_id: str
    status: str
    request_id: Optional[str] = None