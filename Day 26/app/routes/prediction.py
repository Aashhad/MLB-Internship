from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Query
)

from fastapi.responses import Response

import cv2
import numpy as np

from app.services.detector import detector
from app.schemas.response import PredictionResponse


# CREATE ROUTER

router = APIRouter(
    prefix="/predict",
    tags=["YOLO Prediction"]
)


# ALLOWED IMAGE TYPES

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/jpg",
    "image/webp"
}


# READ AND VALIDATE IMAGE

async def read_image(file: UploadFile):

    # Check file type

    if file.content_type not in ALLOWED_CONTENT_TYPES:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Please upload JPG, JPEG, PNG, or WEBP."
            )
        )

    # Read file

    contents = await file.read()

    # Check empty file

    if not contents:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # Convert bytes to NumPy array

    image_array = np.frombuffer(
        contents,
        dtype=np.uint8
    )

    # Decode image

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    # Invalid image check

    if image is None:

        raise HTTPException(
            status_code=400,
            detail="Invalid image file. Unable to decode image."
        )

    return image


# JSON PREDICTION ENDPOINT
# POST /predict

@router.post(
    "",
    response_model=PredictionResponse
)
async def predict_image(
    file: UploadFile = File(...),
    confidence: float = Query(
        0.25,
        ge=0.0,
        le=1.0,
        description="YOLO confidence threshold between 0 and 1"
    )
):

    # Read and validate image
    image = await read_image(file)

    # Run YOLO inference
    detections, _ = detector.predict(
        image=image,
        confidence=confidence
    )

    # Return JSON response
    return {
        "filename": file.filename,
        "confidence_threshold": confidence,
        "detection_count": len(detections),
        "detections": detections
    }


# PROCESSED IMAGE ENDPOINT
# POST /predict/image

@router.post(
    "/image"
)
async def predict_processed_image(
    file: UploadFile = File(...),
    confidence: float = Query(
        0.25,
        ge=0.0,
        le=1.0,
        description="YOLO confidence threshold between 0 and 1"
    )
):

    # Read and validate image
    image = await read_image(file)

    # Run YOLO inference
    detections, _ = detector.predict(
        image=image,
        confidence=confidence
    )

    # Draw bounding boxes
    processed_image = detector.draw_predictions(
        image=image,
        detections=detections
    )

    # Encode image as JPEG
    success, encoded_image = cv2.imencode(
        ".jpg",
        processed_image
    )

    if not success:

        raise HTTPException(
            status_code=500,
            detail="Failed to encode processed image."
        )

    # Return processed image
    return Response(
        content=encoded_image.tobytes(),
        media_type="image/jpeg",
        headers={
            "Content-Disposition": (
                f'inline; filename="prediction_{file.filename}"'
            )
        }
    )