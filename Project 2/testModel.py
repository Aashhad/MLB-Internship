from ultralytics import YOLO

# Path to your trained model
MODEL_PATH = "Project 2/models/best.pt"

# Load trained YOLO model
model = YOLO(MODEL_PATH)

print("=" * 60)
print("MODEL LOADED SUCCESSFULLY")
print("=" * 60)

print("Model path:", MODEL_PATH)
print("Class names:", model.names)