import os
import cv2
import numpy as np
import gradio as gr
import time
import subprocess
import imageio_ffmpeg

# os.path.join is used so the same code works on Windows and Linux.
SAMPLE_VIDEO = [
    "Day 18/inputVideos/f2.mp4",
    "Day 18/inputVideos/f3.mp4",
    "Day 18/inputVideos/f4.mp4",
    "Day 18/inputVideos/f5.mp4",
    "Day 18/inputVideos/f6.mp4",
    "Day 18/inputVideos/f7.mp4",
]
# Only keep the ones that actually exist, so a missing file doesn't crash the UI
SAMPLE_VIDEO = [p for p in SAMPLE_VIDEO if os.path.exists(p)]

# Processed videos are saved here instead of a temp folder, so they're easy
# to find and don't get wiped by the OS temp-cleanup.
OUTPUT_DIR = os.path.join("Day 18", "outputVideos")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Scratch folder for the intermediate mp4v file before it gets transcoded
TEMP_DIR = os.path.join("Day 18", "_tempRaw")
os.makedirs(TEMP_DIR, exist_ok=True)

DISPLAY_MODES = ["Edges Only", "Grayscale", "Blurred"]

# Path to the ffmpeg binary bundled by imageio-ffmpeg (no system install needed)
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()


# function processing on frame one by one
def process_frame(frame, blur_ksize=5, canny_low=50, canny_high=150, show_mode="Edges Only"):

    # Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gaussian Blur (kernel size must be odd)
    k = int(blur_ksize)
    if k % 2 == 0:
        k += 1
    k = max(1, k)
    blurred = cv2.GaussianBlur(gray, (k, k), 0)

    # Canny Edge Detection
    edges = cv2.Canny(blurred, int(canny_low), int(canny_high))

    if show_mode == "Grayscale":
        out = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    elif show_mode == "Blurred":
        out = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)
    else:  # Edges Only
        out = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    return out


def transcode_to_h264(raw_path, final_path):
    # OpenCV saves a video in a format (mp4v) that browsers can't play. FFmpeg converts it to H.264, which browsers and Gradio can play, without needing you to install FFmpeg manually.

    cmd = [
        FFMPEG_EXE,  # Launches FFmpeg
        "-y",  # overwrite output if it exists
        "-i",  # Specifies the input video
        raw_path,  # Video to convert
        "-c:v",  # Chooses the video encoder
        "libx264",  # Creates browser-compatible video
        "-pix_fmt",  # Defines how color is stored
        "yuv420p",  # widest browser/player compatibility
        "-preset",  # Balances speed vs. compression
        "veryfast",  # Good default for quick encoding
        "-movflags",  # Changes file organization
        "+faststart",  # allows the video to start playing before it's fully downloaded
        final_path,  # Location of the converted video
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise gr.Error(f"Video transcoding failed: {result.stderr[-500:]}")


# Process an uploaded video file
def process_video_file(video_path, blur_ksize, canny_low, canny_high, show_mode, progress=gr.Progress()):
    if video_path is None:
        raise gr.Error("Please upload the video")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise gr.Error("video format is wrong, so that not opened on it")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0

    base_name = f"{os.path.splitext(os.path.basename(video_path))[0]}_{show_mode.replace(' ', '')}_{int(time.time())}"
    raw_path = os.path.join(TEMP_DIR, f"{base_name}_raw.mp4")
    final_path = os.path.join(OUTPUT_DIR, f"{base_name}.mp4")

    # Step 1: write processed frames with OpenCV (mp4v — always works, no codec dependency issues)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(raw_path, fourcc, fps, (width, height))
    if not writer.isOpened():
        raise gr.Error("Could not initialize the video writer on this machine.")

    frame_idx = 0
    while True:
        bool_process, frame = cap.read()
        if not bool_process:
            break
        processed = process_frame(frame, blur_ksize, canny_low, canny_high, show_mode)
        writer.write(processed)
        frame_idx += 1
        if total_frames > 0:
            # Reserve the last 15% of the progress bar for the transcode step below
            progress(0.85 * frame_idx / total_frames, desc=f"Processing frame {frame_idx}/{total_frames}")

    cap.release()
    writer.release()

    # Step 2: transcode to H.264 so it plays in the browser preview
    progress(0.9, desc="Encoding browser-compatible video...")
    transcode_to_h264(raw_path, final_path)

    # Clean up the intermediate raw file — only the final H.264 file is kept
    try:
        os.remove(raw_path)
    except OSError:
        pass

    progress(1.0, desc="Done")
    return final_path, final_path  # preview player, download file


# Live webcam: one frame in, one processed frame out, streaming
def process_webcam_stream(frame, blur_ksize, canny_low, canny_high, show_mode):
    if frame is None:
        return None
    # gr.Image with webcam gives RGB numpy array — convert to BGR for OpenCV
    bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    processed = process_frame(bgr, blur_ksize, canny_low, canny_high, show_mode)
    rgb_out = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
    return rgb_out


# UI
with gr.Blocks(title="Real-Time Video Edge Processor", theme=gr.themes.Soft()) as app:
    gr.Markdown(
        "# 🎥 Real-Time Video Processing Tool\n"
        "This application provides two processing modes:\n\n"
        "📁 **Video File:** Upload a recorded video, process every frame, preview the output, and download the processed video.\n\n"
        "📷 **Live Webcam:** Capture and process your webcam feed in real time with instant visual results.\n\n"
        "**Developed by : MUHAMMAD ASHHAD**"
    )

    with gr.Tab("📁 Video File"):
        with gr.Row():
            with gr.Column():
                video_input = gr.Video(label="Upload Video")
                if SAMPLE_VIDEO:
                    gr.Examples(
                        examples=SAMPLE_VIDEO,
                        inputs=video_input,
                        label="Or try a sample video",
                    )
                blur_1 = gr.Slider(1, 31, value=5, step=2, label="Gaussian Blur Kernel Size")
                low_1 = gr.Slider(0, 255, value=50, step=1, label="Canny Lower Threshold")
                high_1 = gr.Slider(0, 255, value=150, step=1, label="Canny Upper Threshold")
                mode_1 = gr.Radio(
                    DISPLAY_MODES,
                    value="Edges Only",
                    label="Display Mode",
                )
                with gr.Row():
                    run_btn = gr.Button("▶ Process Video", variant="primary")
                    clear_btn_file = gr.ClearButton(value="Clear", variant="secondary")
            with gr.Column():
                video_preview = gr.Video(label="Processed Video (Preview)")
                video_download = gr.File(label="Download Processed Video")

        run_btn.click(
            fn=process_video_file,
            inputs=[video_input, blur_1, low_1, high_1, mode_1],
            outputs=[video_preview, video_download],
        )
        clear_btn_file.add([video_input, video_preview, video_download])

    with gr.Tab("📷 Webcam (Live)"):
        with gr.Row():
            with gr.Column():
                webcam_input = gr.Image(sources=["webcam"], streaming=True, label="Webcam Input")
                blur_2 = gr.Slider(1, 31, value=5, step=2, label="Gaussian Blur Kernel Size")
                low_2 = gr.Slider(0, 255, value=50, step=1, label="Canny Lower Threshold")
                high_2 = gr.Slider(0, 255, value=150, step=1, label="Canny Upper Threshold")
                mode_2 = gr.Radio(
                    DISPLAY_MODES,
                    value="Edges Only",
                    label="Display Mode",
                )
                clear_btn_webcam = gr.ClearButton(value="Clear", variant="secondary")
            with gr.Column():
                webcam_output = gr.Image(label="Processed Output", streaming=True)

        webcam_input.stream(
            fn=process_webcam_stream,
            inputs=[webcam_input, blur_2, low_2, high_2, mode_2],
            outputs=webcam_output,
            time_limit=60,
            stream_every=0.1,
        )
        clear_btn_webcam.add([webcam_input, webcam_output])

if __name__ == "__main__":
    app.launch()