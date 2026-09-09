import time
import subprocess
import tempfile

from pathlib import Path

import cv2

from ultralytics import YOLO

import imageio_ffmpeg


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "model" / "yolov8n.pt"

TRACKER_PATH = BASE_DIR / "botsort_custom.yaml"

OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# YOLO CONFIGURATION
# ============================================================

CONFIDENCE_THRESHOLD = 0.25

IMAGE_SIZE = 640

DEVICE = "cpu"


# ============================================================
# LOAD MODEL
# ============================================================

print("=" * 60)
print("LOADING YOLO MODEL")
print("=" * 60)

model = YOLO(
    str(MODEL_PATH)
)

print("YOLO model loaded successfully!")


# ============================================================
# H264 CONVERSION
# ============================================================

def convert_to_h264(
    input_video,
    output_video
):

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    command = [
        ffmpeg,
        "-y",
        "-i",
        str(input_video),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(output_video)
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:

        raise RuntimeError(
            "Could not convert video to H.264."
        )

    return output_video


# ============================================================
# PROCESS VIDEO
# ============================================================

def process_video(
    input_video: Path,
    output_video: Path
):

    if not input_video.exists():

        raise FileNotFoundError(
            "Input video not found."
        )


    # --------------------------------------------------------
    # Open video
    # --------------------------------------------------------

    cap = cv2.VideoCapture(
        str(input_video)
    )


    if not cap.isOpened():

        raise RuntimeError(
            "Could not open input video."
        )


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

    total_frames = int(
        cap.get(
            cv2.CAP_PROP_FRAME_COUNT
        )
    )


    if fps <= 0:

        fps = 30


    # --------------------------------------------------------
    # Temporary output
    # --------------------------------------------------------

    temp_dir = Path(
        tempfile.mkdtemp()
    )

    temp_video = (
        temp_dir / "tracking_temp.mp4"
    )


    fourcc = cv2.VideoWriter_fourcc(
        *"mp4v"
    )


    writer = cv2.VideoWriter(
        str(temp_video),
        fourcc,
        fps,
        (width, height)
    )


    if not writer.isOpened():

        cap.release()

        raise RuntimeError(
            "Could not create output video."
        )


    # --------------------------------------------------------
    # Tracking variables
    # --------------------------------------------------------

    unique_ids = set()

    tracked_classes = {}

    frame_count = 0

    start_time = time.time()


    # ========================================================
    # PROCESS FRAMES
    # ========================================================

    while True:

        ret, frame = cap.read()


        if not ret:

            break


        frame_count += 1


        # ----------------------------------------------------
        # YOLO TRACKING
        # ----------------------------------------------------

        results = model.track(

            frame,

            persist=True,

            tracker=str(
                TRACKER_PATH
            ),

            conf=CONFIDENCE_THRESHOLD,

            imgsz=IMAGE_SIZE,

            device=DEVICE,

            verbose=False
        )


        result = results[0]


        # ----------------------------------------------------
        # DETECTIONS
        # ----------------------------------------------------

        if (
            result.boxes is not None
            and result.boxes.id is not None
        ):

            boxes = (
                result.boxes.xyxy
                .cpu()
                .numpy()
            )

            track_ids = (
                result.boxes.id
                .int()
                .cpu()
                .tolist()
            )

            classes = (
                result.boxes.cls
                .int()
                .cpu()
                .tolist()
            )

            confidences = (
                result.boxes.conf
                .cpu()
                .numpy()
            )


            for (
                box,
                track_id,
                class_id,
                confidence
            ) in zip(
                boxes,
                track_ids,
                classes,
                confidences
            ):

                track_id = int(
                    track_id
                )

                class_id = int(
                    class_id
                )


                unique_ids.add(
                    track_id
                )


                class_name = model.names[
                    class_id
                ]


                tracked_classes[
                    track_id
                ] = class_name


                x1, y1, x2, y2 = map(
                    int,
                    box
                )


                # ------------------------------------------------
                # Bounding box
                # ------------------------------------------------

                cv2.rectangle(

                    frame,

                    (x1, y1),

                    (x2, y2),

                    (0, 255, 0),

                    2
                )


                # ------------------------------------------------
                # Label
                # ------------------------------------------------

                label = (
                    f"ID: {track_id} | "
                    f"{class_name} | "
                    f"{confidence:.2f}"
                )


                cv2.putText(

                    frame,

                    label,

                    (x1, max(30, y1 - 10)),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.6,

                    (0, 255, 0),

                    2
                )


        # ----------------------------------------------------
        # Statistics
        # ----------------------------------------------------

        unique_count = len(
            unique_ids
        )


        cv2.putText(

            frame,

            f"Unique Objects: {unique_count}",

            (20, 40),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (255, 255, 255),

            2
        )


        cv2.putText(

            frame,

            f"Frame: {frame_count}/{total_frames}",

            (20, 70),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.6,

            (255, 255, 255),

            2
        )


        writer.write(frame)


    # ========================================================
    # RELEASE
    # ========================================================

    cap.release()

    writer.release()


    # ========================================================
    # CONVERT TO H264
    # ========================================================

    try:

        convert_to_h264(
            temp_video,
            output_video
        )

    except Exception:

        # Fallback
        import shutil

        shutil.copy2(
            temp_video,
            output_video
        )


    # ========================================================
    # PROCESSING TIME
    # ========================================================

    processing_time = (
        time.time()
        - start_time
    )


    # ========================================================
    # RETURN INFORMATION
    # ========================================================

    return {

        "unique_objects": len(
            unique_ids
        ),

        "frames_processed": frame_count,

        "processing_time": processing_time,

        "tracked_classes": tracked_classes
    }