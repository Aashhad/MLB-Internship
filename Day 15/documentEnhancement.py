"""
====================================================================
 Document Image Enhancement Tool
====================================================================
A Gradio web app that cleans up photos of documents so they look
like proper scans.

Pipeline (in order):
  1. Load a document image        -> from your computer OR the bundled dataset
  2. Perspective correction       -> straightens a tilted/skewed document
  3. Grayscale conversion         -> removes color, keeps only intensity
  4. Noise reduction              -> removes speckle / camera noise
  5. Brightness & contrast boost  -> makes text pop, background cleaner
  6. Blur (optional)              -> softens the image / hides texture noise
  7. Sharpening                   -> crisper text edges
  8. Display the final result

The UI lets you either:
  (a) run the FULL pipeline in one click, or
  (b) pick ONE step at a time from a dropdown to see what each
      step does individually (great for learning / demos).
====================================================================
"""

import os
import glob
import cv2
import numpy as np
import gradio as gr

# STEP 0 — Locate the bundled sample dataset (expects a "dataset" folder sitting next to this script, e.g. Day 15/dataset/image1.jpg ... image10.jpg — matching your project layout)
SAMPLE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")
SAMPLE_IMAGES = sorted(glob.glob(os.path.join(SAMPLE_DIR, "*.jpg")))
SAMPLE_NAMES = [os.path.basename(p) for p in SAMPLE_IMAGES]


# STEP 1 — Helper: order 4 corner points as TL, TR, BR, BL (needed for perspective warp)
def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]        # top-left     -> smallest x+y
    rect[2] = pts[np.argmax(s)]        # bottom-right -> largest x+y
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]     # top-right    -> smallest x-y
    rect[3] = pts[np.argmax(diff)]     # bottom-left  -> largest x-y
    return rect


# STEP 2 — Perspective correction
def correct_perspective(img_bgr):
    """
    Tries to find the document's 4 edges in the photo and warps
    it into a straight, top-down rectangle (like a flatbed scan).
    If no clean 4-corner outline is found (e.g. document fills the
    whole frame, or background is busy), the original image is
    returned unchanged.
    """
    orig = img_bgr.copy()
    h = img_bgr.shape[0]
    ratio = h / 500.0 if h > 500 else 1.0
    resized = cv2.resize(img_bgr, (int(img_bgr.shape[1] / ratio), int(h / ratio)))

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    edged = cv2.dilate(edged, np.ones((3, 3), np.uint8), iterations=1)

    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

    doc_contour = None
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4 and cv2.contourArea(c) > 0.2 * resized.shape[0] * resized.shape[1]:
            doc_contour = approx
            break

    if doc_contour is None:
        return orig, False  # nothing found -> pass image through unchanged

    pts = doc_contour.reshape(4, 2).astype("float32") * ratio
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    width = max(int(np.linalg.norm(br - bl)), int(np.linalg.norm(tr - tl)))
    height = max(int(np.linalg.norm(tr - br)), int(np.linalg.norm(tl - bl)))

    dst = np.array([[0, 0], [width - 1, 0],
                     [width - 1, height - 1], 
                     [0, height - 1]], 
                     dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(orig, M, (width, height))
    return warped, True


# STEP 3 — Grayscale conversion
def to_grayscale(img_bgr):
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)  # keep 3 channels for consistent display


# STEP 4 — Noise reduction
def denoise_image(img_bgr, strength=10):
    is_gray = np.all(img_bgr[:, :, 0] == img_bgr[:, :, 1]) and np.all(img_bgr[:, :, 1] == img_bgr[:, :, 2])
    if is_gray:
        gray = img_bgr[:, :, 0]
        denoised = cv2.fastNlMeansDenoising(gray, None, h=strength, templateWindowSize=7, searchWindowSize=21)
        return cv2.cvtColor(denoised, cv2.COLOR_GRAY2BGR)
    return cv2.fastNlMeansDenoisingColored(img_bgr, None, h=strength, hColor=strength, templateWindowSize=7, searchWindowSize=21)


# STEP 5 — Brightness & contrast enhancement
def enhance_brightness_contrast(img_bgr, brightness=15, contrast=25):
    """
    brightness: -100..100  (added to every pixel)
    contrast:   -100..100  (scales pixel spread around 127)
    """
    b = brightness
    c = contrast
    f = 131 * (c + 127) / (127 * (131 - c)) if c != 0 else 1.0
    img = cv2.addWeighted(img_bgr, f, img_bgr, 0, b - 128 * f + 128) if c != 0 else img_bgr.copy()
    if b != 0 and c == 0:
        img = cv2.convertScaleAbs(img_bgr, alpha=1.0, beta=b)
    return np.clip(img, 0, 255).astype(np.uint8)


# STEP 6 — Blur (NEW)
def blur_image(img_bgr, blur_type="Gaussian", strength=5):
    
    # Softens the image. Useful for hiding paper texture/grain before
    # other steps, or as a standalone effect.

    # blur_type: "Gaussian", "Median", or "Average"
    # strength:  odd kernel size (bigger = blurrier). Values are
    #            automatically forced to be odd, since OpenCV requires
    #            odd kernel sizes for Gaussian/Median blur.
    
    k = int(strength)
    if k < 1:
        k = 1
    if k % 2 == 0:
        k += 1  # kernel size must be odd

    if blur_type == "Median":
        return cv2.medianBlur(img_bgr, k)
    elif blur_type == "Average":
        return cv2.blur(img_bgr, (k, k))
    else:  # Gaussian (default)
        return cv2.GaussianBlur(img_bgr, (k, k), 0)


# STEP 7 — Sharpening
def sharpen_image(img_bgr, amount=1.0):
    blurred = cv2.GaussianBlur(img_bgr, (0, 0), sigmaX=3)
    sharpened = cv2.addWeighted(img_bgr, 1 + amount, blurred, -amount, 0)
    return np.clip(sharpened, 0, 255).astype(np.uint8)


# STEP 8 — Full pipeline (runs all steps in order)
def full_pipeline(img_bgr, brightness, contrast, denoise_strength, sharpen_amount,
                   apply_blur=False, blur_type="Gaussian", blur_strength=5):
    img, found = correct_perspective(img_bgr)
    img = to_grayscale(img)
    img = denoise_image(img, strength=denoise_strength)
    img = enhance_brightness_contrast(img, brightness=brightness, contrast=contrast)
    if apply_blur:
        img = blur_image(img, blur_type=blur_type, strength=blur_strength)
    img = sharpen_image(img, amount=sharpen_amount)
    note = "Perspective corrected." if found else "No clear document border found — perspective step skipped."
    if apply_blur:
        note += f" Blur ({blur_type}, strength={blur_strength}) applied."
    return img, note


# STEP 9 — Gradio glue code
OPERATIONS = [
    "Full Pipeline (all steps)",
    "1. Perspective Correction only",
    "2. Grayscale only",
    "3. Noise Reduction only",
    "4. Brightness / Contrast only",
    "5. Blur only",
    "6. Sharpen only",
]


def load_sample(sample_name):
    if not sample_name:
        return None
    path = os.path.join(SAMPLE_DIR, sample_name)
    img_bgr = cv2.imread(path)
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)


def process(image_rgb, operation, brightness, contrast, denoise_strength, sharpen_amount,
            apply_blur, blur_type, blur_strength):
    if image_rgb is None:
        return None, "⚠️ Please upload an image or pick one from the sample dropdown first."

    img_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    if operation == "Full Pipeline (all steps)":
        result, note = full_pipeline(
            img_bgr, brightness, contrast, denoise_strength, sharpen_amount,
            apply_blur=apply_blur, blur_type=blur_type, blur_strength=blur_strength,
        )
    elif operation.startswith("1"):
        result, found = correct_perspective(img_bgr)
        note = "Perspective corrected." if found else "No clear document border found — original image returned."
    elif operation.startswith("2"):
        result = to_grayscale(img_bgr)
        note = "Converted to grayscale."
    elif operation.startswith("3"):
        result = denoise_image(img_bgr, strength=denoise_strength)
        note = f"Noise reduced (strength={denoise_strength})."
    elif operation.startswith("4"):
        result = enhance_brightness_contrast(img_bgr, brightness=brightness, contrast=contrast)
        note = f"Brightness={brightness}, Contrast={contrast} applied."
    elif operation.startswith("5"):
        result = blur_image(img_bgr, blur_type=blur_type, strength=blur_strength)
        note = f"Blur applied ({blur_type}, strength={blur_strength})."
    elif operation.startswith("6"):
        result = sharpen_image(img_bgr, amount=sharpen_amount)
        note = f"Sharpened (amount={sharpen_amount})."
    else:
        return None, "Unknown operation."

    result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    return result_rgb, "✅ " + note


# STEP 10 — Build the UI
with gr.Blocks(title="Document Image Enhancement Tool") as demo:
    gr.Markdown("# 📄 Document Image Enhancement Tool")
    gr.Markdown(
        "Upload your own document photo **or** pick one of the bundled sample "
        "images, choose an enhancement step from the dropdown, and click **Apply**."
    )
    gr.Markdown("Developed by : MUHAMMAD ASHHAD")

    with gr.Row():
        with gr.Column():
            sample_dropdown = gr.Dropdown(
                choices=SAMPLE_NAMES, label="📁 Or pick a sample image from the dataset",
                value=None,
            )
            image_input = gr.Image(label="Input Document Image", type="numpy")

            operation_dropdown = gr.Dropdown(
                choices=OPERATIONS, value="Full Pipeline (all steps)",
                label="⚙️ Choose enhancement step",
            )

            with gr.Accordion("Advanced settings", open=False):
                brightness_slider = gr.Slider(-100, 100, value=15, step=1, label="Brightness")
                contrast_slider = gr.Slider(-100, 100, value=25, step=1, label="Contrast")
                denoise_slider = gr.Slider(0, 30, value=10, step=1, label="Denoise strength")
                sharpen_slider = gr.Slider(0.0, 3.0, value=1.0, step=0.1, label="Sharpen amount")

                gr.Markdown("**Blur** (used by 'Blur only', and optionally in the full pipeline)")
                blur_toggle = gr.Checkbox(value=False, label="Apply blur in Full Pipeline")
                blur_type_dropdown = gr.Dropdown(
                    choices=["Gaussian", "Median", "Average"], value="Gaussian", label="Blur type"
                )
                blur_strength_slider = gr.Slider(1, 25, value=5, step=2, label="Blur strength (kernel size)")

            apply_btn = gr.Button("✨ Apply Enhancement", variant="primary")

        with gr.Column():
            output_image = gr.Image(label="Enhanced Output")
            status_box = gr.Textbox(label="Status", interactive=False)

    # when a sample is picked from the dropdown, load it into the image box
    sample_dropdown.change(fn=load_sample, inputs=sample_dropdown, outputs=image_input)

    # main action
    apply_btn.click(
        fn=process,
        inputs=[image_input, operation_dropdown, brightness_slider,
                contrast_slider, denoise_slider, sharpen_slider,
                blur_toggle, blur_type_dropdown, blur_strength_slider],
        outputs=[output_image, status_box],
    )

if __name__ == "__main__":
    demo.launch()