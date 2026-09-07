import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions import AppException
from app.logging_config import setup_logging
from app.middleware import request_logging_middleware
from app.routes.video import router


# ============================================================
# LOGGING
# ============================================================

setup_logging()

logger = logging.getLogger(__name__)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Production-Ready AI Video API",
    version="1.0.0",
    description="FastAPI + YOLO Video Processing API"
)


# ============================================================
# MIDDLEWARE
# ============================================================

app.middleware("http")(
    request_logging_middleware
)


# ============================================================
# CUSTOM APPLICATION EXCEPTION
# ============================================================

@app.exception_handler(AppException)
async def app_exception_handler(
    request: Request,
    exc: AppException
):
    request_id = getattr(
        request.state,
        "request_id",
        "unknown"
    )

    logger.warning(
        "Application error | request_id=%s | error=%s",
        request_id,
        exc.message
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.message,
            "request_id": request_id
        }
    )


# ============================================================
# VALIDATION EXCEPTION
# ============================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    request_id = getattr(
        request.state,
        "request_id",
        "unknown"
    )

    logger.warning(
        "Request validation failed | request_id=%s | errors=%s",
        request_id,
        exc.errors()
    )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Invalid request parameters",
            "request_id": request_id
        }
    )


# ============================================================
# GLOBAL EXCEPTION HANDLER
# ============================================================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    request_id = getattr(
        request.state,
        "request_id",
        "unknown"
    )

    logger.exception(
        "Unhandled server error | request_id=%s",
        request_id
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "request_id": request_id
        }
    )


# ============================================================
# ROUTES
# ============================================================

app.include_router(router)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
async def health_check():
    return {
        "success": True,
        "message": "API is healthy"
    }


# ============================================================
# ROOT
# ============================================================

@app.get("/")
async def root():
    return {
        "success": True,
        "message": "Production AI Video API"
    }