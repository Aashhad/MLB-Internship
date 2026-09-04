from pathlib import Path

from ultralytics import YOLO


# ============================================================
# MODEL PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODEL_PATH = BASE_DIR / "models" / "best.pt"


# ============================================================
# LOAD MODEL ONCE
# ============================================================

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"YOLO model not found: {MODEL_PATH}"
    )


model = YOLO(str(MODEL_PATH))


# ============================================================
# DETECTION FUNCTION
# ============================================================

def detect_frame(frame, confidence: float = 0.25):
    """
    Run YOLO inference on a single frame.

    Args:
        frame: OpenCV BGR image
        confidence: YOLO confidence threshold

    Returns:
        YOLO Results object
    """

    results = model.predict(
        source=frame,
        conf=confidence,
        verbose=False
    )

    return results[0]



# from pathlib import Path

# from ultralytics import YOLO


# # ============================================================
# # BASE DIRECTORY
# # ============================================================

# BASE_DIR = Path(__file__).resolve().parent.parent.parent


# # ============================================================
# # YOLOv8n MODEL PATH
# # ============================================================

# MODEL_PATH = BASE_DIR / "models" / "yolov8n.pt"


# # ============================================================
# # CHECK MODEL
# # ============================================================

# if not MODEL_PATH.exists():

#     raise FileNotFoundError(
#         f"YOLOv8n model not found: {MODEL_PATH}"
#     )


# # ============================================================
# # LOAD YOLOv8n MODEL ONCE
# # ============================================================

# model = YOLO(str(MODEL_PATH))


# # ============================================================
# # DETECTION FUNCTION
# # ============================================================

# def detect_frame(
#     frame,
#     confidence: float = 0.25
# ):
#     """
#     Run YOLOv8n inference on a single video frame.

#     Args:
#         frame:
#             OpenCV BGR image.

#         confidence:
#             Minimum confidence threshold for detections.

#     Returns:
#         YOLO Results object.
#     """

#     results = model.predict(
#         source=frame,
#         conf=confidence,
#         verbose=False
#     )

#     return results[0]