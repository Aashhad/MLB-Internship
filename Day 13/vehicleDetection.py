
# This script:
# 1. Loads a pretrained YOLOv8 model
# 2. Detects vehicles in sample_images
# 3. Saves annotated images to outputs
# 4. Creates a grid preview
# 5. Prints detection information
# 6. Provides a brief prediction analysis

import os
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO

#PROJECT PATHS
#Get the folder where this Python script is located
BASE_DIR = Path(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
#Input folder
SOURCE_DIR = BASE_DIR / "sample_images"
#Output folder
OUTPUT_DIR = BASE_DIR / "outputs"
#Create output folder if it does not exist
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)

#MODEL SETTINGS
MODEL_NAME = "yolov8n.pt"
# Confidence threshold
CONFIDENCE_THRESHOLD = 0.25

#VEHICLE CLASSES
#YOLOv8 COCO class IDs
VEHICLE_CLASSES = {
    1: "bicycle",
    2: "car",
    3: "motorcycle",
    5: "bus",
    6: "train",
    7: "truck",
}


#LOAD YOLO MODEL
print("OBJECT DETECTION - VEHICLE DETECTION USING YOLO")
print( f"\nProject directory: {BASE_DIR}")
print(f"Input directory: {SOURCE_DIR}")
print(f"Output directory: {OUTPUT_DIR}")

# Load pretrained YOLO model
print("\nLoading YOLO model...")
model = YOLO(MODEL_NAME)
print(f"Model loaded successfully: "f"{MODEL_NAME}")

#FIND IMAGES
# Supported image extensions
IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


# Check if sample_images folder exists
if not SOURCE_DIR.exists():
    print(f"\nERROR: Image folder not found!")
    print(f"Expected folder:")
    print(SOURCE_DIR)
    print("\nMake sure your folder structure is:")
    print("Day 13/")
    print("├── sample_images/")
    print("│   ├── bus.jpg")
    print("│   ├── car.jpg")
    print("│   ├── cycle.jpg")
    print("│   ├── motorcycle.jpg")
    print("│   ├── train.jpg")
    print("│   └── truck.jpg")
    print("└── objectDetectionYOLO.py")
    exit()

# Find all images
image_paths = sorted(
    [
        path
        for path in SOURCE_DIR.iterdir()
        if path.suffix.lower()
        in IMAGE_EXTENSIONS
    ]
)


# Check if images were found
if not image_paths:
    print(f"\nNo images found in:")
    print(SOURCE_DIR)
    print("Please add .jpg, .jpeg, .png, .bmp, or .webp files.")
    exit()


print(f"\nFound {len(image_paths)} image(s):")

for image_path in image_paths:
    print(f"  - {image_path.name}")


#RUN YOLO INFERENCE
print("\n" + "=" * 60)
print("RUNNING YOLO OBJECT DETECTION")
all_results_summary = []


# Process each image
for image_path in image_paths:

    # Run YOLO prediction
    results = model.predict(
        source=str(image_path),
        conf=CONFIDENCE_THRESHOLD,
        verbose=False
    )

    # Get first result
    result = results[0]


    
    # SAVE ANNOTATED IMAGE
    # YOLO automatically draws:
    # - Bounding boxes
    # - Class names
    # - Confidence scores

    annotated_image = result.plot()
    # Output filename
    output_path = (OUTPUT_DIR/ f"detected_{image_path.name}")

    # Save annotated image
    cv2.imwrite(str(output_path),annotated_image)


    # COLLECT DETECTION INFORMATION

    detections = []

    # Check detected boxes
    if (
        result.boxes is not None and len(result.boxes) > 0
    ):

        for box in result.boxes:
            # Class ID
            class_id = int(box.cls[0])
            # Class name
            class_name = model.names[class_id]
            # Confidence
            confidence = float(box.conf[0])
            # Bounding box
            x1, y1, x2, y2 = (box.xyxy[0].tolist())
            # Store detection
            detections.append(
                {
                    "class_id": class_id,
                    "class_name": class_name,
                    "confidence": confidence,
                    "bbox": (
                        x1,
                        y1,
                        x2,
                        y2
                    )
                }
            )


    # Store summary
    all_results_summary.append(
        {
            "image": image_path.name,
            "num_detections": len(
                detections
            ),
            "detections": detections
        }
    )


    # PRINT IMAGE RESULTS
    print(f"\nImage: {image_path.name}")
    print(f"Objects detected: "f"{len(detections)}")
    print(f"Saved to: "f"{output_path}")


    # Print every detected object
    if detections:
        for detection in detections:
            print(f"  Object: "f"{detection['class_name']}")
            print(f"  Confidence: "f"{detection['confidence']:.2%}")
            x1, y1, x2, y2 = (detection["bbox"])
            print(
                f"  Bounding Box: "
                f"({x1:.0f}, "
                f"{y1:.0f}, "
                f"{x2:.0f}, "
                f"{y2:.0f})"
            )
    else:
        print("No objects detected.")



#CREATE VISUALIZATION GRID
print("CREATING VISUALIZATION GRID")


# Get saved prediction images
output_images = sorted(
    [
        path
        for path in OUTPUT_DIR.iterdir()
        if path.name.startswith(
            "detected_"
        )
        and path.suffix.lower()
        in IMAGE_EXTENSIONS
    ]
)


if output_images:

    # Maximum images to show
    max_images = min(
        len(output_images),
        6
    )

    # Number of columns
    columns = 3
    # Calculate rows
    rows = (max_images + columns- 1) // columns
    # Create figure
    plt.figure(figsize=(15,5 * rows))
    # Display images
    for i in range(max_images):
        image_path = (output_images[i])
        # Read image
        image = cv2.imread(str(image_path))
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        # Create subplot
        plt.subplot(rows,columns,i + 1)
        # Display image
        plt.imshow(image_rgb)
        # Add title
        plt.title(image_path.name)
        # Hide axes
        plt.axis("off")
    # Adjust layout
    plt.tight_layout()
    # Grid output path
    grid_path = (OUTPUT_DIR / "_grid_preview.png")
    # Save grid
    plt.savefig(str(grid_path))
    # Close figure
    plt.close()
    print(f"Grid preview saved to:")
    print( grid_path)


# DETECTION ANALYSIS
print("DETECTION ANALYSIS")

# Number of images
total_images = len(all_results_summary)
# Total objects
total_detections = sum(
    result["num_detections"]
    for result
    in all_results_summary
)


# Class counts
class_counts = {}
# Confidence scores
confidences = []


# Process summaries
for result in all_results_summary:
    for detection in result["detections"]:
        class_name = detection["class_name"]
        confidence = detection["confidence"]
        # Count class
        class_counts[class_name] = (class_counts.get(class_name,0)+ 1)
        # Store confidence
        confidences.append(confidence)
# Print analysis
print(f"Images processed: "f"{total_images}")
print(f"Total objects detected: "f"{total_detections}")


if total_images > 0: print(f"Average detections per image: "f"{total_detections / total_images:.2f}")
if confidences: 
    average_confidence = (sum(confidences)/ len(confidences))


    print(f"Average confidence: "f"{average_confidence:.2%}")
    print(f"Minimum confidence: "f"{min(confidences):.2%}")
    print(f"Maximum confidence: "f"{max(confidences):.2%}")


# Print class breakdown
print("\nDetections by class:")
if class_counts:
    for class_name, count in sorted(
        class_counts.items(),
        key=lambda item: -item[1]
    ):
        print(f"  {class_name:12s}: "f"{count}")
else:
    print("  No objects detected.")


#VEHICLE DETECTION SUMMARY

print("VEHICLE DETECTION SUMMARY")
vehicle_counts = {}
total_vehicle_detections = 0


# Check every detection
for result in all_results_summary:
    for detection in result["detections"]:
        class_id = detection["class_id"]
        class_name = detection["class_name"]

        # Check whether class is a vehicle
        if class_id in VEHICLE_CLASSES:
            total_vehicle_detections += 1

            vehicle_counts[class_name] = (vehicle_counts.get(class_name,0)+ 1)


print(f"Total vehicle detections: "f"{total_vehicle_detections}")
print("\nBreakdown by vehicle type:")


if vehicle_counts:
    for vehicle_type, count in sorted(
        vehicle_counts.items(),
        key=lambda item: -item[1]
    ):

        print(f"  {vehicle_type:12s}: " f"{count}")

else:
    print("No vehicles detected.")

# FINAL MESSAGE
print("YOLO VEHICLE DETECTION COMPLETED!")
print("\nPrediction images saved in:")
print(OUTPUT_DIR)
print("\nGrid preview saved as:")
print(OUTPUT_DIR / "_grid_preview.png")

