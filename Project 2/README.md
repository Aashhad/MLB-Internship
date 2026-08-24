# Custom Helmet Detection System

## 📌 Project Overview

This project implements a **custom object detection system using YOLO** for detecting helmets and identifying whether a person is wearing a helmet.

The model was trained using a custom **Helmet Detection dataset from Roboflow Universe**. The trained `best.pt` model is used for model evaluation, image inference, confidence-score visualization, and saving prediction results.

The application provides an interactive **Gradio interface** for detecting objects in images and videos.

### Main Features

* Train a custom YOLO object detection model.
* Evaluate the trained model.
* Run inference on test images.
* Detect helmets and people without helmets.
* Display bounding boxes.
* Display confidence scores.
* Save prediction results.
* Process images and videos.
* Provide an interactive Gradio web interface.

---

## 📂 Dataset

### Selected Dataset

**Helmet Detection Dataset from Roboflow Universe**

The Helmet Detection dataset was selected because helmet detection is an important real-world computer vision application for **workplace safety, construction sites, factories, and road safety**.

The dataset contains annotated images that can be used to train a custom YOLO object detection model.

### Why This Dataset?

I selected this dataset because:

* It is directly related to real-world safety applications.
* It contains labeled images suitable for object detection.
* The dataset is compatible with the YOLO format.
* It contains bounding-box annotations.
* It provides examples of people with helmets and without helmets.
* Helmet detection is a practical computer vision problem with real-world applications.

---

## 🤖 Model

The project uses a **custom-trained YOLO model**.

The final trained model is:

```text
models/best.pt
```

The model was trained to detect two classes:

```text
0: helmet
1: without helmet
```

The trained `best.pt` file contains the weights of the best-performing model obtained during training.

---

## ⚙️ Training Configuration

The model was trained using **Google Colab** with the Ultralytics YOLO framework.

| Parameter            |            Value |
| -------------------- | ---------------: |
| Model                |             YOLO |
| Dataset              | Helmet Detection |
| Epochs               |          **100** |
| Batch Size           |           **16** |
| Image Size           |    **640 × 640** |
| Device               | Google Colab GPU |
| Confidence Threshold |         **0.25** |
| Output Model         |        `best.pt` |

### Training Configuration

The model was trained for **100 epochs** to allow it enough time to learn the visual features of helmets and people without helmets.

Example training configuration:

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data="dataset/data.yaml",
    epochs=100,
    batch=16,
    imgsz=640,
    device=0
)
```

---

## 📊 Final Evaluation Metrics

The trained model was evaluated on the validation dataset.

### Overall Results

| Metric    |            Result |
| --------- | ----------------: |
| Precision | **0.861 (86.1%)** |
| Recall    | **0.818 (81.8%)** |
| mAP@50    | **0.870 (87.0%)** |
| mAP@50-95 | **0.537 (53.7%)** |

### Class-wise Results

| Class          | Precision |    Recall |    mAP@50 | mAP@50-95 |
| -------------- | --------: | --------: | --------: | --------: |
| Helmet         | **86.8%** | **82.9%** | **88.8%** | **61.5%** |
| Without Helmet | **85.5%** | **80.6%** | **85.3%** | **45.9%** |
| **Overall**    | **86.1%** | **81.8%** | **87.0%** | **53.7%** |

### Performance Target

The project required:

```text
mAP@50 ≥ 80%
```

The final model achieved:

```text
mAP@50 = 87.0%
```

Therefore, the model **successfully exceeded the required performance target** by approximately **7 percentage points**.

The model achieved particularly strong performance for the `helmet` class, with:

```text
Helmet mAP@50 = 88.8%
```

---

## 🔍 Model Inference

After training and evaluation, the trained `best.pt` model was used to perform inference on test images.

The system detects:

* `helmet`
* `without helmet`

For every detected object, the application displays:

* Bounding box
* Class name
* Confidence score

Example:

```text
helmet: 0.94
without helmet: 0.87
```

A confidence score of `0.94` means the model is approximately **94% confident** in that detection.

---

## 💻 Gradio Application

A **Gradio-based web application** was developed to make the trained YOLO model easy to use.

### Image Detection

The user can:

1. Upload an image.
2. Select a confidence threshold.
3. Run object detection.
4. View the annotated image.
5. View detected classes and confidence scores.

### Video Detection

The user can:

1. Upload a video.
2. Select the confidence threshold.
3. Process the video using YOLO.
4. View the detected objects in the output video.
5. Save the processed video.

---

## 📁 Project Structure

```text
Project 2/
│
├── models/
│   └── best.pt
│
│
├── test_images/
│   ├── test1.jpg
│   ├── test2.jpg
│   └── test3.jpg
│
├── predictions/
│   ├── images/
│   └── videos/
│
│
├── test_model.py
├── predict.py
├── app.py
├── requirements.txt
└── README.md
```

---

## 🛠️ Technologies Used

* **Python**
* **YOLO**
* **Ultralytics**
* **OpenCV**
* **NumPy**
* **Gradio**
* **Google Colab**
* **Roboflow**

---

## ⚠️ Challenges Faced

### 1. Dataset Preparation

Preparing the dataset and ensuring that the images and YOLO annotation files were correctly organized was an important step.

The dataset needed to follow the YOLO structure containing:

```text
images/
labels/
```

The `data.yaml` file was also required to correctly define the training, validation, and test datasets.

---

### 2. Model Accuracy

Object detection performance can be affected by different image conditions.

Some challenges included:

* Small objects.
* Different viewing angles.
* Partially visible helmets.
* Multiple people in an image.
* Complex backgrounds.
* Different lighting conditions.
* Similar-looking objects.

Training the model for **100 epochs** helped it learn better features from the dataset.

---

### 3. Detecting Two Different Classes

The model needed to distinguish between:

```text
helmet
without helmet
```

This can be challenging when helmets are small or partially hidden.

The final results show that the model achieved:

```text
Helmet mAP@50        = 88.8%
Without Helmet mAP@50 = 85.3%
```

which indicates that the model learned both classes effectively.

---

### 4. Confidence Threshold

The confidence threshold affects the number of detections produced by the model.

A low threshold can result in more detections but may also produce false positives.

The project uses:

```python
CONFIDENCE_THRESHOLD = 0.25
```

The Gradio application also allows the user to adjust the confidence threshold.

---

### 5. Local CPU Inference

The model was trained using a GPU in Google Colab, while local inference was performed on a computer without an NVIDIA GPU.

Therefore, CPU inference was used:

```python
DEVICE = "cpu"
```

Although CPU inference works successfully, it is slower than GPU inference.

---

## 🚀 Model Improvements

Several approaches were considered to improve model performance:

* Increasing the number of training epochs.
* Adjusting batch size.
* Using an appropriate image size.
* Improving dataset annotations.
* Adding more diverse training images.
* Removing incorrect annotations.
* Using data augmentation.
* Adjusting the confidence threshold.
* Testing different YOLO model configurations.

Increasing the training duration to **100 epochs** helped improve the model's ability to learn the dataset.

The final **mAP@50 of 87.0%** demonstrates that the model successfully achieved the required performance target.

---

## ▶️ How to Run the Project

### Step 1 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2 — Verify the Model

```bash
python test_model.py
```


### Step 3 — Add Test Images

Place test images inside:

```text
test_images/
```

### Step 4 — Run Predictions

```bash
python predict.py
```

The prediction results will be saved inside:

```text
predictions/
```

### Step 5 — Launch the Gradio Application

```bash
python app.py
```

Then open the local Gradio URL displayed in the terminal.

---

## 📈 Final Results

The final custom YOLO model achieved:

```text
Precision      : 86.1%
Recall         : 81.8%
mAP@50         : 87.0%
mAP@50-95      : 53.7%
```

The most important project target was:

```text
mAP@50 ≥ 80%
```

The achieved result was:

```text
87.0%
```

Therefore, the model **successfully achieved and exceeded the required performance target**.

---

## 🎯 Conclusion

This project demonstrates the complete workflow of a **custom YOLO object detection system**, from dataset selection and model training to evaluation and real-world inference.

The Helmet Detection model successfully identifies both **helmets** and **people without helmets** in images and videos while displaying bounding boxes and confidence scores.

With an overall **mAP@50 of 87.0%**, the model exceeded the required target of 80%.

The project provided practical experience with:

* Custom YOLO training
* Roboflow datasets
* Google Colab
* Object detection
* Model evaluation
* Precision and recall
* mAP@50
* OpenCV
* Video processing
* Gradio application development

---

## 👨‍💻 Author

**Muhammad Ashhad**


### Project

**Custom Helmet Object Detection System**
