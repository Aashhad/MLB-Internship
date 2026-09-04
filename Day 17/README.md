# Shape Detection System using OpenCV 

## 📌 Project Overview

The **Shape Detection System** is a Python application built using **OpenCV** and **Gradio** that detects different geometric shapes in an image. The application can process both **uploaded images** and **preloaded dataset images**, identify the shapes present, draw contours around them, calculate their **area** and **perimeter**, and display the processed image with labels.

---

# Features

- Upload your own image or select an image from the dataset.
- Detect multiple shapes in a single image.
- Draw contours around detected shapes.
- Identify and label each shape.
- Calculate the area of each detected shape.
- Calculate the perimeter of each detected shape.
- Display the final processed image.
- User-friendly Gradio interface.

---

# Technologies Used

- Python
- OpenCV
- NumPy
- Gradio

---

# Project Workflow

1. Load the input image.
2. Convert the image to grayscale.
3. Apply Gaussian Blur to remove noise.
4. Apply Binary Thresholding.
5. Detect contours using OpenCV.
6. Approximate contours into polygons.
7. Identify shapes based on the number of polygon vertices.
8. Calculate contour area and perimeter.
9. Draw contours and shape labels.
10. Display the final output image.

---

# What are Contours?

Contours are the boundaries or outlines of objects in an image. They connect all the continuous points along the edge of an object that have the same intensity or color. In OpenCV, contours are mainly used for object detection, shape recognition, and image analysis.

For example, if an image contains a circle or a rectangle, OpenCV detects the outer boundary of the object as its contour.

---

# How Contour Detection Works

The contour detection process consists of the following steps:

1. Read the input image.
2. Convert the image to grayscale.
3. Apply Gaussian Blur to reduce image noise.
4. Apply Binary Thresholding to separate objects from the background.
5. Use `cv2.findContours()` to detect the object boundaries.
6. Approximate each contour into a polygon using `cv2.approxPolyDP()`.
7. Count the number of vertices of the polygon.
8. Classify the object based on its vertices.
9. Draw the contour and display the detected shape name.

---

# Shapes Detected by the Program

The application can detect the following shapes:

- Triangle
- Square
- Rectangle
- Circle
- Pentagon
- Hexagon

The program determines the shape by counting the number of vertices after polygon approximation. For four-sided shapes, it uses the aspect ratio to distinguish between a square and a rectangle.

---

# Contour Measurements

For every detected shape, the application calculates:

- Contour Area using `cv2.contourArea()`
- Contour Perimeter using `cv2.arcLength()`
- Bounding Rectangle using `cv2.boundingRect()`
- Minimum Enclosing Circle using `cv2.minEnclosingCircle()`

These measurements help analyze the size and geometry of each detected object.

---

# Dataset

The dataset contains 10–15 images with different geometric shapes.

The images include:

- Different colors
- Different sizes
- Different backgrounds
- Single and multiple shapes

The application also allows users to upload their own images for testing.

---

# Challenges Faced

During the development of this project, several challenges were encountered:

- Detecting dark-colored shapes on dark backgrounds.
- Selecting an appropriate threshold value for different images.
- Distinguishing between squares and rectangles accurately.
- Reducing image noise before contour detection.
- Detecting multiple overlapping shapes.
- Handling images with different lighting conditions.
- Choosing the correct approximation accuracy (`epsilon`) for polygon detection.

These challenges were addressed by applying Gaussian Blur, selecting suitable threshold values, filtering small contours, and using aspect ratio calculations for four-sided shapes.

---

# Conclusion

This Shape Detection System successfully detects multiple geometric shapes using OpenCV contour detection techniques. It accurately identifies different shapes, calculates their area and perimeter, and presents the results through an easy-to-use Gradio interface. The project demonstrates practical applications of image processing, contour analysis, and computer vision for object recognition tasks.

---

## Author

**Muhammad Ashhad**
