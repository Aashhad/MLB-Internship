import os
from ultralytics import YOLO

# Paths (always relative to this script's own location)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# Load model
model = YOLO("yolov8n.pt")


def print_detections(results):
    """Print class name, confidence, and bbox for each detected object."""
    for i, r in enumerate(results):
        print(f"\n--- Image {i}: {r.path} ---")

        boxes = r.boxes
        if boxes is None or len(boxes) == 0:
            print("No objects detected.")
            continue

        for box in boxes:
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]
            confidence = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            print(
                f"Object: {class_name:15s} | "
                f"Confidence: {confidence:.2f} | "
                f"BBox: ({x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f})"
            )


# Individual images — one inference call per image, each saved with its own correctly matching filename
image_names = ["dog.jpg", "street.jpg", "cat.jpg"]

individual_results = []

for name in image_names:
    image_path = os.path.join(IMAGES_DIR, name)
    result = model(image_path)[0]          # single Results object
    base_name = os.path.splitext(name)[0]  # "dog", "street", "cat"
    output_path = os.path.join(OUTPUTS_DIR, f"{base_name}_result.jpg")
    result.save(filename=output_path)
    print(f"Saved: {output_path}")
    individual_results.append(result)

print_detections(individual_results)