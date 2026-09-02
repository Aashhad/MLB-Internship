# 🎥 Real-Time Video Processing Tool

A Gradio-based Computer Vision application that processes both uploaded videos and live webcam streams using OpenCV. 

## 🚀 Features

- 📁 Upload and process recorded videos
- 📷 Real-time webcam processing
- 🎨 Convert frames to Grayscale
- 🌫️ Apply Gaussian Blur
- 🔍 Detect edges using Canny Edge Detection
- ▶️ Preview the processed video
- 💾 Download the processed output video

---

# 🛠️ Technologies Used

- Python
- OpenCV
- Gradio
- NumPy

---

# 📖 How OpenCV Reads Videos

OpenCV reads videos using the `cv2.VideoCapture()` class.

```python
cap = cv2.VideoCapture("video.mp4")
```

A video is made up of many individual images called **frames**. OpenCV reads one frame at a time using:

```python
ret, frame = cap.read()
```

- `ret` indicates whether the frame was successfully read.
- `frame` contains the current image as a NumPy array.

The application continuously reads frames until the video ends.

---

# 🎞️ What FPS Means

FPS stands for **Frames Per Second**.

It represents the number of frames displayed or processed every second.

For example:

- **30 FPS** means 30 frames are displayed every second.
- Higher FPS produces smoother video playback.
- Lower FPS results in less smooth motion.

The application preserves the original video's FPS while saving the processed output.

---

# 🖥️ Processing Techniques Applied

Each frame goes through the following image processing pipeline:

### 1. Grayscale Conversion

The original color frame is converted to grayscale to simplify image processing.

```python
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```

---

### 2. Gaussian Blur

A Gaussian Blur filter is applied to reduce image noise and smooth the frame before edge detection.

```python
blur = cv2.GaussianBlur(gray, (5,5), 0)
```

---

### 3. Canny Edge Detection

The Canny algorithm detects object boundaries by identifying strong intensity changes.

```python
edges = cv2.Canny(blur, 50, 150)
```

---

# ⚙️ Application Modes

## 📁 Video File Mode

- Upload a recorded video.
- Process every frame.
- Preview the processed result.
- Download the processed video.

## 📷 Live Webcam Mode

- Capture live webcam frames.
- Process each frame in real time.
- Display the processed output instantly.

---

# ⚠️ Challenges Faced

During development, I encountered several challenges:

- Understanding how videos are processed frame by frame instead of all at once.
- Managing the correct frame size and FPS while saving processed videos.
- Ensuring Gaussian Blur uses an odd kernel size.
- Finding a browser-compatible video codec.

Initially, I used the **mp4v** codec, which successfully saved the processed video, but the preview did not work correctly inside the Gradio application because some browsers have limited support for it.

After switching to the **avc1 (H.264)** codec, the processed video preview worked correctly in Gradio and browsers.

---


# 👨‍💻 Author

**Muhammad Ashhad**
