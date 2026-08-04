import os
import cv2
import numpy as np
import gradio as gr

# Create Output Folder
OUTPUT_FOLDER = r"Day 16\outputImages"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Edge Detection
def edge_detection(gray, method, t1, t2):

    if method == "Canny":
        edges = cv2.Canny(gray, t1, t2)

    elif method == "Sobel":

        sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

        edges = cv2.magnitude(sx, sy)
        edges = np.uint8(np.clip(edges,0,255))

    elif method == "Laplacian":

        edges = cv2.Laplacian(gray, cv2.CV_64F)
        edges = np.uint8(np.absolute(edges))

    return edges


# Morphology

def morphology(img, operation, kernel_size):

    kernel = np.ones((kernel_size,kernel_size), np.uint8)

    if operation=="None":
        return img

    elif operation=="Erosion":
        return cv2.erode(img,kernel,iterations=1)

    elif operation=="Dilation":
        return cv2.dilate(img,kernel,iterations=1)

    elif operation=="Opening":
        return cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)

    elif operation=="Closing":
        return cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)

    elif operation=="Gradient":
        return cv2.morphologyEx(img,cv2.MORPH_GRADIENT,kernel)

    elif operation=="Top Hat":
        return cv2.morphologyEx(img,cv2.MORPH_TOPHAT,kernel)

    elif operation=="Black Hat":
        return cv2.morphologyEx(img,cv2.MORPH_BLACKHAT,kernel)


# 
# Main Processing

def detect_document(image,
                    edge_method,
                    morph_method,
                    blur_size,
                    kernel_size,
                    threshold1,
                    threshold2):

    if image is None:
        return None, None, None, None

    original = image.copy()

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    if blur_size % 2 == 0:
        blur_size += 1

    blurred = cv2.GaussianBlur(gray, (blur_size, blur_size), 0)

    edges = edge_detection(
        blurred,
        edge_method,
        threshold1,
        threshold2
    )

    morph = morphology(edges, morph_method, kernel_size)

    contours, _ = cv2.findContours(
        morph,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    result = original.copy()

    if contours:

        largest = max(contours, key=cv2.contourArea)

        epsilon = 0.02 * cv2.arcLength(largest, True)

        approx = cv2.approxPolyDP(largest, epsilon, True)

        cv2.drawContours(
            result,
            [approx],
            -1,
            (0,255,0),
            5
        )

    filename = os.path.join(
        OUTPUT_FOLDER,
        "document_boundary_result.png"
    )

    cv2.imwrite(
        filename,
        cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    )

    return gray, edges, morph, result


# Professional Theme


css = """

.gradio-container{
    max-width:1300px !important;
    margin:auto;
}

h1{
    text-align:center;
    color:#1E88E5;
}

footer{
    display:none;
}

"""


# Interface

with gr.Blocks(css=css,
               theme=gr.themes.Soft()) as demo:

    gr.Markdown(
        """
# 📄 Document Boundary Detection Tool

### OpenCV + Gradio

Detect document boundaries using different Edge Detection and Morphological Operations.
"""
    )

    with gr.Row():

        with gr.Column(scale=1):

            image = gr.Image(
                type="numpy",
                label="Upload Document"
            )

            edge = gr.Dropdown(
                ["Canny","Sobel","Laplacian"],
                value="Canny",
                label="Edge Detection"
            )

            morph = gr.Dropdown(
                [
                    "None",
                    "Erosion",
                    "Dilation",
                    "Opening",
                    "Closing",
                    "Gradient",
                    "Top Hat",
                    "Black Hat"
                ],
                value="Closing",
                label="Morphological Operation"
            )

            blur = gr.Slider(
                3,
                15,
                value=5,
                step=2,
                label="Gaussian Blur Kernel"
            )

            kernel = gr.Slider(
                3,
                15,
                value=5,
                step=2,
                label="Morphology Kernel"
            )

            t1 = gr.Slider(
                0,
                255,
                value=50,
                label="Threshold 1"
            )

            t2 = gr.Slider(
                0,
                255,
                value=150,
                label="Threshold 2"
            )

            btn = gr.Button(
                "Detect Boundary",
                variant="primary"
            )

        with gr.Column(scale=2):

            with gr.Row():

                gray = gr.Image(label="Grayscale")

                edge_img = gr.Image(label="Edge Detection")

            with gr.Row():

                morph_img = gr.Image(label="Morphology Output")

                result = gr.Image(label="Detected Boundary")

    btn.click(
        detect_document,
        inputs=[
            image,
            edge,
            morph,
            blur,
            kernel,
            t1,
            t2
        ],
        outputs=[
            gray,
            edge_img,
            morph_img,
            result
        ]
    )
    gr.Markdown("""
# 📄 Document Boundary Detection Tool

### OpenCV + Gradio

Upload a document image, choose an edge detector and morphology operation, then detect and visualize the document boundary.

**Author:** Muhammad Ashhad
"""
)
    demo.launch(share=True)

