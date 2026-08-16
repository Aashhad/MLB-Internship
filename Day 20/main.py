import os
import cv2
import numpy as np
import easyocr
import gradio as gr
from datetime import datetime


#CREATE EASY OCR READER

print("Loading EasyOCR...")

reader = easyocr.Reader(
    ["en"],
    gpu=False
)

print("EasyOCR loaded successfully!")


# OUTPUT FOLDER

OUTPUT_FOLDER = "Day 20/images/outputImages"

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


# SAMPLE IMAGES

SAMPLE_IMAGES = [
    "Day 20/images/inputImages/text (1).jpg",
    "Day 20/images/inputImages/text (2).jpg",
    "Day 20/images/inputImages/text (3).jpg",
    "Day 20/images/inputImages/text (4).jpg",
    "Day 20/images/inputImages/text (5).jpg",
    "Day 20/images/inputImages/text (6).jpg",
    "Day 20/images/inputImages/text (7).jpg",
    "Day 20/images/inputImages/text (8).jpg",
]


# OCR FUNCTION

def extract_text(image):

    # Check image

    if image is None:
        return (
            None,
            "Please upload an image.",
            None
        )


    # Convert PIL image to NumPy
    image = np.array(image)

    # RGB -> BGR
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


    # Keep original image
    output_image = image_bgr.copy()


    # RUN EASY OCR

    results = reader.readtext(
        image_bgr,
        detail=1,
        paragraph=False,
        min_size=10,
        text_threshold=0.5,
        low_text=0.3,
        link_threshold=0.3,
        mag_ratio=1.5
    )


    # NO TEXT DETECTED

    if not results:
        output_rgb = cv2.cvtColor(
            output_image,
            cv2.COLOR_BGR2RGB
        )

        return (
            output_rgb,
            "No text detected.",
            None
        )


    # EXTRACT ONLY TEXT
    extracted_lines = []
    for detection in results:
        # EasyOCR result:
        # detection[0] = bounding box
        # detection[1] = detected text
        # detection[2] = confidence
        box = detection[0]
        text = detection[1]
        confidence = detection[2]

        # ONLY TEXT IS ADDED TO TXT FILE
        extracted_lines.append(text)


        # CONVERT BOUNDING BOX

        points = [(int(x), int(y))
            for x, y in box
        ]


        points_array = np.array(
            points,
            dtype=np.int32
        )


        # DRAW BOUNDING BOX
        cv2.polylines(
            output_image,
            [points_array],
            True,
            (0, 255, 0),
            2
        )

        # DRAW DETECTED TEXT
        cv2.putText(
            output_image,
            text[:40],
            points[0],
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


    # JOIN TEXT

    final_text = "\n".join(extracted_lines)


    # CREATE UNIQUE FILE NAME

    # Use timestamp so every OCR operation
    # creates a different TXT file.

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    output_file = os.path.join(
        OUTPUT_FOLDER,
        f"extracted_text_{timestamp}.txt"
    )


    # SAVE ONLY TEXT TO TXT FILE

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:
        
        file.write(
            final_text
        )


    # PRINT OCR RESULTS IN TERMINAL

    print("\n")
    print("=" * 60)
    print("OCR RESULTS")
    print("=" * 60)


    for detection in results:
        text = detection[1]
        confidence = detection[2]

        print(f"Text: {text}")
        print(f"Confidence: {confidence:.2f}")
        print("-" * 60)
    print(f"Text saved to: {output_file}")


    # BGR -> RGB
    output_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)


    # RETURN RESULTS
    return (
        output_image,
        final_text,
        output_file
    )


# GRADIO INTERFACE

with gr.Blocks(
    title="Simple OCR Document Reader",
    theme=gr.themes.Soft()
) as app:
    # TITLE
    gr.Markdown(
        """
        # 📄 Simple OCR Document Reader

        Upload an image or select a sample image
        to extract text using **EasyOCR**.

        ### Features

        - 🖼️ Upload an image
        - 📚 Use 10 sample images
        - 🔍 Extract text using EasyOCR
        - 📦 Detect text regions
        - 💾 Save only extracted text as `.txt`
        - ⬇️ Download extracted text

        **Note:** Confidence scores are displayed only
        in the terminal and are NOT saved in the TXT file.
        """
    )


    # MAIN ROW
    with gr.Row():

        # LEFT COLUMN
        with gr.Column(
            scale=1
        ):
            # INPUT IMAGE
            input_image = gr.Image(
                type="pil",
                label="📤 Upload Image"
            )
            # SAMPLE IMAGES
            gr.Examples(
                examples=SAMPLE_IMAGES,
                inputs=input_image,
                label="📚 Sample Images"
            )
            # EXTRACT BUTTON
            extract_button = gr.Button(
                "🔍 Extract Text",
                variant="primary"
            )
            # CLEAR BUTTON
            clear_button = gr.ClearButton(
                value="Clear"
            )
        # RIGHT COLUMN
        with gr.Column(
            scale=1
        ):
            # RESULT IMAGE
            output_image = gr.Image(
                type="numpy",
                label="🔍 OCR Detection Result"
            )
            # EXTRACTED TEXT
            extracted_text = gr.Textbox(
                label="📝 Extracted Text",
                placeholder=("Detected text will appear here..."),
                lines=15,
                interactive=False
            )
            # DOWNLOAD TXT
            download_file = gr.File(label="⬇️ Download Extracted Text")
    # CLEAR BUTTON
    clear_button.add(
        [
            input_image,
            output_image,
            extracted_text,
            download_file
        ]
    )
    # EXTRACT BUTTON
    extract_button.click(
        fn=extract_text,
        inputs=input_image,
        outputs=[
            output_image,
            extracted_text,
            download_file
        ]
    )
# LAUNCH APPLICATION

if __name__ == "__main__":
    app.launch(
        share=True
    )