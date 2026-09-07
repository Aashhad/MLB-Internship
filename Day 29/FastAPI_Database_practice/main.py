from fastapi import FastAPI

from .database import engine, Base
from .routes.jobs import router as jobs_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Video Processing Database API",
    version="1.0.0"
)


# Register routes
app.include_router(jobs_router)


@app.get("/")
def root():

    return {
        "message": "AI Video Processing API is running"
    }