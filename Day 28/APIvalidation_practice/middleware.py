import logging
import time
import uuid

from fastapi import Request


logger = logging.getLogger(__name__)


# REQUEST LOGGING MIDDLEWARE

async def request_logging_middleware(
    request: Request,
    call_next
):

    request_id = str(uuid.uuid4())

    request.state.request_id = request_id

    start_time = time.perf_counter()

    logger.info(
        "Request started | "
        "request_id=%s | "
        "method=%s | "
        "path=%s",
        request_id,
        request.method,
        request.url.path
    )

    try:

        response = await call_next(request)

        processing_time = (
            time.perf_counter() - start_time
        )

        response.headers[
            "X-Request-ID"
        ] = request_id

        logger.info(
            "Request completed | "
            "request_id=%s | "
            "status_code=%s | "
            "duration=%.3fs",
            request_id,
            response.status_code,
            processing_time
        )

        return response

    except Exception:

        processing_time = (
            time.perf_counter() - start_time
        )

        logger.exception(
            "Request failed | "
            "request_id=%s | "
            "duration=%.3fs",
            request_id,
            processing_time
        )

        raise