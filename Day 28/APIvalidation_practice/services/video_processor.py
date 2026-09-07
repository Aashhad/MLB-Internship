import logging
import time

from pathlib import Path

import cv2

from APIvalidation_practice.services.detector import predict


logger = logging.getLogger(__name__)


# VIDEO PROCESSOR

def process_video(
    input_path: Path,
    output_path: Path,
    confidence: float,
    job_id: str
):

    start_time = time.perf_counter()

    logger.info(
        "Video processing started | "
        "job_id=%s | input=%s",
        job_id,
        input_path.name
    )

    # OPEN VIDEO

    cap = cv2.VideoCapture(
        str(input_path)
    )

    if not cap.isOpened():

        raise ValueError(
            "Unable to open video. "
            "The video may be corrupted or unsupported."
        )

    # VIDEO PROPERTIES

    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    width = int(
        cap.get(
            cv2.CAP_PROP_FRAME_WIDTH
        )
    )

    height = int(
        cap.get(
            cv2.CAP_PROP_FRAME_HEIGHT
        )
    )

    frame_count = int(
        cap.get(
            cv2.CAP_PROP_FRAME_COUNT
        )
    )

    if fps <= 0 or width <= 0 or height <= 0:

        cap.release()

        raise ValueError(
            "Invalid or corrupted video."
        )

    # OUTPUT DIRECTORY

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # VIDEO WRITER

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

        cap.release()

        raise RuntimeError(
            "Unable to create output video."
        )

    # PROCESS FRAMES

    processed_frames = 0

    try:

        while True:

            success, frame = cap.read()

            if not success:
                break

            results = predict(
                frame,
                confidence
            )

            annotated_frame = results[0].plot()

            writer.write(
                annotated_frame
            )

            processed_frames += 1

    except Exception:

        logger.exception(
            "Video inference failed | "
            "job_id=%s",
            job_id
        )

        raise

    finally:

        cap.release()
        writer.release()

    # VALIDATE PROCESSING

    if processed_frames == 0:

        raise ValueError(
            "Video contains no readable frames."
        )

    # PROCESSING TIME

    processing_time = (
        time.perf_counter() - start_time
    )

    logger.info(
        "Video processing completed | "
        "job_id=%s | frames=%s | "
        "duration=%.3fs",
        job_id,
        processed_frames,
        processing_time
    )

    return {
        "frames_processed": processed_frames,
        "processing_time": round(
            processing_time,
            3
        ),
        "fps": fps,
        "width": width,
        "height": height,
        "output": str(output_path)
    }