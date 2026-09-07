import logging
import time
import uuid

from fastapi import Request


logger = logging.getLogger(__name__)


async def request_logging_middleware(
    request: Request,
    call_next
):

    request_id = f"req_{uuid.uuid4().hex[:12]}"

    # Store request ID so routes can access it
    request.state.request_id = request_id

    start_time = time.perf_counter()

    logger.info(
        "Request started | request_id=%s | method=%s | path=%s",
        request_id,
        request.method,
        request.url.path
    )

    try:

        response = await call_next(request)

        process_time = (
            time.perf_counter() - start_time
        )

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "Request completed | request_id=%s | "
            "status=%s | duration=%.3fs",
            request_id,
            response.status_code,
            process_time
        )

        return response

    except Exception:

        process_time = (
            time.perf_counter() - start_time
        )

        logger.exception(
            "Request failed | request_id=%s | "
            "duration=%.3fs",
            request_id,
            process_time
        )

        raise