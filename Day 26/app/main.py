from fastapi import FastAPI

from app.routes.prediction import router as prediction_router



# CREATE FASTAPI APPLICATION

app = FastAPI(
    title="Custom YOLO Prediction API",
    description="REST API for custom YOLO object detection",
    version="1.0.0"
)


# INCLUDE ROUTES

app.include_router(prediction_router)


# ROOT ENDPOINT

@app.get("/")
def root():
    return {
        "message": "Welcome to Custom YOLO Prediction API"
    }


# HEALTH CHECK

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "YOLO Prediction API is running"
    }