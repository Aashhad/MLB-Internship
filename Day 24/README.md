# 🥤 Cup Detection System

A custom **YOLOv8 object detection system** developed to detect cups in images. The model was trained on a custom dataset and deployed with a **Gradio web application** for testing on both sample images and newly uploaded images.

---

## 📌 Project Overview

The goal of this project was to build a custom object detection model capable of identifying cups in images.

The system can:

* Detect cups in images.
* Draw bounding boxes around detected cups.
* Display confidence scores.
* Count the number of detected cups.
* Test the model on new/unseen images.
* Test using sample images.
* Save prediction results automatically.
* Provide a simple Gradio interface for inference.

---

## 🎯 Object/Class Selected

### Cup

I selected **cup** as the object/class for this project.

The cup class was selected because cups have different shapes, sizes, colors, materials, and orientations. This makes the dataset useful for learning object detection and testing how well the YOLO model generalizes to unseen images.

The dataset contains:

```text
Class 0: cup
```

---

## 📷 Image Collection

The images were collected from different sources and environments to create a diverse dataset.

The dataset includes images containing cups with variations in:

* Size
* Shape
* Color
* Background
* Viewing angle
* Lighting conditions
* Distance from the camera
* Number of cups in an image
* Different types of cups

The purpose of collecting diverse images was to improve the model's ability to detect cups in real-world situations.

---

## 🏷️ Dataset Annotation

The images were manually annotated by drawing **bounding boxes** around each cup.

Each bounding box identifies the location of the cup in the image.

The annotations were created in YOLO-compatible format.

Each annotation contains:

```text
class_id center_x center_y width height
```

The coordinates are normalized between `0` and `1`.

Example:

```text
0 0.512 0.478 0.325 0.614
```

Where:

* `0` = cup class
* `center_x` = horizontal center of the bounding box
* `center_y` = vertical center of the bounding box
* `width` = bounding box width
* `height` = bounding box height

The annotated dataset was exported from **Roboflow in YOLOv8 format**.

---

## 📊 Dataset Split

The dataset was divided into three subsets:

| Dataset    | Purpose                                                        |
| ---------- | -------------------------------------------------------------- |
| Training   | Used to train the YOLO model                                   |
| Validation | Used to monitor and evaluate model performance during training |
| Testing    | Used to evaluate the model on unseen images                    |

The split used was:

```text
Training:   [70%]
Validation: [20%]
Testing:    [10%]
```

> Replace the percentages above with the actual split shown in your Roboflow dataset.

---

## 🔄 Data Augmentation

Data augmentation was applied using **Roboflow** to increase the variety of training examples and improve model generalization.

The augmentations used included:

* Horizontal flipping
* Rotation
* Scaling
* Translation
* Brightness variation
* Saturation variation
* Hue variation

### Why augmentation was used

Augmentation helps the model recognize cups under different real-world conditions.

For example:

* **Rotation** helps detect tilted cups.
* **Scaling** helps detect cups at different distances.
* **Horizontal flipping** helps the model recognize objects from different orientations.
* **Brightness changes** help with different lighting conditions.
* **Hue and saturation changes** help when cup colors or lighting vary.
* **Translation** helps when cups are not centered in the image.

---

## 📈 Original vs Augmented Dataset Size

The original dataset contained:

```text
Original images: [YOUR ORIGINAL IMAGE COUNT]
```

After augmentation:

```text
Augmented images: [YOUR AUGMENTED IMAGE COUNT]
```

### Comparison

| Dataset   | Number of Images |
| --------- | ---------------: |
| Original  |  `157` |
| Augmented |  `471` |

Augmentation increased the number and variety of training examples, helping the model learn more robust visual features.

---

## 🤖 Model Training

The custom object detection model was trained using **YOLOv8** from Ultralytics.

Training was performed using **Google Colab with GPU acceleration**.

### Training Configuration

| Parameter            |               Value |
| -------------------- | ------------------: |
| Model                |             YOLOv8n |
| Epochs               |                 100 |
| Image Size           |           640 × 640 |
| Batch Size           |                  16 |
| Device               |    Google Colab GPU |
| Optimizer            | Ultralytics default |
| Confidence Threshold |                0.25 |

The pretrained `yolov8n.pt` model was used as the starting point for transfer learning.

The best-performing model was saved as:

```text
best.pt
```

---

## 📉 Model Evaluation

The trained model was evaluated using standard object detection metrics:

* Precision
* Recall
* mAP@50
* mAP@50-95

### Final Results

Replace the following values with the actual results from `model.val()`:

| Metric    |  Result |
| --------- | ------: |
| Precision | `0.974` |
| Recall    | `0.986` |
| mAP@50    | `0.993` |
| mAP@50-95 | `0.715` |

### Evaluation Code

```python
from ultralytics import YOLO

model = YOLO("best.pt")

metrics = model.val(
    data="data.yaml",
    imgsz=640,
    device=0
)

print(f"Precision: {metrics.box.mp:.4f}")
print(f"Recall: {metrics.box.mr:.4f}")
print(f"mAP@50: {metrics.box.map50:.4f}")
print(f"mAP@50-95: {metrics.box.map:.4f}")
```

The target for this project was:

```text
mAP@50 ≥ 80%
```

---

## ⚠️ Problems Found in the Dataset

During dataset preparation and model testing, several challenges can occur:

### 1. Different Cup Sizes

Some cups appeared very large while others were small in the image. Small objects can be more difficult for the model to detect.

### 2. Different Backgrounds

Cups appeared against different backgrounds. Complex backgrounds can make object detection more challenging.

### 3. Similar Colors

Some cups had colors similar to their background, which can make the cup less distinguishable.

### 4. Different Lighting Conditions

Images captured under different lighting conditions can change the appearance of cups.

### 5. Occlusion

In some images, cups may be partially hidden behind other objects or other cups.

### 6. Annotation Quality

Incorrect or inconsistent bounding boxes can negatively affect model training. Careful annotation is therefore important.

### 7. Limited Dataset Diversity

If most training images contain similar types of cups or similar environments, the model may not generalize well to completely new environments.

---

## 🚀 Future Dataset Improvements

The dataset can be improved in the future by:

* Collecting more cup images.
* Adding different types and shapes of cups.
* Adding transparent cups.
* Adding cups with different materials.
* Including more indoor and outdoor environments.
* Adding images with different lighting conditions.
* Adding partially occluded cups.
* Adding images containing multiple cups.
* Improving annotation accuracy.
* Removing duplicate or low-quality images.
* Including more difficult negative examples.
* Increasing the number of real-world test images.

A larger and more diverse dataset would help the model generalize better to real-world images.

---

## 🖥️ Gradio Application

After training, the `best.pt` model was integrated into a **Gradio application**.

The application supports two ways of testing:

### 1. Upload New Image

Users can upload any new image directly through the Gradio interface.

### 2. Sample Images

Users can select sample images from:

```text
Day 24/images/input
```

The model then performs inference and displays:

* Bounding boxes
* Cup class
* Confidence scores
* Total number of detected cups

The prediction is automatically saved to:

```text
Day 24/images/output
```

---

## 📁 Project Structure

```text
Day 24/
│
├── model/
│   └── best.pt
│
├── images/
│   ├── input/
│   │   ├── cup1.jpg
│   │   ├── cup2.jpg
│   │   └── cup3.jpg
│   │
│   └── output/
│       ├── cup1_20260828_120000.jpg
│       └── cup2_20260828_120100.jpg
│
├── app.py
│
└── README.md
```

---

## 🛠️ Technologies Used

* Python
* YOLOv8
* Ultralytics
* Roboflow
* Google Colab
* OpenCV
* NumPy
* Pillow
* Gradio

---

## ▶️ How to Run

Install the required libraries:

```bash
pip install ultralytics gradio pillow numpy opencv-python
```

Run the application:

```bash
python app.py
```

The Gradio interface will open in the browser.

---

## 🔍 Detection Workflow

```text
Collect Images
      ↓
Annotate Images
      ↓
Create Dataset
      ↓
Apply Augmentation
      ↓
Export YOLOv8 Dataset
      ↓
Train YOLOv8 Model
      ↓
Evaluate Model
      ↓
Save best.pt
      ↓
Build Gradio Application
      ↓
Upload / Select Image
      ↓
YOLO Detection
      ↓
Bounding Boxes + Confidence
      ↓
Save Prediction
```

---

## ✅ Conclusion

This project demonstrates the complete workflow of a custom object detection system, starting from image collection and annotation through augmentation, YOLOv8 model training, evaluation, and deployment.

The trained model can detect cups in both sample images and new images uploaded through the Gradio application. Future improvements will focus on increasing dataset size and diversity, improving annotation quality, and adding more challenging real-world examples.

## 👨‍💻 Author
## Muhammad Ashhad

