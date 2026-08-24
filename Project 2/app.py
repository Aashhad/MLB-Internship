import gradio as gr
from ultralytics import YOLO
import cv2
from pathlib import Path
import imageio.v2 as imageio
import time


# CONFIGURATION

MODEL_PATH = "Project 2/models/best.pt"
CONFIDENCE_THRESHOLD = 0.25
IMAGE_SIZE = 768

# CPU
DEVICE = "cpu"


# DIRECTORIES
PROJECT_DIR = Path("Project 2")

# Test images will also be used as Gradio samples
TEST_IMAGE_DIR = (PROJECT_DIR / "images" / "testImages")

# Prediction output folders
IMAGE_OUTPUT_DIR = (PROJECT_DIR / "predictions" / "images")

VIDEO_OUTPUT_DIR = (PROJECT_DIR / "predictions" / "videos")


# CREATE OUTPUT DIRECTORIES

IMAGE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# LOAD MODEL

print("=" * 60)
print("LOADING YOLO MODEL")
print("=" * 60)

model = YOLO(MODEL_PATH)

print("Model loaded successfully!")
print("Classes:", model.names)


# FIND SAMPLE IMAGES

IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".JPG",
    ".JPEG",
    ".PNG"
]

sample_images = []

if TEST_IMAGE_DIR.exists():

    for image_file in sorted(
        TEST_IMAGE_DIR.iterdir()
    ):

        if (
            image_file.is_file()
            and image_file.suffix in IMAGE_EXTENSIONS
        ):

            sample_images.append(
                str(image_file)
            )


print(
    f"Found {len(sample_images)} sample images."
)


# IMAGE DETECTION

def detect_image(image, confidence):

    if image is None:

        return (
            None,
            "Please upload an image."
        )


    # RGB → BGR

    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


    # YOLO prediction

    results = model.predict(
        source=image_bgr,
        imgsz=IMAGE_SIZE,
        conf=confidence,
        device=DEVICE,
        verbose=False
    )


    if not results:

        return (
            image,
            "No prediction result."
        )


    result = results[0]


    # Copy image
    annotated_image = image_bgr.copy()


    # Detection information
    detection_text = []


    if (
        result.boxes is not None
        and len(result.boxes) > 0
    ):

        for box in result.boxes:

            # Bounding box

            coordinates = (
                box.xyxy[0]
                .cpu()
                .numpy()
                .astype(int)
            )

            x1, y1, x2, y2 = coordinates


            # Confidence

            score = float(
                box.conf[0]
                .cpu()
                .numpy()
            )


            # Class ID

            class_id = int(
                box.cls[0]
                .cpu()
                .numpy()
            )


            # Class name

            if isinstance(
                model.names,
                dict
            ):

                class_name = model.names.get(
                    class_id,
                    "helmet"
                )

            else:

                if (
                    0 <= class_id
                    < len(model.names)
                ):

                    class_name = (
                        model.names[class_id]
                    )

                else:

                    class_name = "helmet"


            # Draw bounding box
        

            cv2.rectangle(
                annotated_image,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )


            # Label

            label = (
                f"{class_name}: "
                f"{score:.2f}"
            )


            cv2.putText(
                annotated_image,
                label,
                ( x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )


            # Detection result
            detection_text.append(f"Helmet: " f"Confidence = {score:.2%}")


    else:
        detection_text.append("No helmet detected.")


    # SAVE IMAGE

    filename = (f"prediction_" f"{int(time.time() * 1000)}.jpg")

    image_output_path = (IMAGE_OUTPUT_DIR / filename)
    cv2.imwrite(str(image_output_path), annotated_image)
    print("Image saved:", image_output_path)


    # BGR → RGB
    annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
    return (annotated_image, "\n".join(detection_text))


# VIDEO DETECTION

def detect_video(video_path, confidence):

    if video_path is None:

        return None

    print("\n" + "=" * 60)
    print("VIDEO PROCESSING")
    print("=" * 60)


    # Open video

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():

        raise ValueError(
            "Unable to open video."
        )


    # Video properties

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


    if fps <= 0:
        fps = 30.0


    print(f"Resolution: {width} x {height}")
    print(f"FPS: {fps}")


    # Output filename
    timestamp = int(time.time())
    output_filename = (f"processed_video_" f"{timestamp}.mp4")
    output_path = (VIDEO_OUTPUT_DIR / output_filename)

    print("Output video:")
    print(output_path)


    # H.264 writer

    writer = imageio.get_writer(
        str(output_path),
        fps=fps,
        codec="libx264",
        format="FFMPEG",
        pixelformat="yuv420p"
    )

    # Counters
    frame_count = 0
    detection_count = 0


    # Process video
    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1


        # YOLO prediction

        results = model.predict(
            source=frame,
            imgsz=IMAGE_SIZE,
            conf=confidence,
            device=DEVICE,
            verbose=False
        )


        if results:

            result = results[0]

            if (
                result.boxes is not None
                and len(result.boxes) > 0
            ):

                detection_count += (
                    len(result.boxes)
                )


                for box in result.boxes:

                    # Coordinates

                    coordinates = (
                        box.xyxy[0]
                        .cpu()
                        .numpy()
                        .astype(int)
                    )

                    x1, y1, x2, y2 = coordinates


                    # Confidence

                    score = float(
                        box.conf[0]
                        .cpu()
                        .numpy()
                    )


                    # Class ID

                    class_id = int(
                        box.cls[0]
                        .cpu()
                        .numpy()
                    )


                    # Class name

                    if isinstance(
                        model.names,
                        dict
                    ):

                        class_name = (
                            model.names.get(
                                class_id,
                                "helmet"
                            )
                        )

                    else:

                        if (
                            0 <= class_id
                            < len(model.names)
                        ):

                            class_name = (
                                model.names[class_id]
                            )

                        else:

                            class_name = "helmet"


                    # Bounding box

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )


                    # Label

                    label = (f"{class_name}: " f"{score:.2f}")

                    cv2.putText(
                        frame,
                        label,
                        (x1, max(y1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2
                    )


        # BGR → RGB

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


        # Save frame

        writer.append_data(frame_rgb)


        # Progress

        if frame_count % 30 == 0:

            print(
                f"Processed frames: "
                f"{frame_count}",
                end="\r"
            )


    # Release

    cap.release()
    writer.close()
    print("\n")


    # Check output

    if output_path.exists():

        file_size = (output_path.stat().st_size / (1024 * 1024))
        print("Video processing completed!")
        print(f"Frames processed: " f"{frame_count}")
        print(f"Helmet detections: " f"{detection_count}")
        print("Video saved to:")
        print(output_path)
        print(f"File size: " f"{file_size:.2f} MB")

    else:
        print("ERROR: Output video was not created.")

    return str(output_path)


# GRADIO INTERFACE

with gr.Blocks(
    title="Helmet Detection System"
) as demo:


    # HEADER

    gr.Markdown(
        """
        # 🪖 Custom Helmet Detection System

        Detect **helmets only** using a custom-trained YOLO model.

        ### Features

        - 🖼️ Image Detection
        - 🎥 Video Detection
        - 📊 Confidence Scores
        - 💾 Save Prediction Results
        - 📥 Download Processed Results

        **Model:** Custom YOLO  
        **Object:** Helmet  
        **Device:** CPU
        """
    )


    # IMAGE TAB

    with gr.Tab("🖼️ Image Detection"):

        image_input = gr.Image(
            type="numpy",
            label="Upload Image"
        )


        # SAMPLE IMAGES

        if sample_images:
            gr.Examples(
                examples=[
                    [image]
                    for image in sample_images
                ],
                inputs=image_input,
                label="📷 Sample Test Images",
                examples_per_page=15

            )

        else:

            gr.Markdown(
                f"""
                ⚠️ No sample images found.

                Put your test images inside:

                `{TEST_IMAGE_DIR}`
                """
            )


        # Confidence

        confidence_slider = gr.Slider(
            minimum=0.1,
            maximum=0.9,
            value=0.25,
            step=0.05,
            label="Confidence Threshold"
        )


        # Button

        image_button = gr.Button(
            "🔍 Detect Helmet",
            variant="primary"
        )


        # Output image
        image_output = gr.Image(label="Detection Result")


        # Detection information

        detection_output = gr.Textbox(
            label="Detection Results",
            lines=15
        )


        # Button event

        image_button.click(

            fn=detect_image,

            inputs=[
                image_input,
                confidence_slider
            ],

            outputs=[
                image_output,
                detection_output
            ]
        )


    # ========================================================
    # VIDEO TAB
    # ========================================================

    with gr.Tab("🎥 Video Detection"):


        video_input = gr.Video(

            label="Upload Video"
        )


        # ----------------------------------------------------
        # Confidence
        # ----------------------------------------------------

        video_confidence = gr.Slider(
            minimum=0.1,
            maximum=0.9,
            value=0.25,
            step=0.05,
            label="Confidence Threshold"
        )


        # Button

        video_button = gr.Button(
            "🎥 Detect Helmets in Video",
            variant="primary"
        )


        # Output
    

        video_output = gr.Video(
            label="Processed Video",
            format="mp4"
        )


        # Button event

        video_button.click(
            fn=detect_video,
            inputs=[video_input, video_confidence],
            outputs=video_output
        )


# LAUNCH

if __name__ == "__main__":

    print("\n")

    print("=" * 60)
    print("STARTING GRADIO APPLICATION")
    print("=" * 60)

    print("\nTest images:")
    print(TEST_IMAGE_DIR)
    print("\nImage output:")
    print(IMAGE_OUTPUT_DIR)
    print("\nVideo output:")
    print(VIDEO_OUTPUT_DIR)

    demo.launch()