import os
import cv2
import numpy as np
import gradio as gr
from datetime import datetime

# Dataset folder
DATASET_PATH = r"Day 17\dataset"

# Output folder
OUTPUT_PATH = r"Day 17\outputImages"
os.makedirs(OUTPUT_PATH, exist_ok=True)


# Shape Detection Function
def detect_shapes(image):

    if image is None:
        return None, "No image selected."

    img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    output = img.copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(
        blur,
        120,
        255,
        cv2.THRESH_BINARY_INV
    )

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    info = []
    detected_shapes = []

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area < 200:
            continue

        perimeter = cv2.arcLength(cnt, True)

        approx = cv2.approxPolyDP(
            cnt,
            0.02 * perimeter,
            True
        )

        vertices = len(approx)

        shape = "Unknown"

        if vertices == 3:
            shape = "Triangle"

        elif vertices == 4:

            x, y, w, h = cv2.boundingRect(approx)

            ratio = w / float(h)

            if 0.95 <= ratio <= 1.05:
                shape = "Square"
            else:
                shape = "Rectangle"

        elif vertices == 5:
            shape = "Pentagon"

        elif vertices == 6:
            shape = "Hexagon"

        elif vertices == 10:
            shape = "Star"

        else:

            circularity = 4 * np.pi * area / (perimeter * perimeter)

            if circularity > 0.80:
                shape = "Circle"
            else:
                shape = "Ellipse"

        # Store detected shape names
        detected_shapes.append(shape)

        # Draw contour
        cv2.drawContours(output, [approx], -1, (0, 255, 0), 3)

        # Find center
        M = cv2.moments(cnt)

        if M["m00"] != 0:

            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            cv2.putText(
                output,
                shape,
                (cx - 40, cy),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 0),
                2
            )

        info.append(
            f"{shape}\n"
            f"Area : {area:.2f}\n"
            f"Perimeter : {perimeter:.2f}\n"
        )

    # Convert to RGB
    output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

    # Create descriptive filename
    if detected_shapes:
        unique_shapes = sorted(set(detected_shapes))
        shape_part = "_".join(unique_shapes)
    else:
        shape_part = "NoShape"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{shape_part}_{timestamp}.png"

    save_path = os.path.join(OUTPUT_PATH, filename)

    # Save image
    cv2.imwrite(
        save_path,
        cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
    )

    # Prepare output text
    if len(info) == 0:
        return output, (
            "No shapes detected."
            f"\n\n💾 Image saved as:\n{filename}"
        )

    result = "\n-------------------------\n".join(info)
    result += (
        f"\n\n💾 Image saved as:\n{filename}"
    )

    return output, result

# Dataset Loader
def load_dataset_image(filename):

    if filename is None:
        return None

    path = os.path.join(DATASET_PATH, filename)

    img = cv2.imread(path)

    if img is None:
        return None

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img


# Dataset List
images = [
    f for f in os.listdir(DATASET_PATH)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]


# Gradio UI
with gr.Blocks(title="Shape Detection System") as demo:

    gr.Markdown(
        """
# 🔷 Shape Detection System

Detect and identify geometric shapes from images using **OpenCV contour analysis**. The application extracts object boundaries, classifies common shapes such as **Circle, Triangle, Square, Rectangle, Pentagon, Hexagon, and Star**, and calculates the **area** and **perimeter** of each detected shape. Users can choose a sample image from the dataset or upload their own image for real-time analysis.

### Features
- 📁 Select images from the built-in dataset
- 📤 Upload custom images
- 🔍 Automatic contour extraction
- 🟢 Shape classification
- 📏 Area and perimeter calculation
- 🖼️ Annotated output image with detected shapes
- 💾 Automatically saves processed images

**Developed by:** Muhammad Ashhad
        """
    )

    with gr.Row():

        with gr.Column():

            dropdown = gr.Dropdown(
                choices=images,
                label="Choose Dataset Image"
            )

            dataset_image = gr.Image(
                label="Dataset Image",
                type="numpy"
            )

            upload = gr.Image(
                label="Or Upload Your Own Image",
                type="numpy"
            )

            btn = gr.Button("🔍 Detect Shapes")

        with gr.Column():

            output = gr.Image(
                label="Detected Shapes"
            )

            details = gr.Textbox(
                lines=15,
                label="Detection Details"
            )

    dropdown.change(
        load_dataset_image,
        inputs=dropdown,
        outputs=dataset_image
    )

    btn.click(
        detect_shapes,
        inputs=upload,
        outputs=[output, details]
    )

    btn.click(
        detect_shapes,
        inputs=dataset_image,
        outputs=[output, details]
    )

demo.launch()