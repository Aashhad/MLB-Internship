# Day-13: Object Detection using YOLO11

## Project Overview

This project demonstrates **Object Detection using the pre-trained YOLO11 model** from the **Ultralytics** library.

For this mini project, I used a **public Vehicle Detection Dataset in YOLO format**. The project focuses on performing object detection using a pre-trained YOLO11 model without training a custom model.

The model was used to detect different objects such as **cars, buses, trucks, motorcycles, bicycles, trains, and other objects** in sample images. The detection results were visualized using bounding boxes, class labels, and confidence scores.

A simple **Gradio application** was also developed to allow users to upload an image and view the detected objects with bounding boxes.

---

## What is Object Detection?

**Object Detection** is a Computer Vision task that identifies and locates one or more objects within an image.

Unlike simple image classification, object detection provides:

- The **class/category** of each detected object.
- The **location** of each object using a bounding box.
- The **confidence score** indicating how confident the model is about the prediction.

For example, if an image contains a car and a bus, an object detection model can identify both objects and draw separate bounding boxes around them.

---

## How is it different from Image Classification?

**Image Classification** predicts the category or class of an entire image. It does not identify the exact location of objects inside the image.

For example:

> Input Image → "Car"

The model only predicts that the image contains a car.

**Object Detection**, on the other hand, can detect multiple objects in the same image and identify their locations.

For example:

> Input Image → Car + Bus + Truck

The model detects each object separately and draws a bounding box around each detected object.

| Image Classification | Object Detection |
|----------------------|------------------|
| Classifies the entire image | Detects individual objects |
| Usually provides one or more class labels | Provides class labels for each object |
| Does not show object location | Shows object location using bounding boxes |
| Example: "This is a car" | Example: "Car at this location" |

---

## What is YOLO?

**YOLO** stands for **You Only Look Once**.

YOLO is a popular and efficient real-time object detection algorithm. It processes an image in a single forward pass through the neural network and predicts:

- Object classes
- Bounding boxes
- Confidence scores

YOLO is widely used because of its combination of **speed and accuracy**.

It can be used in many real-world applications, including:

- Vehicle detection
- Traffic monitoring
- Autonomous driving
- Surveillance systems
- Robotics
- Pedestrian detection
- Industrial inspection

In this project, I used the **pre-trained YOLO11 model** from the **Ultralytics** library to perform object detection.

---

## Which YOLO Model Did You Use?

I used the **YOLO11 pre-trained model** provided by the **Ultralytics** library.

The model was loaded and used for inference on sample images without performing any additional training.

The purpose of this project was to understand how a pre-trained YOLO model performs object detection and how its predictions can be interpreted and visualized.

---

## Which Dataset Did You Use?

I used a **public Vehicle Detection Dataset** downloaded in **YOLO format**.

The dataset contains images of different types of vehicles and road-related objects.

For this project, sample images were selected and used for inference with the pre-trained YOLO11 model.

The project also contains separate folders for the original input images and the generated detection results.

---

## What Objects Were Detected?

The YOLO11 model was used to detect different objects present in the input images.

The sample detection results include objects such as:

- Car
- Bus
- Truck
- Bicycle
- Motorcycle
- Train
- Person
- Other COCO-supported objects

The exact objects detected depend on the content of each input image and the predictions made by the pre-trained YOLO11 model.

---

## Understanding YOLO Detection Results

Each detection result contains important information about the detected object.

### 1. Bounding Box

A **bounding box** is drawn around the detected object to show its location in the image.

The bounding box is generally represented using coordinates such as:

- `x1`
- `y1`
- `x2`
- `y2`

These coordinates define the top-left and bottom-right corners of the detected object.

### 2. Class Label

The **class label** identifies what object the model detected.

Examples include:

- Car
- Bus
- Truck
- Motorcycle
- Bicycle

### 3. Confidence Score

The **confidence score** represents how confident the model is about its prediction.

For example:

> Car 0.92

This means the model is approximately **92% confident** that the detected object is a car.

Higher confidence scores generally indicate that the model is more confident in its prediction.

---

## Observations About the Detection Results

After running inference using the pre-trained YOLO11 model, the following observations were made:

- The model successfully detected several vehicles and objects in the sample images.
- Large and clearly visible objects were generally detected with higher confidence scores.
- Objects that were small, partially hidden, or far away sometimes received lower confidence scores.
- The model was able to detect multiple objects in a single image.
- Bounding boxes clearly showed the location of detected objects.
- Class labels helped identify the type of each detected object.
- Confidence scores provided an indication of the reliability of each prediction.
- Since the pre-trained YOLO11 model supports common object classes, it was able to perform inference without requiring additional training.
- The detection results demonstrate that YOLO can perform fast and effective object detection.
- The quality of detection depends on factors such as object size, image quality, lighting, and how clearly the object is visible.

---

## Input Images

The project contains sample input images in the `images` and `sample_images` folders.

### `images/`

The `images` folder contains example images used for testing object detection.

It includes:

- `cat.jpg`
- `dog.jpg`
- `street.jpg`

These images were used to observe how the YOLO11 model performs detection on different types of images.

### `sample_images/`

The `sample_images` folder contains vehicle-related images used for object detection.

It includes:

- `bus.jpg`
- `car.jpg`
- `cycle.jpg`
- `motorcycle.jpg`
- `train.jpg`
- `truck.jpg`

These images were used as sample inputs for the YOLO11 detection process.

---

## Output Images

The detection results generated by YOLO11 are saved in the `outputs` folder.

The output images contain bounding boxes and labels around the objects detected by the model.

The output folder includes files such as:

- `_grid_preview.png`
- `cat_result.jpg`
- `detected_bus.jpg`
- `detected_car.jpg`
- `detected_cycle.jpg`
- `detected_motorcycle.jpg`
- `detected_train.jpg`
- `detected_truck.jpg`
- `dog_result.jpg`
- `street_result.jpg`

These output images allow the detection results to be visually inspected and analyzed.

---

## How My Object Detection Script Works

The `objectDetectionYOLO.py` script performs object detection using the pre-trained YOLO11 model.

The basic workflow is:

1. Import the required Python libraries.
2. Load the pre-trained YOLO11 model.
3. Read the input images.
4. Pass the images to the YOLO11 model.
5. Perform object detection.
6. Extract the detected classes, bounding boxes, and confidence scores.
7. Display or print the detection results.
8. Draw bounding boxes and labels on the detected objects.
9. Save the resulting images to the `outputs` folder.

This script demonstrates the basic YOLO object detection workflow.

---

## How My Vehicle Detection Script Works

The `vehicleDetection.py` script focuses on performing object detection on vehicle-related sample images.

The script uses the pre-trained YOLO11 model to analyze images containing vehicles and detect objects such as:

- Cars
- Buses
- Trucks
- Motorcycles
- Bicycles
- Trains

The detection results are saved as output images with bounding boxes and labels.

This makes it easier to visually analyze the model's predictions.

---

## How My Gradio App Works

The project also includes a simple **Gradio application** in `app.py`.

The application provides an interactive interface for performing object detection.

The workflow of the Gradio application is:

1. The user opens the Gradio application.
2. The user uploads an image through the interface.
3. The uploaded image is passed to the pre-trained YOLO11 model.
4. The model performs object detection on the image.
5. The detected objects are identified using class labels.
6. Bounding boxes are drawn around the detected objects.
7. The output image containing the detection results is displayed to the user.
8. A status message provides information about the detected objects.
9. The user can upload another image and perform another prediction.

The Gradio app provides a simple and user-friendly way to interact with the YOLO11 object detection model.

---

## Technologies Used

- **Python**
- **Ultralytics**
- **YOLO8**
- **Gradio**
- **NumPy**
- **OpenCV**
- **Matplotlib**

---

# 📂 Project Structure

The project is organized as follows:

```text
Day 13/
│
├── images/
│   ├── cat.jpg
│   ├── dog.jpg
│   └── street.jpg
│
├── outputs/
│   ├── _grid_preview.png
│   ├── cat_result.jpg
│   ├── detected_bus.jpg
│   ├── detected_car.jpg
│   ├── detected_cycle.jpg
│   ├── detected_motorcycle.jpg
│   ├── detected_train.jpg
│   ├── detected_truck.jpg
│   ├── dog_result.jpg
│   └── street_result.jpg
│
├── sample_images/
│   ├── bus.jpg
│   ├── car.jpg
│   ├── cycle.jpg
│   ├── motorcycle.jpg
│   ├── train.jpg
│   └── truck.jpg
│
├── app.py
├── objectDetectionYOLO.py
└── vehicleDetection.py

👨‍💻 Author
Muhammad Ashhad
