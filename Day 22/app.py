import cv2
import numpy as np
import gradio as gr
import os


# CONFIGURATION
OUTPUT_FOLDER = "Day 22/images/outputImages"

# Create output directory
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# HELPER FUNCTION

def add_label(image, text):
    """
    Add a label to an image.
    """

    result = image.copy()

    cv2.putText(
        result,
        text,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
        cv2.LINE_AA
    )

    return result


# PREPROCESS IMAGE

def preprocess_image(image):
    """
    Convert RGB image to grayscale.
    """

    # Gradio gives image in RGB format
    rgb_image = image.copy()

    # Convert RGB to grayscale
    gray = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)

    # Slight Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    return rgb_image, gray, blurred


# BINARY THRESHOLD

def binary_threshold(gray):
    """
    Apply fixed binary thresholding.
    """

    threshold_value = 127

    _, result = cv2.threshold(
        gray,
        threshold_value,
        255,
        cv2.THRESH_BINARY
    )

    return result


# ADAPTIVE THRESHOLD

def adaptive_threshold(gray):
    """
    Apply adaptive Gaussian thresholding.
    """

    block_size = 11
    C = 2

    result = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        block_size,
        C
    )

    return result


# OTSU THRESHOLD

def otsu_threshold(gray):
    """
    Apply Otsu automatic thresholding.
    """

    threshold_value, result = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return result, threshold_value


# MORPHOLOGICAL CLEANING

def clean_mask(mask):
    """
    Remove small noise and fill small holes.
    """

    # Morphological kernel
    kernel = np.ones((5, 5), np.uint8)

    # Remove small noise
    opened = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel,
        iterations=1
    )

    # Close small holes
    closed = cv2.morphologyEx(
        opened,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    return closed


# FIND MAIN OBJECT

def get_main_object_mask(mask):
    """
    Find the largest contour and create a mask
    for the main object/document.
    """

    # Find contours
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # If no contour found
    if not contours:
        return mask

    # Find largest contour
    largest_contour = max(
        contours,
        key=cv2.contourArea
    )

    # Create empty mask
    main_mask = np.zeros_like(mask)

    # Draw largest contour
    cv2.drawContours(
        main_mask,
        [largest_contour],
        -1,
        255,
        thickness=cv2.FILLED
    )

    return main_mask


# CREATE FOREGROUND

def create_foreground(image, mask):
    """
    Extract foreground from original image.
    """

    foreground = cv2.bitwise_and(
        image,
        image,
        mask=mask
    )

    return foreground


# CREATE TRANSPARENT BACKGROUND

def create_transparent_result(image, mask):
    """
    Create RGBA image where background becomes transparent.
    """

    # Convert RGB to RGBA
    rgba = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)

    # Put mask into alpha channel
    rgba[:, :, 3] = mask

    return rgba


# SEGMENTATION QUALITY SCORE

def calculate_score(mask):
    """
    Calculate a simple score for selecting
    the best segmentation method.

    This is not a machine-learning accuracy score.
    It is a heuristic based on the foreground area.
    """

    total_pixels = mask.shape[0] * mask.shape[1]

    foreground_pixels = cv2.countNonZero(mask)

    percentage = ( foreground_pixels / total_pixels ) * 100

    # Prefer masks that contain a reasonable
    # foreground area.

    if 10 <= percentage <= 90:
        score = 100

    elif 5 <= percentage < 10:
        score = 70

    elif 90 < percentage <= 95:
        score = 70

    else:
        score = 30

    return score, percentage


# MAIN SEGMENTATION FUNCTION

def segment_image(
    image,
    selected_method,
    threshold_value,
    block_size,
    C
):
    """
    Main function used by Gradio.
    """

    # Check input
    if image is None:

        return (
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            "Please upload an image first."
        )

    # Convert image

    rgb_image = image.copy()

    gray = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)

    # Blur image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Binary threshold

    _, binary = cv2.threshold(
        blurred,
        int(threshold_value),
        255,
        cv2.THRESH_BINARY
    )

    # Adaptive threshold

    # Ensure block size is odd
    block_size = int(block_size)

    if block_size % 2 == 0:
        block_size += 1

    if block_size < 3:
        block_size = 3

    adaptive = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        block_size,
        int(C)
    )

    # Otsu threshold

    otsu_value, otsu = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Select segmentation method

    if selected_method == "Binary":
        selected_mask = binary
        method_name = "Binary"

    elif selected_method == "Adaptive":
        selected_mask = adaptive
        method_name = "Adaptive"

    elif selected_method == "Otsu":
        selected_mask = otsu
        method_name = "Otsu"

    else:

        # Automatic mode
        methods = {
            "Binary": binary,
            "Adaptive": adaptive,
            "Otsu": otsu
        }

        scores = {}

        for name, current_mask in methods.items():

            cleaned = clean_mask(current_mask)

            main_mask = get_main_object_mask(cleaned)

            score, percentage = calculate_score(main_mask)

            scores[name] = (score, percentage, main_mask)

        # Select highest score
        best_method = max(scores, key=lambda x: scores[x][0])

        selected_mask = scores[ best_method ][2]

        method_name = best_method

    # Clean selected mask

    cleaned_mask = clean_mask(selected_mask)

    # Extract largest/main object

    final_mask = get_main_object_mask(cleaned_mask)

    # Create foreground

    foreground = create_foreground(rgb_image, final_mask)

    # Create transparent result

    transparent_result = create_transparent_result(rgb_image, final_mask)

    # Calculate score

    score, foreground_percentage = calculate_score(final_mask)

    # Save outputs

    cv2.imwrite(
        os.path.join(OUTPUT_FOLDER, "original.png"),
        cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR))

    cv2.imwrite(os.path.join(OUTPUT_FOLDER, "grayscale.png"), gray)
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, "binary.png"), binary)
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, "adaptive.png"), adaptive)

    cv2.imwrite(os.path.join(OUTPUT_FOLDER, "otsu.png"), otsu)
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, "foreground_mask.png"), final_mask)
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, "foreground.png"),
        cv2.cvtColor(foreground, cv2.COLOR_RGB2BGR)
    )

    # Save transparent PNG
    cv2.imwrite(
        os.path.join(OUTPUT_FOLDER, "best_segmentation.png"),
        cv2.cvtColor(transparent_result, cv2.COLOR_RGBA2BGRA)
    )

    # Create comparison images

    display_size = (400, 300)

    original_display = cv2.resize(rgb_image, display_size)
    binary_display = cv2.resize(binary, display_size)
    adaptive_display = cv2.resize(adaptive, display_size)
    otsu_display = cv2.resize(otsu, display_size)
    mask_display = cv2.resize(final_mask, display_size)
    foreground_display = cv2.resize(foreground, display_size)

    # Convert grayscale images to RGB
    binary_display = cv2.cvtColor(binary_display, cv2.COLOR_GRAY2RGB)
    adaptive_display = cv2.cvtColor(adaptive_display, cv2.COLOR_GRAY2RGB)
    otsu_display = cv2.cvtColor(otsu_display, cv2.COLOR_GRAY2RGB)
    mask_display = cv2.cvtColor(mask_display, cv2.COLOR_GRAY2RGB)

    # Add labels
    original_display = add_label(original_display, "Original")
    binary_display = add_label(binary_display, "Binary")
    adaptive_display = add_label(adaptive_display, "Adaptive")
    otsu_display = add_label(otsu_display, "Otsu")
    mask_display = add_label(mask_display, "Final Mask")

    foreground_display = add_label(foreground_display, "Foreground")

    # Combine comparison

    top_row = np.hstack([original_display, binary_display])
    middle_row = np.hstack([adaptive_display, otsu_display])
    bottom_row = np.hstack([mask_display, foreground_display])
    comparison = np.vstack([top_row, middle_row, bottom_row])

    # Save comparison
    cv2.imwrite(
        os.path.join(OUTPUT_FOLDER, "comparison.png"),
        cv2.cvtColor(comparison,cv2. COLOR_RGB2BGR)
    )

    # Information

    information = f"""
### Segmentation Result
**Selected Method:** {method_name}
**Otsu Threshold:** {otsu_value:.2f}
**Foreground Area:** {foreground_percentage:.2f}%
**Segmentation Score:** {score}/100
**Saved File:**
`{OUTPUT_FOLDER}/best_segmentation.png`
"""

    return (
        rgb_image,
        binary,
        adaptive,
        otsu,
        final_mask,
        foreground,
        transparent_result,
        information
    )


# RESET FUNCTION

def reset_app():
    """
    Reset all outputs.
    """

    return (
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ""
    )


# GRADIO INTERFACE

with gr.Blocks(
    title="Document & Object Segmentation Tool"
) as demo:

    # HEADER
    gr.Markdown(
        """
        # 📄 Document & Object Segmentation Tool

        Upload an image or select a sample image below.

        The application applies:

        - Binary Thresholding
        - Adaptive Thresholding
        - Otsu Thresholding
        - Automatic Method Selection
        - Morphological Cleaning
        - Main Object Detection
        - Foreground Extraction
        - Transparent Background
        """
    )

    # INPUT SECTION

    with gr.Row():

        with gr.Column():

            # IMAGE UPLOAD

            input_image = gr.Image(
                label="Upload Image",
                type="numpy"
            )

            # SAMPLE IMAGES

            gr.Markdown(
                "### 🖼️ Sample Images"
            )

            gr.Examples(
                examples=[
                    ["Day 22/images/inputImages/Tools.jpg"],
                    ["Day 22/images/inputImages/bicycle.jpg"],
                    ["Day 22/images/inputImages/sheeps.jpg"],
                    ["Day 22/images/inputImages/lion.jpg"],
                    ["Day 22/images/inputImages/text.jpg"]
                ],
                inputs=input_image,
                label="Click a sample image",
                examples_per_page=6
            )

            # METHOD

            method = gr.Dropdown(
                choices=[
                    "Binary",
                    "Adaptive",
                    "Otsu",
                    "Automatic"
                ],
                value="Automatic",
                label="Segmentation Method"
            )

            # BINARY THRESHOLD

            threshold_slider = gr.Slider(
                minimum=0,
                maximum=255,
                value=127,
                step=1,
                label="Binary Threshold"
            )

            # ADAPTIVE BLOCK SIZE

            block_slider = gr.Slider(
                minimum=3,
                maximum=51,
                value=11,
                step=2,
                label="Adaptive Block Size"
            )

            # ADAPTIVE C

            c_slider = gr.Slider(
                minimum=-10,
                maximum=20,
                value=2,
                step=1,
                label="Adaptive C"
            )

            # BUTTONS

            with gr.Row():

                process_button = gr.Button(
                    "🚀 Segment Image",
                    variant="primary"
                )

                clear_button = gr.Button(
                    "🗑️ Clear"
                )


    # THRESHOLDING RESULTS

    gr.Markdown(
        "## 🔍 Thresholding Results"
    )

    with gr.Row():

        original_output = gr.Image(
            label="Original",
            type="numpy"
        )

        binary_output = gr.Image(
            label="Binary Threshold",
            type="numpy"
        )

    with gr.Row():

        adaptive_output = gr.Image(
            label="Adaptive Threshold",
            type="numpy"
        )

        otsu_output = gr.Image(
            label="Otsu Threshold",
            type="numpy"
        )


    # SEGMENTATION RESULTS

    gr.Markdown(
        "## ✂️ Final Segmentation"
    )

    with gr.Row():

        mask_output = gr.Image(
            label="Foreground Mask",
            type="numpy"
        )

        foreground_output = gr.Image(
            label="Extracted Foreground",
            type="numpy"
        )

    transparent_output = gr.Image(
        label="🏆 Best Segmentation - Transparent Background",
        type="numpy"
    )


    # INFORMATION

    information_output = gr.Markdown()


    # PROCESS BUTTON

    process_button.click(
        fn=segment_image,

        inputs=[
            input_image,
            method,
            threshold_slider,
            block_slider,
            c_slider
        ],

        outputs=[
            original_output,
            binary_output,
            adaptive_output,
            otsu_output,
            mask_output,
            foreground_output,
            transparent_output,
            information_output
        ]
    )


    # CLEAR BUTTON

    clear_button.click(
        fn=reset_app,

        inputs=[],

        outputs=[
            original_output,
            binary_output,
            adaptive_output,
            otsu_output,
            mask_output,
            foreground_output,
            transparent_output,
            information_output
        ]
    )


# LAUNCH

if __name__ == "__main__":

    demo.launch(
        share=True
    )