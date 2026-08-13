# 🅿️ Smart Parking Lot Occupancy Analyzer

A Computer Vision-based parking occupancy detection system developed using **Python**, **OpenCV**, and **Gradio**. The application automatically determines whether parking spaces are **Occupied** or **Vacant** by analyzing aerial parking lot images using image processing techniques and manually annotated parking slots.

---

## 📌 Project Overview

This project analyzes parking lot images captured from a fixed overhead camera and identifies the occupancy status of each predefined parking space.

The system provides:

- 🅿️ Automatic parking occupancy detection
- 📊 Total parking slot count
- 🔴 Occupied parking slot count
- 🟢 Vacant parking slot count
- 📈 Parking occupancy percentage
- 🖼️ Visualized detection results
- 🎛️ Interactive Gradio-based user interface

Parking slots are manually annotated once using a polygon-based annotation tool. The saved annotations are then reused to analyze any parking image captured from the same camera viewpoint.

---

## 🔄 How It Works

```text
Parking Lot Image
        ↓
Load Parking Slot Annotations
        ↓
Image Preprocessing
        ↓
Parking Slot Extraction
        ↓
Edge Density Calculation
        ↓
Threshold Comparison
        ↓
Occupied / Vacant Classification
        ↓
Visualization & Statistics
```

---

## 1️⃣ Parking Slot Annotation

Before running occupancy detection, parking spaces are manually annotated.

Each parking slot is marked by selecting its four corner points.

The annotations are saved in:

```text
annotation/parking_slots.json
```

These annotations are loaded automatically during parking occupancy analysis.

---

## 2️⃣ Image Processing

Each parking image is processed using OpenCV techniques including:

- Grayscale Conversion
- Gaussian Blur
- Edge Detection
- Polygon Mask Generation
- Edge Density Calculation

These operations help determine whether a parking space contains a vehicle.

---

## 3️⃣ Occupancy Detection

For every parking slot, the system calculates the percentage of edge pixels inside the parking region.

```text
Edge Density =
Edge Pixels Inside Slot
-----------------------
Total Pixels Inside Slot
```

If the calculated density is greater than the selected threshold, the parking slot is marked as:

- 🔴 Occupied

Otherwise it is marked as:

- 🟢 Vacant

The occupancy threshold can also be adjusted interactively in the Gradio interface.

---

## 4️⃣ Visualization

After processing, the application draws colored parking slot boundaries directly on the image.

### Color Representation

- 🔴 Red → Occupied Parking Slot
- 🟢 Green → Vacant Parking Slot

The application also displays:

- Total Parking Slots
- Occupied Slots
- Vacant Slots
- Occupancy Percentage
- Occupied Slot IDs
- Vacant Slot IDs

---

## 🖥️ Gradio User Interface

The project includes a modern Gradio interface that allows users to:

- 📷 Select a parking image from the built-in image gallery
- 📤 Upload a custom parking image
- 🎚️ Adjust the occupancy threshold
- 🔍 Run parking occupancy analysis
- 📊 View parking statistics
- 🖼️ Display annotated parking results

---

## 🛠️ Technologies Used

- **Python**
- **OpenCV**
- **NumPy**
- **Gradio**
- **JSON**
- **Computer Vision**
- **Image Processing**

---

## 📂 Project Structure

```text
Smart Parking Lot Occupancy Analyzer/
│
├── dataset/
│   ├── inputImages/
│   │   └── images/
│   └── outputImages/
│
├── annotation/
│   └── parking_slots.json
│
├── src/
│   ├── __init__.py
│   ├── slotDetection.py
│   ├── occupancyDecision.py
│   ├── visualization.py
│   ├── preprocessing.py
│    └── createSlots.py
│
├── main.py
├── app.py
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Create Parking Slot Annotations

Run:

```bash
python createSlots.py
```

Select the four corner points of every parking space and save the annotations.

---

### 3. Run Parking Occupancy Detection

Place parking lot images inside:

```text
dataset/inputImages/images/
```

Run:

```bash
python main.py
```

Processed images and summaries will be saved in:

```text
dataset/outputImages/
```

---

### 4. Run the Gradio Application

Launch the interactive interface:

```bash
python app.py
```

The application allows you to:

- 📷 Select sample parking images
- 📤 Upload your own image
- 🎚️ Adjust occupancy threshold
- 🔍 Analyze parking occupancy
- 📊 View occupancy statistics
- 🖼️ Display annotated parking results

---

## 📊 Dataset

This project uses aerial parking lot images for parking occupancy analysis.

Images are captured from a fixed overhead camera viewpoint, allowing the annotated parking slots to remain consistent across different images.

The sample images are stored inside:

```text
dataset/inputImages/
```

---

## 📈 Output

For every analyzed image, the system generates:

- Annotated parking image
- Occupancy statistics
- Total parking slots
- Occupied parking slots
- Vacant parking slots
- Occupancy percentage
- Occupied slot IDs
- Vacant slot IDs

Output files are saved in:

```text
dataset/outputImages/
```

---

## ⚠️ Limitations

The current approach is based on edge-density analysis and assumes a fixed camera viewpoint.

Performance may decrease due to:

- Different camera angles
- Heavy shadows
- Poor lighting
- Rain or weather conditions
- Occluded vehicles
- Incorrect parking slot annotations

The parking slot annotations must correspond to the same camera view used during analysis.

---

## 🔮 Future Improvements

- 🚗 YOLO-based vehicle detection
- 🎥 Live CCTV camera support
- 📹 Video-based parking analysis
- 🤖 Deep Learning-based occupancy classification
- 📊 Performance evaluation using Accuracy, Precision, Recall, and F1-Score
- ☁️ Cloud deployment
- 📱 Mobile-friendly interface
- 🌙 Improved robustness under varying weather and lighting conditions

---

## 👨‍💻 Project Goal

The objective of this project is to build a practical **Computer Vision-based Smart Parking Lot Occupancy Analyzer** using traditional image processing techniques.

The system demonstrates how OpenCV can be used to detect parking occupancy efficiently from aerial images while providing an intuitive Gradio interface for real-time analysis and visualization.

# 👨‍💻 Author

**Muhammad Ashhad**
