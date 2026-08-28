
import gradio as gr
from ultralytics import YOLO
from pathlib import Path
from datetime import datetime


# CONFIGURATION

MODEL_PATH = "Day 24/model/best.pt"

INPUT_FOLDER = Path("Day 24/images/input")
OUTPUT_FOLDER = Path("Day 24/images/output")

CONFIDENCE_THRESHOLD = 0.25
IMAGE_SIZE = 640
DEVICE = "cpu"


# CREATE DIRECTORIES

INPUT_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


# LOAD MODEL
model = YOLO(MODEL_PATH)


# GET SAMPLE IMAGES

def get_sample_images():

    extensions = [
        "*.jpg",
        "*.jpeg",
        "*.png",
        "*.bmp",
        "*.webp"
    ]

    images = []

    for extension in extensions:
        images.extend(INPUT_FOLDER.glob(extension))

    return sorted(images)


# DETECTION FUNCTION

def detect_cups(uploaded_image, sample_image):

    """
    Detect cups from either:

    1. Uploaded image
    2. Sample image from input folder

    The detection result is displayed and saved.
    """

    # SELECT IMAGE SOURCE

    if uploaded_image is not None:

        image_source = uploaded_image
        image_name = "uploaded_image"

    elif sample_image is not None:

        image_source = sample_image
        image_name = Path(sample_image).stem

    else:

        return None, "⚠️ Please upload an image or select a sample image."

    # RUN YOLO

    results = model.predict(
        source=image_source,
        conf=CONFIDENCE_THRESHOLD,
        imgsz=IMAGE_SIZE,
        device=DEVICE,
        verbose=False
    )

    result = results[0]

    # GET ANNOTATED IMAGE
    # pil=True returns PIL image directly.
    # Therefore, no manual RGB/BGR conversion is required.
    annotated_image = result.plot(pil=True)

    # CREATE OUTPUT FILENAME

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{image_name}_{timestamp}.jpg"
    output_path = OUTPUT_FOLDER / output_filename

    # SAVE RESULT
    annotated_image.save(output_path)

    # COUNT DETECTIONS
    number_of_cups = len(result.boxes)

    # GET CONFIDENCE SCORES

    confidence_scores = []

    for confidence in result.boxes.conf:

        confidence_scores.append(f"{float(confidence):.2f}")

    # DETECTION INFORMATION

    if number_of_cups > 0:

        message = (
            f"✅ Detection completed!\n\n"
            f"🥤 Cups detected: {number_of_cups}\n"
            f"📊 Confidence scores: "
            f"{', '.join(confidence_scores)}\n\n"
            f"💾 Saved to:\n"
            f"{output_path}"
        )

    else:

        message = (
            f"ℹ️ No cups detected.\n\n"
            f"💾 Result saved to:\n"
            f"{output_path}"
        )

    return annotated_image, message


# REFRESH SAMPLE IMAGES

def refresh_samples():

    images = get_sample_images()

    image_paths = [
        str(image)
        for image in images
    ]

    return gr.update(choices=image_paths, value=None)


# GRADIO APPLICATION

with gr.Blocks(
    title="Cup Detection System"
) as app:

    # HEADER

    gr.Markdown(
        """
        # 🥤 Cup Detection System

        ### YOLOv8 Custom Object Detection

        Detect cups using your trained YOLO model.

        You can either **upload a new image** or
        **select a sample image** from the input folder.
        """
    )

    # INPUT SECTION

    with gr.Row():

        # UPLOAD IMAGE

        with gr.Column():

            gr.Markdown("### 📤 Upload New Image")

            uploaded_image = gr.Image(
                type="pil",
                label="Upload Any Image"
            )

        # SAMPLE IMAGE

        with gr.Column():
            gr.Markdown("### 🖼️ Select Sample Image")

            sample_image = gr.Dropdown(
                choices=[
                    str(image)
                    for image in get_sample_images()
                ],
                label="Sample Images",
                interactive=True
            )

            refresh_button = gr.Button(
                "🔄 Refresh Sample Images"
            )

    # DETECT BUTTON

    detect_button = gr.Button(
        "🔍 Detect Cups",
        variant="primary",
        size="lg"
    )

    # OUTPUT SECTION

    with gr.Row():
        with gr.Column():

            output_image = gr.Image(
                type="pil",
                label="Detection Result"
            )

        with gr.Column():

            detection_info = gr.Textbox(
                label="Detection Information",
                lines=8
            )

    # BUTTON EVENTS

    detect_button.click(
        fn=detect_cups,
        inputs=[uploaded_image, sample_image],
        outputs=[output_image, detection_info]
    )

    refresh_button.click(fn=refresh_samples, inputs=None, outputs=sample_image)


    # MODEL INFORMATION

    gr.Markdown(
        f"""
        ---

        ### Developed By : Muhammad Ashhad.
        """
    )


# LAUNCH APPLICATION

if __name__ == "__main__":

    app.launch()
