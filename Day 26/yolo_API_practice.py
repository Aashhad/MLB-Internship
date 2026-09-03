from fastapi import FastAPI, UploadFile, File, HTTPException
from ultralytics import YOLO

import numpy as np
import cv2


# FASTAPI APPLICATION

app = FastAPI(
    title="Helmet Detection API",
    description="AI Inference API using custom YOLO model",
    version="1.0.0"
)


# MODEL

MODEL_PATH = "models/best.pt"

model = YOLO(MODEL_PATH)


# HEALTH CHECK

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


# YOLO PREDICTION

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Validate file type

    if not file.content_type:

        raise HTTPException(
            status_code=400,
            detail="File type could not be determined."
        )

    if not file.content_type.startswith("image/"):

        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an image."
        )

    # Read uploaded file

    contents = await file.read()

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

    # Convert NumPy array to OpenCV image

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if image is None:

        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted image."
        )

    # Run YOLO inference

    results = model(
        image,
        conf=0.25
    )

    # Extract detections

    detections = []

    for result in results:

        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            detections.append(
                {
                    "class": model.names[class_id],

                    "confidence": round(
                        confidence,
                        2
                    ),

                    "bbox": [
                        round(x1, 2),
                        round(y1, 2),
                        round(x2, 2),
                        round(y2, 2)
                    ]
                }
            )

    # Return response

    return {
        "detections": detections,
        "total": len(detections)
    }