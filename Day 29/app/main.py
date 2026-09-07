from fastapi import FastAPI
from .database import Base, engine
from .core.logging_config import setup_logging
from .routes.video import router as video_router
from .routes.jobs import router as jobs_router



# LOGGING

setup_logging()


# DATABASE TABLES

Base.metadata.create_all(
    bind=engine
)


# FASTAPI

app = FastAPI(
    title="AI Video Processing History API",
    version="1.0.0"
)


# ROUTERS

app.include_router(
    video_router
)

app.include_router(
    jobs_router
)


# ROOT

@app.get("/")
def root():

    return {
        "message": "AI Video Processing API is running"
    }