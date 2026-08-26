# Day 23 Smart Object Tracking System

## 📌 Project Overview

The **Smart Object Tracking System** is a computer vision application built with **Python, Ultralytics YOLO, OpenCV, and Gradio**. It detects objects in a video, assigns a unique tracking ID to each object, displays the object's ID and confidence score, counts unique objects, and saves the processed video.

## 🎯 What is Object Tracking?

**Object tracking** is the process of continuously following detected objects across multiple frames of a video.

Instead of detecting an object independently in every frame, a tracking algorithm associates the same object between frames and assigns it a **unique ID**.

For example:

```text
Frame 1 → Person → ID 1
Frame 2 → Person → ID 1
Frame 3 → Person → ID 1
```

The object keeps the same ID as it moves through the video.

## 🔍 Detection vs Tracking

| Object Detection                              | Object Tracking                            |
| --------------------------------------------- | ------------------------------------------ |
| Detects objects in individual frames          | Follows objects across video frames        |
| Identifies object classes                     | Maintains a unique ID for each object      |
| Does not necessarily remember previous frames | Uses information from previous frames      |
| Example: Person, Car, Helmet                  | Example: Person ID 1, Person ID 2          |
| Useful for finding objects                    | Useful for counting and monitoring objects |

### Example

**Detection:**

```text
Frame 1 → Person
Frame 2 → Person
Frame 3 → Person
```

**Tracking:**

```text
Frame 1 → Person ID 1
Frame 2 → Person ID 1
Frame 3 → Person ID 1
```

## 🤖 Tracking Algorithm Used

This project uses **BoT-SORT** through the **Ultralytics YOLO tracking framework**.

BoT-SORT combines object detection with tracking techniques to associate objects between consecutive video frames.

The tracker helps to:

* Assign unique IDs to objects.
* Maintain IDs while objects move.
* Handle multiple objects at the same time.
* Associate detections between consecutive frames.
* Reduce unnecessary ID changes.

The YOLO model is responsible for detecting objects, while **BoT-SORT** helps maintain their identities across frames.

## ⚙️ Main Technologies

* **Python** – Main programming language.
* **Ultralytics YOLO** – Object detection and tracking.
* **BoT-SORT** – Multi-object tracking algorithm.
* **OpenCV** – Video processing and frame manipulation.
* **Gradio** – Web-based user interface.
* **FFmpeg** – Video encoding and output compatibility.

## ✨ Features

* Upload a video through the Gradio interface.
* Select sample videos from the UI.
* Detect objects in the video.
* Track multiple objects.
* Assign unique tracking IDs.
* Display confidence scores.
* Count unique tracked objects.
* Save the processed video.
* Display the processed video in the Gradio interface.

## 🚧 Challenges Faced

### 1. ID Switching

Sometimes the tracker may assign a new ID to an object or switch IDs when objects overlap or temporarily disappear.

**Solution:** Used the BoT-SORT tracking algorithm and appropriate tracking parameters to improve object association.

### 2. Occlusion

When one object moves behind another object, the detector may temporarily fail to detect it.

**Solution:** The tracking algorithm uses information from previous frames to help maintain object identities.

### 3. Similar Objects

When multiple objects have similar appearances and move close to each other, maintaining separate IDs can be difficult.

**Solution:** Multi-object tracking and motion-based association help distinguish between objects.

### 4. Fast Object Movement

Objects moving quickly can cause changes in their position between consecutive frames.

**Solution:** Proper tracker configuration and consistent video processing help improve tracking stability.

### 5. Video Encoding

Processed videos may not play correctly in some browsers when using incompatible codecs.

**Solution:** FFmpeg was used to encode the final video in a browser-compatible format.

## 📊 Tracking Workflow

```text
Input Video
     ↓
Read Video Frames
     ↓
YOLO Object Detection
     ↓
BoT-SORT Tracking
     ↓
Assign Unique Object IDs
     ↓
Display ID + Confidence
     ↓
Count Unique Objects
     ↓
Save Processed Video
     ↓
Display Result in Gradio
```

## 📁 Project Structure

```text
Project/
│
├── app.py
├── tracking.py
├── requirements.txt
├── README.md
│
├── input/
│   └── sample videos
│
└── outputs/
    └── processed videos
```

## 📈 Conclusion

The **Smart Object Tracking System** demonstrates how object detection and multi-object tracking can be combined to analyze video. YOLO detects objects in each frame, while **BoT-SORT maintains object identities across frames**, allowing the system to track and count unique objects effectively.

## 👨‍💻 Author

**Muhammad Ashhad**

