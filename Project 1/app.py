import cv2
import json
import glob
import os
import gradio as gr

from src.occupancyDecision import (
    check_occupancy,
    DEFAULT_THRESHOLD
)

from src.visualization import draw

# ==========================================================
# PATHS
# ==========================================================

PROJECT_DIR = "Project 1"

ANNOTATION_PATH = os.path.join(
    PROJECT_DIR,
    "annotation",
    "parking_slots.json"
)

INPUT_FOLDER = os.path.join(
    PROJECT_DIR,
    "dataset",
    "inputImages"
)

OUTPUT_FOLDER = os.path.join(
    PROJECT_DIR,
    "dataset",
    "outputImages"
)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==========================================================
# LOAD PARKING SLOTS
# ==========================================================

with open(ANNOTATION_PATH, "r") as file:
    parking_slots = json.load(file)

print(f"Loaded {len(parking_slots)} parking slots.")

# ==========================================================
# LOAD INPUT IMAGES
# ==========================================================

sample_images = []

for ext in ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]:
    sample_images.extend(
        glob.glob(os.path.join(INPUT_FOLDER, ext))
    )

sample_images = sorted(set(sample_images))

image_names = [
    os.path.basename(img)
    for img in sample_images
]

image_map = {
    os.path.basename(img): img
    for img in sample_images
}

print(f"Loaded {len(sample_images)} images.")

# ==========================================================
# SHOW INPUT IMAGE
# ==========================================================

def show_input_image(image_name):

    path = image_map[image_name]

    image = cv2.imread(path)

    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    return image, path

# ==========================================================
# ANALYZE
# ==========================================================

def analyze_parking(image_path, threshold):

    image = cv2.imread(image_path)

    occupied, vacant, used_threshold = check_occupancy(
        image,
        parking_slots,
        threshold
    )

    result = draw(
        image.copy(),
        occupied,
        vacant
    )

    image_name = os.path.basename(image_path)
    file_name = os.path.splitext(image_name)[0]

    output_path = os.path.join(
        OUTPUT_FOLDER,
        f"{file_name}_result.jpg"
    )

    cv2.imwrite(output_path, result)

    result = cv2.cvtColor(
        result,
        cv2.COLOR_BGR2RGB
    )

    total = len(parking_slots)

    occupied_count = len(occupied)
    vacant_count = len(vacant)

    occupancy = occupied_count / total * 100

    report = f"""
## Analysis Report

**Image:** {image_name}

**Total Slots:** {total}

**Occupied:** {occupied_count}

**Vacant:** {vacant_count}

**Occupancy:** {occupancy:.1f} %

**Threshold:** {used_threshold:.2f}

**Saved To**

{output_path}
"""

    return result, report

# ==========================================================
# UI
# ==========================================================

with gr.Blocks(
    title="Smart Parking Lot Occupancy Analyzer",
    theme=gr.themes.Soft()
) as app:

    gr.Markdown("""
# 🅿️ Smart Parking Lot Occupancy Analyzer

Select an image, adjust the threshold and click **Analyze Parking**.

The processed image will automatically be saved inside **outputImages**.

**Developed by Muhammad Ashhad**
""")

    image_path = gr.State(sample_images[0])

    with gr.Row():

        with gr.Column(scale=1):

            image_dropdown = gr.Dropdown(
                choices=image_names,
                value=image_names[0],
                label="📂 Select Input Image"
            )

            input_image = gr.Image(
                label="📥 Input Image",
                interactive=False,
                height=350
            )

            threshold = gr.Slider(
                minimum=0,
                maximum=1,
                value=DEFAULT_THRESHOLD,
                step=0.01,
                label="Edge Density Threshold"
            )

            analyze_btn = gr.Button(
                "🔍 Analyze Parking",
                variant="primary",
                size="lg"
            )

        with gr.Column(scale=1):

            output_image = gr.Image(
                label="📤 Output Image",
                height=500
            )

            statistics = gr.Markdown()

    image_dropdown.change(
        fn=show_input_image,
        inputs=image_dropdown,
        outputs=[
            input_image,
            image_path
        ]
    )

    analyze_btn.click(
        fn=analyze_parking,
        inputs=[
            image_path,
            threshold
        ],
        outputs=[
            output_image,
            statistics
        ]
    )

    app.load(
        fn=show_input_image,
        inputs=image_dropdown,
        outputs=[
            input_image,
            image_path
        ]
    )

if __name__ == "__main__":
    app.launch()