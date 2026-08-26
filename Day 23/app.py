import gradio as gr
from ultralytics import YOLO

import cv2
from pathlib import Path

import tempfile
import time
import subprocess

import imageio_ffmpeg


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "yolov8n.pt"
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
CUSTOM_TRACKER_PATH = BASE_DIR / "botsort_custom.yaml"


# YOLO SETTINGS

CONFIDENCE_THRESHOLD = 0.25
IMAGE_SIZE = 640
DEVICE = "cpu"


# CREATE DIRECTORIES

INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# CHECK MODEL

if not MODEL_PATH.exists():

    print()
    print("=" * 60)
    print("ERROR: YOLO MODEL NOT FOUND")
    print("=" * 60)
    print(f"Expected model location:\n{MODEL_PATH}")
    print()
    print("Please put yolov8n.pt inside the Day 23 folder.")

    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")


# LOAD YOLO MODEL

print("=" * 60)
print("LOADING YOLOv8 MODEL")
print("=" * 60)
print(f"Model path: {MODEL_PATH}"
)

model = YOLO(str(MODEL_PATH))
print("YOLOv8 model loaded successfully!")
print(f"Classes: {model.names}")
print()


# FIND SAMPLE VIDEOS

def get_sample_videos():

    extensions = [
        "*.mp4",
        "*.avi",
        "*.mov",
        "*.mkv",
        "*.webm"
    ]

    videos = []

    for extension in extensions:

        videos.extend(INPUT_DIR.glob(extension))

    return sorted(videos)



# GET VIDEO PATH FROM GRADIO

def get_video_path(video_input):

    """
    Gradio versions can return different values.

    This function safely extracts the actual video path.
    """

    print()
    print("-" * 60)
    print("GRADIO INPUT INFORMATION")
    print("-" * 60)

    print("Received:",video_input)
    print("Type:", type(video_input))

    # Nothing selected

    if video_input is None:
        return None


    # Already a string/path

    if isinstance(video_input, (str, Path)):

        return Path(str(video_input))


    # Dictionary returned by some Gradio versions

    if isinstance(video_input, dict):

        possible_keys = [
            "path",
            "video",
            "name"
        ]

        for key in possible_keys:

            value = video_input.get(key)

            if value:

                return Path(str(value))


    # Tuple/list

    if isinstance(video_input, (list, tuple)):

        if len(video_input) > 0:
            first_value = video_input[0]
            if first_value:
                return Path(str(first_value))


    # Unsupported format

    raise gr.Error(
        "Unsupported video input format. "
        "Please upload the video again."
    )


# CONVERT VIDEO TO H.264

def convert_to_h264(
    input_video,
    output_video
):

    print()
    print("Converting video to H.264...")

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

        print("FFmpeg conversion failed.")
        print(result.stderr)
        raise RuntimeError("Could not convert video to H.264.")
    print("H.264 conversion completed.")

    return output_video


# GET TRACKER

def get_tracker():

    """
    Use custom BoT-SORT configuration if available.

    Otherwise use Ultralytics built-in botsort.yaml.
    """

    if CUSTOM_TRACKER_PATH.exists():

        print(f"Using custom tracker: " f"{CUSTOM_TRACKER_PATH}")
        return str(CUSTOM_TRACKER_PATH)
    print("Custom tracker not found.")
    print("Using default Ultralytics BoT-SORT.")

    return "botsort.yaml"


# TRACK VIDEO

def track_video(video_input):

    print()
    print("=" * 60)
    print("STARTING VIDEO TRACKING")
    print("=" * 60)

    # GET VIDEO PATH

    video_path = get_video_path(video_input)

    if video_path is None:

        raise gr.Error("Please upload a video first.")
    print(f"Video path: {video_path}")


    # CHECK VIDEO EXISTS

    if not video_path.exists():

        raise gr.Error(
            f"Video file does not exist:\n"
            f"{video_path}"
        )

    print("Video file exists.")


    # OPEN VIDEO

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():

        raise gr.Error(
            "OpenCV could not open this video. "
            "Try converting it to MP4."
        )

    print("Video opened successfully.")


    # VIDEO INFORMATION

    fps = cap.get(cv2.CAP_PROP_FPS)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


    # Fix invalid FPS

    if fps <= 0:
        fps = 30.0


    # Validate dimensions

    if width <= 0 or height <= 0:

        cap.release()

        raise gr.Error("Could not read the video dimensions.")

    print()
    print(f"FPS: {fps:.2f}")
    print(f"Resolution: {width} x {height}")
    print(f"Total frames: {total_frames}")


    # CREATE TEMPORARY OUTPUT

    temp_dir = Path(tempfile.mkdtemp(prefix="yolo_tracking_"))

    temp_video = (temp_dir / "tracking_temp.mp4")


    # CREATE FINAL OUTPUT

    timestamp = int(time.time())

    final_video = (OUTPUT_DIR / f"tracked_{timestamp}.mp4")


    # VIDEO WRITER

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        str(temp_video),
        fourcc,
        fps,
        (width, height)
    )


    if not writer.isOpened():
        cap.release()
        raise gr.Error("Could not create the output video.")


    print(f"Temporary output: {temp_video}")


    # TRACKING VARIABLES

    unique_ids = set()
    tracked_classes = {}
    frame_count = 0
    start_time = time.time()


    # GET TRACKER

    tracker = get_tracker()


    # PROCESS VIDEO

    try:
        while True:
            ret, frame = cap.read()

            # End of video

            if not ret:
                break

            frame_count += 1


            # YOLO TRACKING

            try:
                results = model.track(
                    frame,
                    persist=True,
                    tracker=tracker,
                    conf=CONFIDENCE_THRESHOLD,
                    imgsz=IMAGE_SIZE,
                    device=DEVICE,
                    verbose=False
                )

            except Exception as error:

                print()
                print("YOLO TRACKING ERROR:")
                print(error)

                raise gr.Error(f"YOLO tracking failed:\n{error}")


            # Get first result

            if not results:

                writer.write(frame)

                continue

            result = results[0]


            # PROCESS DETECTIONS

            if (
                result.boxes is not None
                and len(result.boxes) > 0
            ):

                boxes = (
                    result.boxes
                    .xyxy
                    .cpu()
                    .numpy()
                )


                classes = (
                    result.boxes
                    .cls
                    .int()
                    .cpu()
                    .tolist()
                )


                confidences = (
                    result.boxes
                    .conf
                    .cpu()
                    .numpy()
                )


                # Tracking IDs

                if result.boxes.id is not None:

                    track_ids = (
                        result.boxes
                        .id
                        .int()
                        .cpu()
                        .tolist()
                    )

                else:

                    # No tracking ID available
                    track_ids = [
                        None
                    ] * len(boxes)


                # DRAW DETECTIONS

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

                    # Bounding box

                    x1, y1, x2, y2 = map(
                        int,
                        box
                    )


                    # Class name

                    class_name = model.names[
                        int(class_id)
                    ]


                    # Track ID

                    if track_id is not None:

                        track_id = int(track_id)

                        unique_ids.add(track_id)

                        tracked_classes[track_id] = class_name

                        label = (
                            f"ID: {track_id} | "
                            f"{class_name} | "
                            f"{confidence:.2f}"
                        )

                    else:

                        label = (
                            f"{class_name} | "
                            f"{confidence:.2f}"
                        )


                    # Draw bounding box

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )


                    # Calculate text size

                    (text_width,text_height), baseline = cv2.getTextSize(
                        label,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        2
                    )


                    # Label background

                    label_y1 = max(
                        0,
                        y1 -
                        text_height -
                        baseline -
                        8
                    )


                    cv2.rectangle(

                        frame,
                        (x1, label_y1),
                        (x1 + text_width + 8, y1),
                        (0, 255, 0),
                        -1
                    )


                    # Draw label

                    cv2.putText(
                        frame,
                        label,
                        (x1 + 4, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 0, 0),
                        2
                    )


            # DISPLAY STATISTICS

            unique_count = len(unique_ids)


            # Statistics background

            cv2.rectangle(
                frame,
                (10, 10),
                (430, 115),
                (0, 0, 0),
                -1
            )


            # Unique objects

            cv2.putText(
                frame,
                f"Unique Objects: {unique_count}",
                (20, 42),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 255, 255),
                2
            )


            # Frame

            cv2.putText(
                frame,
                f"Frame: {frame_count}/{total_frames}",
                (20, 73),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.60,
                (255, 255, 255),
                2
            )


            # Progress

            if total_frames > 0:

                progress = (
                    frame_count /
                    total_frames
                ) * 100

            else:

                progress = 0

            cv2.putText(
                frame,
                f"Progress: {progress:.1f}%",
                (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.60,
                (255, 255, 255),
                2
            )


            # Write frame

            writer.write(frame)


            # Terminal progress

            if (
                frame_count % 100 == 0
            ):

                if total_frames > 0:

                    percentage = (
                        frame_count /
                        total_frames
                    ) * 100

                else:

                    percentage = 0


                print(
                    f"Processing: "
                    f"{frame_count}/{total_frames} "
                    f"({percentage:.1f}%)"
                )


    finally:

        cap.release()
        writer.release()


    # PROCESSING TIME

    processing_time = (time.time() - start_time)


    print()
    print("Video processing completed.")

    print(f"Frames processed: {frame_count}")
    print(f"Unique objects: {len(unique_ids)}")
    print(f"Processing time: " f"{processing_time:.2f} seconds")


    # CONVERT OUTPUT VIDEO

    try:

        convert_to_h264(temp_video, final_video)

    except Exception as error:

        print()
        print("WARNING: H.264 conversion failed.")
        print(error)
        print("Using OpenCV output instead.")

        final_video = temp_video


    # CHECK FINAL FILE

    if not Path(
        final_video
    ).exists():

        raise gr.Error("The processed video was not created.")


    print(f"Final video: {final_video}")


    print(f"Final video size: " f"{Path(final_video).stat().st_size / (1024 * 1024):.2f} MB")


    # 
    # CREATE OBJECT SUMMARY

    if tracked_classes:

        object_lines = []


        for track_id in sorted(
            tracked_classes.keys()
        ):

            class_name = tracked_classes[track_id]

            object_lines.append(
                f"- **ID {track_id}** → "
                f"{class_name}"
            )


        object_summary = "\n".join(object_lines)

    else:

        object_summary = (
            "No tracking IDs were generated."
        )


    # RESULT SUMMARY

    summary = f"""
## ✅ Tracking Completed

### Video Information

**Input Video:** `{video_path.name}`

**Frames Processed:** `{frame_count}`

**Processing Time:** `{processing_time:.2f} seconds`

### Tracking Results

**Unique Objects:** `{len(unique_ids)}`

### Tracked Objects

{object_summary}

### Output

`{Path(final_video).name}`
"""


    print()
    print("=" * 60)
    print("TRACKING FINISHED SUCCESSFULLY")
    print("=" * 60)
    print(f"Output: {final_video}")
    print()


    # RETURN RESULTS TO GRADIO

    return (
        str(final_video),
        int(len(unique_ids)),
        summary
    )


# SAMPLE VIDEOS

sample_videos = get_sample_videos()

sample_paths = [
    [str(video)]
    for video in sample_videos
]


# GRADIO UI

with gr.Blocks(
    title="Smart Object Tracking System"
) as demo:


    # HEADER

    gr.Markdown(
        """
# 🎯 Smart Object Tracking System

Upload a video or select one of the sample videos.

The application uses **YOLOv8 + BoT-SORT** to:

- Detect objects
- Track objects across frames
- Assign unique tracking IDs
- Display confidence scores
- Count unique objects
- Save the processed video

# Developed By : Ashhad
"""
    )


    # INPUT SECTION

    with gr.Row():


        # VIDEO INPUT

        with gr.Column(scale=1):
            video_input = gr.Video(label="Upload Video", sources=["upload"])


        # SAMPLE VIDEOS

        with gr.Column(scale=1):

            gr.Markdown(
                """
### 📁 Sample Videos

"""
            )


            if sample_paths:
                gr.Examples(
                    examples=sample_paths,
                    inputs=video_input,
                    label="Select a Sample Video"
                )

            else:
                gr.Markdown(
                    """
⚠️ **No sample videos found.**

Add `.mp4`, `.avi`, `.mov`, `.mkv`
or `.webm` files to:

`Day 23/input/`
"""
                )


    # PROCESS BUTTON

    process_button = gr.Button(
        "🚀 Start Tracking",
        variant="primary"
    )


    # OUTPUT SECTION

    gr.Markdown("## 📊 Tracking Results")


    with gr.Row():


        # PROCESSED VIDEO

        output_video = gr.Video(
            label="Processed Tracking Video",
            autoplay=False
        )


        # UNIQUE COUNT

        unique_count = gr.Number(
            label="Total Unique Objects",
            precision=0
        )


    # TRACKING SUMMARY

    tracking_summary = gr.Markdown()


    # BUTTON EVENT

    process_button.click(

        fn=track_video,

        inputs=video_input,

        outputs=[
            output_video,
            unique_count,
            tracking_summary
        ]
    )


    # FOOTER

    gr.Markdown(
        """
---

### ⚙️ Configuration

**Model:** YOLOv8 Nano (`yolov8n.pt`)  
**Tracker:** BoT-SORT  
**Device:** CPU  

    """
    )

    print()
print("=" * 60)
print("STARTING SMART OBJECT TRACKING SYSTEM")
print("=" * 60)
print(f"Sample videos found: " f"{len(sample_videos)}")

for video in sample_videos:
    print(f"  - {video.name}")


print()
demo.launch()