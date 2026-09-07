from typing import Any, Optional

from pydantic import BaseModel


class APIResponse(BaseModel):

    success: bool

    message: Optional[str] = None

    request_id: str

    job_id: Optional[str] = None

    data: Optional[Any] = None

    error: Optional[str] = None