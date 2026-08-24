from ultralytics import YOLO
from pathlib import Path
import cv2


# CONFIGURATION

MODEL_PATH = "Project 2/models/best.pt"

INPUT_DIR = Path("Project 2/images/testImages")
OUTPUT_DIR = Path("Project 2/predictions/images")

CONFIDENCE_THRESHOLD = 0.25
IMAGE_SIZE = 832

DEVICE = "cpu"


# CREATE OUTPUT DIRECTORY
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# LOAD MODEL
print("=" * 60)
print("LOADING MODEL")
print("=" * 60)

model = YOLO(MODEL_PATH)
print("Classes:", model.names)


# FIND TEST IMAGES
image_extensions = [
    "*.jpg",
    "*.jpeg",
    "*.png",
    "*.JPG",
    "*.JPEG",
    "*.PNG"
]

image_files = []

for extension in image_extensions:
    image_files.extend(INPUT_DIR.glob(extension))


if not image_files:
    print("No images found in:", INPUT_DIR)
    exit()


print(f"\nFound {len(image_files)} test images.")


# RUN INFERENCE

for image_path in image_files:

    print("\n" + "=" * 60)
    print("Processing:", image_path.name)
    print("=" * 60)

    results = model.predict(
        source=str(image_path),
        imgsz=IMAGE_SIZE,
        conf=CONFIDENCE_THRESHOLD,
        device=DEVICE,
        verbose=False
    )

    result = results[0]

    # Original image
    image = cv2.imread(str(image_path))

    # PROCESS DETECTIONS

    if result.boxes is not None:

        boxes = result.boxes

        for box in boxes:

            # Bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)

            # Confidence score
            confidence = float(box.conf[0].cpu().numpy())

            # Class ID
            class_id = int(box.cls[0].cpu().numpy())

            # Class name
            class_name = model.names[class_id]

            print(
                f"Detected: {class_name} "
                f"| Confidence: {confidence:.2%}"
            )

            # DRAW BOUNDING BOX

            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # CREATE LABEL

            label = f"{class_name} {confidence:.2f}"

            cv2.putText(
                image,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    else:

        print("No objects detected.")


    # SAVE RESULT

    output_path = OUTPUT_DIR / image_path.name

    cv2.imwrite(
        str(output_path),
        image
    )

    print("Saved:", output_path)

print("\n" + "=" * 60)
print("INFERENCE COMPLETED")
print("=" * 60)