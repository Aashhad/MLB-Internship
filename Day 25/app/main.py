from fastapi import FastAPI
from app.routes.students import router as student_router


# CREATE FASTAPI APPLICATION

app = FastAPI(
    title="Student Management REST API",
    description="A simple REST API for managing students",
    version="1.0.0"
)


# INCLUDE STUDENT ROUTES
app.include_router(student_router)


# ROOT ENDPOINT

@app.get("/")
def home():
    return {
        "message": "Welcome to Student Management REST API"
    }


# HEALTH CHECK

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "API is running successfully"
    }
