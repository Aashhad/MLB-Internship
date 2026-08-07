import os
import cv2
import gradio as gr

# Output Folder
OUTPUT_FOLDER = "outputVideos"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def process_video(video_file):

    if video_file is None:
        return None, "Please upload a video."

    # Input Video Path
    video_path = video_file

    # Video Name
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(OUTPUT_FOLDER,f"{video_name}_processed.mp4")

    # Open Video
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return None, "Error opening video."

    # Video Properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Video Writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height),
        False  # grayscale output
    )

    frame_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        # Grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Gaussian Blur
        blur = cv2.GaussianBlur(gray, (5, 5),0)
        # Canny Edge Detection
        edges = cv2.Canny(blur, 100, 200)
        # Save Processed Frame
        out.write(edges)
        frame_count += 1

    cap.release()
    out.release()

    return output_path, (
        f"Processing Completed!\n\n"
        f"Frames Processed: {frame_count}\n"
        f"Saved As: {output_path}"
    )
