import easyocr as ocr
import cv2
import numpy as np
import os


# CREATE EASY OCR READER

reader = ocr.Reader(["en"], gpu=False)
print("EasyOCR loaded successfully!")


# FOLDERS
input_folder = "Day 20/images/inputImages"
output_folder = "Day 20/images/outputImages"
processed_folder = os.path.join(output_folder, "processed_images")
result_folder = os.path.join(output_folder, "result_images")

# CREATE FOLDERS

os.makedirs(output_folder, exist_ok=True)
os.makedirs(processed_folder, exist_ok=True)
os.makedirs(result_folder, exist_ok=True)


# IMAGE EXTENSIONS
valid_extensions = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)


# CHECK INPUT FOLDER

if not os.path.exists(input_folder):
    print(
        f"ERROR: Input folder does not exist:\n"
        f"{input_folder}"
    )
    exit()


# PROCESS ALL IMAGES

for filename in sorted(
    os.listdir(input_folder)
):
    # Check image extension
    if not filename.lower().endswith(
        valid_extensions
    ):
        continue

    print("\n")
    print("=" * 70)
    print(f"PROCESSING: {filename}")
    print("=" * 70)

    # READ IMAGE

    image_path = os.path.join(
        input_folder,
        filename
    )
    image = cv2.imread(image_path)

    if image is None:
        print(f"Could not read image: {filename}")
        continue


    # RESIZE IMAGE

    scale = 2

    image_resized = cv2.resize(
        image,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_CUBIC
    )


    # GRAYSCALE

    gray = cv2.cvtColor(
        image_resized,
        cv2.COLOR_BGR2GRAY
    )


    # DENOISING

    denoised = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )


    # CLAHE

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )
    enhanced = clahe.apply(denoised)


    # ADAPTIVE THRESHOLD

    threshold = cv2.adaptiveThreshold(
        enhanced,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )


    # MORPHOLOGICAL OPENING

    kernel = np.ones(
        (2, 2),
        np.uint8
    )

    processed = cv2.morphologyEx(
        threshold,
        cv2.MORPH_OPEN,
        kernel
    )


    # EASY OCR

    result = reader.readtext(
        processed,
        detail=1,
        paragraph=False,
        min_size=10,
        text_threshold=0.5,
        low_text=0.3,
        link_threshold=0.3,
        mag_ratio=1.5
    )


    # CHECK OCR RESULT

    if not result:
        print("No text detected.")
    else:
        print("\nDetected Text:")
        print("-" * 50)


        for detection in result:

            # EasyOCR format:
            #
            # detection[0] = bounding box
            # detection[1] = text
            # detection[2] = confidence

            box = detection[0]
            text = detection[1]
            confidence = detection[2]


            # CONFIDENCE IS ONLY PRINTED IN TERMINAL
            print(f"Text: {text}")
            print(f"Confidence: {confidence:.2f}")
            print("-" * 50)

    # DRAW OCR RESULTS
    for detection in result:
        box = detection[0]
        text = detection[1]
        confidence = detection[2]


        # Convert bounding box coordinates

        points = [(int(x), int(y)) for x, y in box]

        points_array = np.array(
            points,
            dtype=np.int32
        )

        # Draw bounding box
        cv2.polylines(
            image_resized,
            [points_array],
            True,
            (0, 255, 0),
            2
        )

        # Draw detected text + confidence on image

        display_text = (
            f"{text} "
            f"({confidence:.2f})"
        )


        cv2.putText(
            image_resized,
            display_text,
            points[0],
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


    # GET FILE NAME WITHOUT EXTENSION
    name = os.path.splitext(filename)[0]

    # SAVE PROCESSED IMAGE

    processed_path = os.path.join(
        processed_folder,
        name + "_processed.png"
    )

    cv2.imwrite(
        processed_path,
        processed
    )


    # SAVE RESULT IMAGE
    result_path = os.path.join(
        result_folder,
        name + "_result.png"
    )


    cv2.imwrite(
        result_path,
        image_resized
    )


    # SAVE OCR TEXT
    #
    # IMPORTANT:
    # ONLY DETECTED TEXT IS SAVED.
    # Confidence is NOT written to the TXT file.

    text_path = os.path.join(

        output_folder,

        name + ".txt"
    )


    with open(
        text_path,
        "w",
        encoding="utf-8"
    ) as file:
        if not result:
            file.write(
                "No text detected.\n"
            )

        else:
            for detection in result:
                # Get ONLY the detected text
                text = detection[1]
                # Write ONLY text
                file.write(
                    text + "\n"
                )


    # SHOW SAVED FILES
    print(
        f"\nProcessed image saved:"
        f"\n{processed_path}"
    )

    print(
        f"Result image saved:"
        f"\n{result_path}"
    )

    print(
        f"Text file saved:"
        f"\n{text_path}"
    )


# FINISHED
print("\n")
print("=" * 70)
print("ALL IMAGES PROCESSED SUCCESSFULLY")
print("=" * 70)