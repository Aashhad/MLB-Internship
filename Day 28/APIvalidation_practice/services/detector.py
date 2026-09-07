import logging

from pathlib import Path

from ultralytics import YOLO


logger = logging.getLogger(__name__)



# MODEL PATH

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODEL_PATH = BASE_DIR / "models" / "yolov8n.pt"


# MODEL

model = None


try:

    if MODEL_PATH.exists():

        model = YOLO(str(MODEL_PATH))

        logger.info(
            "YOLO model loaded | path=%s",
            MODEL_PATH
        )

    else:

        logger.error(
            "YOLO model not found | path=%s",
            MODEL_PATH
        )

except Exception:

    logger.exception(
        "Failed to load YOLO model"
    )


# MODEL STATUS

def is_model_ready() -> bool:

    return model is not None


# MODEL INFERENCE

def predict(
    frame,
    confidence: float = 0.25
):

    if model is None:

        raise RuntimeError(
            "YOLO model is not loaded"
        )

    results = model.predict(
        source=frame,
        conf=confidence,
        device="cpu",
        verbose=False
    )

    return results