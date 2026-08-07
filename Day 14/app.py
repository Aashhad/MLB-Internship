import cv2
import gradio as gr
import numpy as np


# Image Processing Function
def process_image(
    image,
    operation,
    width,
    height,
    rotation,
    flip,
    crop_x,
    crop_y,
    crop_w,
    crop_h,
    shape,
    text,
):
    if image is None:
        return None

    img = image.copy()


    # Grayscale
    if operation == "Grayscale":
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

    # Resize
    elif operation == "Resize":
        img = cv2.resize(img, (int(width), int(height)))

    # Rotate
    elif operation == "Rotate":
        if rotation == "90°":
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif rotation == "180°":
            img = cv2.rotate(img, cv2.ROTATE_180)
        elif rotation == "270°":
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Flip
    elif operation == "Flip":
        if flip == "Horizontal":
            img = cv2.flip(img, 1)
        elif flip == "Vertical":
            img = cv2.flip(img, 0)
        elif flip == "Both":
            img = cv2.flip(img, -1)

    
    # Crop
    elif operation == "Crop":
        h, w = img.shape[:2]

        x = max(0, int(crop_x))
        y = max(0, int(crop_y))
        cw = min(int(crop_w), w - x)
        ch = min(int(crop_h), h - y)

        img = img[y:y + ch, x:x + cw]

    # Draw Shape
    elif operation == "Draw Shape":

        if shape == "Rectangle":
            cv2.rectangle(img, (50, 50), (250, 200), (0, 255, 0), 3)

        elif shape == "Circle":
            cv2.circle(img, (200, 200), 80, (255, 0, 0), 3)

        elif shape == "Line":
            cv2.line(img, (50, 50), (300, 300), (0, 0, 255), 3)

    # Add Text
    elif operation == "Add Text":
        cv2.putText(
            img,
            text,
            (40, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2,
        )

    return img


# Gradio UI
with gr.Blocks(title="Image Processing Toolkit") as demo:

    gr.Markdown(
        """
# 🖼️ Image Processing Toolkit

Perform basic image processing operations using **OpenCV**.

### Features
- Load Image
- Grayscale
- Resize
- Rotate
- Flip
- Crop
- Draw Shapes
- Add Text
- Download Processed Image

**Author:** Muhammad Ashhad
"""
    )

    with gr.Row():

        with gr.Column():

            input_image = gr.Image(type="numpy", label="Upload Image")

            operation = gr.Dropdown(
                [
                    "Grayscale",
                    "Resize",
                    "Rotate",
                    "Flip",
                    "Crop",
                    "Draw Shape",
                    "Add Text",
                ],
                value="Grayscale",
                label="Select Operation",
            )

            width = gr.Number(value=600, label="Resize Width")
            height = gr.Number(value=400, label="Resize Height")

            rotation = gr.Dropdown(
                ["90°", "180°", "270°"],
                value="90°",
                label="Rotation",
            )

            flip = gr.Dropdown(
                ["Horizontal", "Vertical", "Both"],
                value="Horizontal",
                label="Flip Direction",
            )

            crop_x = gr.Number(value=0, label="Crop X")
            crop_y = gr.Number(value=0, label="Crop Y")
            crop_w = gr.Number(value=300, label="Crop Width")
            crop_h = gr.Number(value=300, label="Crop Height")

            shape = gr.Dropdown(
                ["Rectangle", "Circle", "Line"],
                value="Rectangle",
                label="Shape",
            )

            text = gr.Textbox(
                value="OpenCV",
                label="Custom Text",
            )

            process_btn = gr.Button("Process Image", variant="primary")

        with gr.Column():

            output_image = gr.Image(
                label="Processed Image",
                type="numpy",
            )

            download = gr.File(label="Download Image")

    def save_output(img):
        if img is None:
            return None

        path = "processed_image.jpg"
        cv2.imwrite(path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        return path

    process_btn.click(
        process_image,
        inputs=[
            input_image,
            operation,
            width,
            height,
            rotation,
            flip,
            crop_x,
            crop_y,
            crop_w,
            crop_h,
            shape,
            text,
        ],
        outputs=output_image,
    )

    output_image.change(
        save_output,
        inputs=output_image,
        outputs=download,
    )

demo.launch()