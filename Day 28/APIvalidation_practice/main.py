import logging
from fastapi import (FastAPI, Request)
from fastapi.exceptions import (RequestValidationError)
from fastapi.responses import JSONResponse
from APIvalidation_practice.exceptions import AppException
from APIvalidation_practice.logging_config import setup_logging
from APIvalidation_practice.middleware import request_logging_middleware
from APIvalidation_practice.routes.video import router
from APIvalidation_practice.services.detector import is_model_ready


# APPLICATION CONFIG
APP_VERSION = "1.0.0"


# LOGGING
setup_logging()

logger = logging.getLogger(__name__)


# FASTAPI APPLICATION

app = FastAPI(
    title="Production-Ready AI Video API",
    version=APP_VERSION,
    description=(
        "FastAPI + YOLO Video Processing API"
    )
)


# MIDDLEWARE

app.middleware("http")(
    request_logging_middleware
)


# CUSTOM APPLICATION EXCEPTION

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
        "Application error | "
        "request_id=%s | status=%s | error=%s",
        request_id,
        exc.status_code,
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


# VALIDATION EXCEPTION

@app.exception_handler(
    RequestValidationError
)
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
        "Request validation failed | "
        "request_id=%s | errors=%s",
        request_id,
        exc.errors()
    )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Invalid request parameters.",
            "details": exc.errors(),
            "request_id": request_id
        }
    )


# GLOBAL EXCEPTION HANDLER

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
        "Unhandled server error | "
        "request_id=%s",
        request_id
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error.",
            "request_id": request_id
        }
    )


# ROUTES

app.include_router(router)


# HEALTH CHECK

@app.get("/health")
async def health_check():

    model_status = (
        "ready"
        if is_model_ready()
        else "unavailable"
    )

    api_status = (
        "healthy"
        if is_model_ready()
        else "degraded"
    )

    return {
        "success": True,
        "api_status": api_status,
        "model_status": model_status,
        "version": APP_VERSION
    }


# ROOT

@app.get("/")
async def root():

    return {
        "success": True,
        "message": "Production AI Video API",
        "version": APP_VERSION
    } 