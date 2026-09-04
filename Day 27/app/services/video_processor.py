from pathlib import Path
from time import perf_counter
import cv2

from app.services.detector import detect_frame


# ============================================================
# PROCESS VIDEO
# ============================================================

def process_video(
    input_path: Path,
    output_path: Path,
    confidence: float = 0.25,
    status_store=None,
    job_id: str | None = None
):
    """
    Process a video frame by frame using YOLO.

    Args:
        input_path: Input video path
        output_path: Output video path
        confidence: YOLO confidence threshold
        status_store: Shared dictionary for job status
        job_id: Current job ID

    Returns:
        Dictionary containing processing statistics.
    """

    start_time = perf_counter()

    # --------------------------------------------------------
    # OPEN VIDEO
    # --------------------------------------------------------

    cap = cv2.VideoCapture(str(input_path))

    if not cap.isOpened():
        raise ValueError(
            "Unable to open video. The video may be corrupted "
            "or the format may be unsupported."
        )

    # --------------------------------------------------------
    # VIDEO PROPERTIES
    # --------------------------------------------------------

    total_frames = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    width = int(
        cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    )

    height = int(
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )

    # --------------------------------------------------------
    # VALIDATE VIDEO
    # --------------------------------------------------------

    if total_frames <= 0:
        cap.release()

        raise ValueError(
            "Video contains no frames or is corrupted."
        )

    if width <= 0 or height <= 0:
        cap.release()

        raise ValueError(
            "Invalid video dimensions."
        )

    if fps <= 0:
        fps = 25.0

    # --------------------------------------------------------
    # OUTPUT DIRECTORY
    # --------------------------------------------------------

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # VIDEO WRITER
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    processed_frames = 0
    total_detections = 0

    # --------------------------------------------------------
    # FRAME LOOP
    # --------------------------------------------------------

    try:

        while True:

            success, frame = cap.read()

            if not success:
                break

            processed_frames += 1

            # ------------------------------------------------
            # YOLO DETECTION
            # ------------------------------------------------

            result = detect_frame(
                frame,
                confidence=confidence
            )

            # ------------------------------------------------
            # COUNT DETECTIONS
            # ------------------------------------------------

            if result.boxes is not None:

                total_detections += len(
                    result.boxes
                )

            # ------------------------------------------------
            # DRAW YOLO RESULTS
            # ------------------------------------------------

            annotated_frame = result.plot()

            # ------------------------------------------------
            # FRAME INFORMATION
            # ------------------------------------------------

            progress = int(
                (processed_frames / total_frames) * 100
            )

            frame_text = (
                f"Frame: {processed_frames}/{total_frames}"
            )

            progress_text = (
                f"Progress: {progress}%"
            )

            cv2.putText(
                annotated_frame,
                frame_text,
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.putText(
                annotated_frame,
                progress_text,
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            # ------------------------------------------------
            # WRITE FRAME
            # ------------------------------------------------

            writer.write(
                annotated_frame
            )

            # ------------------------------------------------
            # UPDATE STATUS
            # ------------------------------------------------

            if status_store is not None and job_id:

                status_store[job_id]["progress"] = progress

                status_store[job_id][
                    "processed_frames"
                ] = processed_frames

                status_store[job_id][
                    "total_detections"
                ] = total_detections

    finally:

        cap.release()
        writer.release()

    # --------------------------------------------------------
    # PROCESSING TIME
    # --------------------------------------------------------

    processing_time = (
        perf_counter() - start_time
    )

    # --------------------------------------------------------
    # AVERAGE FPS
    # --------------------------------------------------------

    if processing_time > 0:

        average_fps = (
            processed_frames /
            processing_time
        )

    else:

        average_fps = 0.0

    # --------------------------------------------------------
    # FINAL VALIDATION
    # --------------------------------------------------------

    if processed_frames == 0:

        raise ValueError(
            "No frames could be processed."
        )

    if not output_path.exists():

        raise RuntimeError(
            "Processed video was not created."
        )

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    statistics = {
        "total_frames": total_frames,
        "processed_frames": processed_frames,
        "total_detections": total_detections,
        "average_fps": round(
            average_fps,
            2
        ),
        "processing_time_seconds": round(
            processing_time,
            2
        ),
        "video_fps": round(
            fps,
            2
        ),
        "resolution": f"{width}x{height}"
    }

    return statistics