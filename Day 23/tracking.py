from ultralytics import YOLO
import cv2
from pathlib import Path
import time


# CONFIGURATION

MODEL_PATH = "yolov8n.pt"

INPUT_DIR = Path("Day 23/input")
OUTPUT_DIR = Path("Day 23/output")

CONFIDENCE_THRESHOLD = 0.25
IMAGE_SIZE = 640

# Use BoT-SORT for better tracking and ID consistency
TRACKER = "botsort.yaml"


# CREATE OUTPUT DIRECTORY

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# LOAD YOLO MODEL

print("=" * 60)
print("LOADING YOLOv8 MODEL")
print("=" * 60)

model = YOLO(MODEL_PATH)

print("Model loaded successfully!")
print()


# FIND VIDEOS

video_files = sorted(
    list(INPUT_DIR.glob("*.mp4")) +
    list(INPUT_DIR.glob("*.avi")) +
    list(INPUT_DIR.glob("*.mov")) +
    list(INPUT_DIR.glob("*.mkv"))
)

# CHECK NUMBER OF VIDEOS

print(f"Videos found: {len(video_files)}")

if len(video_files) < 5:
    print()
    print("WARNING!")
    print(f"Only {len(video_files)} videos found.")
    print("Your assignment requires at least 2-3 videos.")
    print()


# PROCESS EACH VIDEO

for video_number, video_path in enumerate(video_files, start=1):

    print("=" * 60)
    print(f"PROCESSING VIDEO {video_number}")
    print(f"File: {video_path.name}")
    print("=" * 60)

    # OPEN VIDEO

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        print(f"ERROR: Could not open {video_path}")
        continue


    # GET VIDEO PROPERTIES

    fps = cap.get(cv2.CAP_PROP_FPS)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Resolution: {width} x {height}")
    print(f"FPS: {fps:.2f}")
    print(f"Total Frames: {total_frames}")
    print()


    # OUTPUT PATH

    output_path = OUTPUT_DIR / f"{video_path.stem}_tracked.mp4"


    # VIDEO WRITER

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        str(output_path),
        fourcc,
        fps,
        (width, height)
    )


    # UNIQUE TRACKING IDs

    unique_ids = set()

    # Store class name for every ID
    tracked_objects = {}
    frame_number = 0
    start_time = time.time()


    # PROCESS VIDEO FRAME BY FRAME

    while True:

        ret, frame = cap.read()
        if not ret:
            break
        frame_number += 1


        # YOLO TRACKING

        results = model.track(
            frame,
            persist=True,
            tracker=TRACKER,
            conf=CONFIDENCE_THRESHOLD,
            imgsz=IMAGE_SIZE,
            verbose=False
        )


        result = results[0]


        # CHECK TRACKING RESULTS

        if (
            result.boxes is not None
            and result.boxes.id is not None
        ):

            boxes = result.boxes.xyxy.cpu().numpy()

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


            # PROCESS EACH OBJECT

            for box, track_id, class_id, confidence in zip(
                boxes,
                track_ids,
                classes,
                confidences
            ):

                # Add ID to unique IDs
                unique_ids.add(track_id)

                # Get class name
                class_name = model.names[class_id]

                # Store object class
                tracked_objects[track_id] = class_name

                # Bounding box
                x1, y1, x2, y2 = map(int, box)


                # DRAW BOUNDING BOX

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    3
                )


                # CREATE LABEL

                label = (
                    f"ID: {track_id} | "
                    f"{class_name} | "
                    f"{confidence:.2f}"
                )


                # Get text size
                (
                    text_width,
                    text_height
                ), baseline = cv2.getTextSize(
                    label,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    2
                )


                # TEXT BACKGROUND

                cv2.rectangle(
                    frame,
                    (x1, y1 - text_height - 10),
                    (x1 + text_width + 5, y1),
                    (0, 255, 0),
                    -1
                )


                # DRAW LABEL

                cv2.putText(
                    frame,
                    label,
                    (x1 + 2, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 0),
                    2
                )


        # DISPLAY STATISTICS ON VIDEO

        unique_count = len(unique_ids)


        # Statistics background
        cv2.rectangle(
            frame,
            (10, 10),
            (430, 105),
            (0, 0, 0),
            -1
        )


        # Unique objects
        cv2.putText(
            frame,
            f"Unique Objects: {unique_count}",
            (20, 42),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )


        # Frame number
        cv2.putText(
            frame,
            f"Frame: {frame_number}/{total_frames}",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )


        # SAVE PROCESSED FRAME
        writer.write(frame)


        # TERMINAL PROGRESS

        if frame_number % 30 == 0:

            progress = (frame_number / total_frames) * 100
            print(f"\rProgress: {progress:.1f}%", end="")


    # RELEASE RESOURCES

    cap.release()
    writer.release()
    print()


    # PROCESSING TIME

    elapsed_time = time.time() - start_time


    # RESULTS

    print()
    print("-" * 60)
    print("TRACKING COMPLETED")
    print("-" * 60)

    print(f"Video: {video_path.name}")
    print(f"Frames Processed: {frame_number}")
    print(f"Unique Objects: {len(unique_ids)}")
    print(f"Processing Time: {elapsed_time:.2f} seconds")
    print(f"Output: {output_path}")

    print()
    print("Tracked Objects:")

    for track_id, class_name in sorted(
        tracked_objects.items()
    ):

        print(f"  ID {track_id} → {class_name}")
    print()


# ALL VIDEOS COMPLETE

print("=" * 60)
print("ALL VIDEOS PROCESSED")
print("=" * 60)

print(f"Output folder: {OUTPUT_DIR}")