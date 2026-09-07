import logging
import uuid
from pathlib import Path

from fastapi import (
    APIRouter,
    BackgroundTasks,
    File,
    Query,
    Request,
    UploadFile
)
from fastapi.responses import JSONResponse

from app.config import (
    ALLOWED_VIDEO_CONTENT_TYPES,
    ALLOWED_VIDEO_EXTENSIONS,
    DEFAULT_CONFIDENCE,
    MAX_CONFIDENCE,
    MAX_VIDEO_SIZE,
    MIN_CONFIDENCE,
    INPUT_DIR,
    OUTPUT_DIR
)

from app.exceptions import AppException

from app.services.video_processor import process_video


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/video",
    tags=["Video"]
)


# ============================================================
# BACKGROUND JOB
# ============================================================

def run_video_job(
    input_path: Path,
    output_path: Path,
    confidence: float,
    job_id: str,
    request_id: str
):

    try:

        process_video(
            input_path=input_path,
            output_path=output_path,
            confidence=confidence,
            job_id=job_id,
            request_id=request_id
        )

        logger.info(
            "Job finished successfully | "
            "job_id=%s | request_id=%s",
            job_id,
            request_id
        )

    except Exception:

        logger.exception(
            "Background job failed | "
            "job_id=%s | request_id=%s",
            job_id,
            request_id
        )


# ============================================================
# VIDEO ENDPOINT
# ============================================================

@router.post("/process")
async def process_video_endpoint(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    confidence: float = Query(
        DEFAULT_CONFIDENCE,
        ge=MIN_CONFIDENCE,
        le=MAX_CONFIDENCE
    )
):

    request_id = request.state.request_id

    # ========================================================
    # CREATE JOB ID
    # ========================================================

    job_id = f"job_{uuid.uuid4().hex[:12]}"

    logger.info(
        "Video upload received | "
        "request_id=%s | job_id=%s",
        request_id,
        job_id
    )

    # ========================================================
    # FILE NAME VALIDATION
    # ========================================================

    if not file.filename:

        raise AppException(
            "Video filename is required",
            status_code=400
        )

    # ========================================================
    # EXTENSION VALIDATION
    # ========================================================

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in ALLOWED_VIDEO_EXTENSIONS:

        logger.warning(
            "Unsupported file format | "
            "request_id=%s | job_id=%s | extension=%s",
            request_id,
            job_id,
            extension
        )

        raise AppException(
            "Unsupported video format",
            status_code=415
        )

    # ========================================================
    # MIME TYPE VALIDATION
    # ========================================================

    if (
        file.content_type
        and file.content_type
        not in ALLOWED_VIDEO_CONTENT_TYPES
    ):

        logger.warning(
            "Unsupported MIME type | "
            "request_id=%s | job_id=%s",
            request_id,
            job_id
        )

        raise AppException(
            "Unsupported video content type",
            status_code=415
        )

    # ========================================================
    # SAVE UPLOAD
    # ========================================================

    input_path = (
        INPUT_DIR /
        f"{job_id}{extension}"
    )

    output_path = (
        OUTPUT_DIR /
        f"{job_id}.mp4"
    )

    total_size = 0

    try:

        with input_path.open("wb") as buffer:

            while True:

                chunk = await file.read(1024 * 1024)

                if not chunk:
                    break

                total_size += len(chunk)

                # ============================================
                # FILE SIZE VALIDATION
                # ============================================

                if total_size > MAX_VIDEO_SIZE:

                    logger.warning(
                        "Video file too large | "
                        "request_id=%s | job_id=%s",
                        request_id,
                        job_id
                    )

                    buffer.close()

                    input_path.unlink(
                        missing_ok=True
                    )

                    raise AppException(
                        "Video file exceeds maximum allowed size of 100 MB",
                        status_code=413
                    )

                buffer.write(chunk)

    except AppException:
        raise

    except Exception:

        input_path.unlink(
            missing_ok=True
        )

        logger.exception(
            "Failed to save uploaded video | "
            "request_id=%s | job_id=%s",
            request_id,
            job_id
        )

        raise AppException(
            "Failed to save uploaded video",
            status_code=500
        )

    finally:

        await file.close()

    # ========================================================
    # START BACKGROUND PROCESSING
    # ========================================================

    background_tasks.add_task(
        run_video_job,
        input_path,
        output_path,
        confidence,
        job_id,
        request_id
    )

    logger.info(
        "Video accepted for processing | "
        "request_id=%s | job_id=%s",
        request_id,
        job_id
    )

    # ========================================================
    # RESPONSE
    # ========================================================

    return {
        "success": True,
        "message": "Video processing started",
        "request_id": request_id,
        "job_id": job_id
    }