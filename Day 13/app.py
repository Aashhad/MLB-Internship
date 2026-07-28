# Then open the local URL Gradio prints (usually http://127.0.0.1:7860).


import cv2
import gradio as gr
from ultralytics import YOLO

# Load model once at startup (fast after first download)
MODEL_NAME = "yolov8n.pt"  # swap for "yolo11n.pt" or a custom-trained "best.pt" if you have one
model = YOLO(MODEL_NAME)


def detect_vehicles(input_image, confidence):
    """
    input_image: numpy array (RGB) from Gradio
    confidence: float slider value
    Returns: annotated RGB image, text summary
    """
    if input_image is None:
        return None, "Please upload an image."

    results = model.predict(source=input_image, conf=confidence, verbose=False)
    result = results[0]

    # result.plot() returns BGR; convert to RGB for Gradio display
    annotated_bgr = result.plot()
    annotated_rgb = cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB)

    # Build a readable summary
    if len(result.boxes) == 0:
        summary = "No objects detected above this confidence threshold."
    else:
        counts = {}
        for box in result.boxes:
            cls_name = model.names[int(box.cls[0])]
            counts[cls_name] = counts.get(cls_name, 0) + 1
        lines = [f"Detected {len(result.boxes)} object(s):"]
        for cls_name, count in sorted(counts.items(), key=lambda x: -x[1]):
            lines.append(f"  • {cls_name}: {count}")
        summary = "\n".join(lines)

    return annotated_rgb, summary


demo = gr.Interface(
    fn=detect_vehicles,
    inputs=[
        gr.Image(type="numpy", label="Upload an image"),
        gr.Slider(minimum=0.05, maximum=0.95, value=0.25, step=0.05,
                   label="Confidence threshold"),
    ],
    outputs=[
        gr.Image(type="numpy", label="Detections"),
        gr.Textbox(label="Summary"),
    ],
    title="🚗 Vehicle Detection with YOLO",
    description=(
        "Upload a street/traffic photo. The pretrained YOLO model will detect "
        "vehicles (car, truck, bus, motorcycle, bicycle, train) and draw bounding "
        "boxes with confidence scores."
    ),
    examples=None,  # add ["sample_images/example1.jpg"] once you have sample images
)

if __name__ == "__main__":
    demo.launch()