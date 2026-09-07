import logging

from ultralytics import YOLO

from app.config import MODEL_PATH


logger = logging.getLogger(__name__)


class YOLODetector:

    def __init__(self):

        logger.info(
            "Loading YOLO model"
        )

        self.model = YOLO(str(MODEL_PATH))

        logger.info(
            "YOLO model loaded successfully"
        )

    def predict(
        self,
        frame,
        confidence: float
    ):

        results = self.model.predict(
            source=frame,
            conf=confidence,
            verbose=False
        )

        return results


# Load model once when application starts
detector = YOLODetector()