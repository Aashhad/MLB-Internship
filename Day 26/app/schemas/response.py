from pydantic import BaseModel
from typing import List


# BOUNDING BOX

class BoundingBox(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int


# SINGLE DETECTION

class Detection(BaseModel):
    class_id: int
    class_name: str
    confidence: float
    bounding_box: BoundingBox


# PREDICTION RESPONSE

class PredictionResponse(BaseModel):
    filename: str
    confidence_threshold: float
    detection_count: int
    detections: List[Detection]