import logging
import time
from pathlib import Path

import cv2

from ultralytics import YOLO


logger = logging.getLogger(__name__)


# PATHS

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODEL_PATH = BASE_DIR / "models" / "yolov8n.pt"

OUTPUT_DIR = BASE_DIR / "videos" / "output"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# LOAD MODEL

model = YOLO(str(MODEL_PATH))


# VIDEO PROCESSING

def process_video(
    input_path: Path,
    output_path: Path
):

    start_time = time.time()

    logger.info(
        "Starting video processing | input=%s",
        input_path
    )

    cap = cv2.VideoCapture(str(input_path))

    if not cap.isOpened():

        raise RuntimeError(
            "Unable to open video file"
        )

    fps = cap.get(cv2.CAP_PROP_FPS)

    width = int(
        cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    )

    height = int(
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )

    # Safety fallback
    if fps <= 0:
        fps = 30

    fourcc = cv2.VideoWriter_fourcc(
        *"mp4v"
    )

    writer = cv2.VideoWriter(
        str(output_path),
        fourcc,
        fps,
        (width, height)
    )

    total_detections = 0

    frame_count = 0

    try:

        while True:

            success, frame = cap.read()

            if not success:
                break

            frame_count += 1

            # YOLOv8n INFERENCE

            results = model(
                frame,
                conf=0.25,
                verbose=False
            )

            result = results[0]

            # Count detected objects
            if result.boxes is not None:

                detection_count = len(
                    result.boxes
                )

                total_detections += detection_count

            # DRAW YOLO RESULTS

            annotated_frame = result.plot()

            writer.write(
                annotated_frame
            )

    finally:

        cap.release()
        writer.release()

    processing_time = (
        time.time() - start_time
    )

    logger.info(
        "Video processing completed | "
        "frames=%s | detections=%s | "
        "processing_time=%.2f seconds",
        frame_count,
        total_detections,
        processing_time
    )

    return {
        "processing_time": processing_time,
        "total_detections": total_detections
    }