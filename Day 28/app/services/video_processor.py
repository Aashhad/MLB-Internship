import logging
import time
from pathlib import Path

import cv2

from app.services.detector import detector


logger = logging.getLogger(__name__)


def process_video(
    input_path: Path,
    output_path: Path,
    confidence: float,
    job_id: str,
    request_id: str
):

    start_time = time.perf_counter()

    logger.info(
        "Job started | job_id=%s | request_id=%s",
        job_id,
        request_id
    )

    capture = cv2.VideoCapture(str(input_path))

    if not capture.isOpened():

        logger.error(
            "Video could not be opened | "
            "job_id=%s | request_id=%s",
            job_id,
            request_id
        )

        raise RuntimeError(
            "Unable to open video"
        )

    fps = capture.get(cv2.CAP_PROP_FPS)

    width = int(
        capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    )

    height = int(
        capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )

    total_frames = int(
        capture.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    # Safety fallback
    if fps <= 0:
        fps = 25.0

    fourcc = cv2.VideoWriter_fourcc(
        *"mp4v"
    )

    writer = cv2.VideoWriter(
        str(output_path),
        fourcc,
        fps,
        (width, height)
    )

    if not writer.isOpened():

        capture.release()

        logger.error(
            "Video writer could not be created | "
            "job_id=%s | request_id=%s",
            job_id,
            request_id
        )

        raise RuntimeError(
            "Unable to create output video"
        )

    processed_frames = 0

    try:

        while True:

            success, frame = capture.read()

            if not success:
                break

            # ================================================
            # YOLO INFERENCE
            # ================================================

            results = detector.predict(
                frame,
                confidence
            )

            # ================================================
            # DRAW DETECTIONS
            # ================================================

            annotated_frame = results[0].plot()

            writer.write(
                annotated_frame
            )

            processed_frames += 1

        processing_time = (
            time.perf_counter() - start_time
        )

        logger.info(
            "Processing completed | "
            "job_id=%s | request_id=%s | "
            "frames=%s/%s | duration=%.3fs",
            job_id,
            request_id,
            processed_frames,
            total_frames,
            processing_time
        )

        return {
            "frames_processed": processed_frames,
            "total_frames": total_frames,
            "duration_seconds": round(
                processing_time,
                3
            )
        }

    except Exception:

        logger.exception(
            "Video processing failed | "
            "job_id=%s | request_id=%s",
            job_id,
            request_id
        )

        raise

    finally:

        capture.release()
        writer.release()