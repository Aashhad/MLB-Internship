# Day-14: Image Processing Toolkit using OpenCV

## 📌 Project Overview

This project is developed as part of the **ML Bench Internship - Day 14 Task**. It demonstrates fundamental image processing techniques using the **OpenCV** library in Python. The toolkit allows users to perform multiple image processing operations on an uploaded image and save the processed output.

A professional **Gradio Web Application** is also included, allowing users to interact with the toolkit through an easy-to-use graphical interface.

---

## 📂 Project Structure

```
Day 14/
│
├── sampleImages/              # Input sample images
├── outputImages/              # Processed images are saved here
├── app.py                     # Gradio Application
├── imageProcessingToolKit.py  # Image Processing Functions
├── openCV.py                  # OpenCV Practice Code
├── README.md                  # Project Documentation
└── requirements.txt           # Required Python Packages
```

---

## 🚀 Features

The toolkit supports the following image processing operations:

- Load an Image
- Display an Image
- Save an Image
- Convert to Grayscale
- Resize Image
- Rotate Image
- Flip Image
- Crop Image
- Blur Image
- Edge Detection (Canny)
- Draw Shapes
- Add Text on Image

---

## 🖥️ Gradio Application

The project includes a professional **Gradio Web Interface** where users can:

- Upload an image
- Select an image processing operation from a dropdown menu
- Preview the processed image
- Download the processed output

---

# Difference Between BGR and RGB

Images are represented using color channels.

### RGB (Red, Green, Blue)

- RGB stores colors in the order:
  - Red
  - Green
  - Blue
- Most image processing libraries such as **Matplotlib**, **PIL**, and web applications use RGB format.

Example:

```
RGB = (255, 0, 0)
```

This represents **Red**.

---

### BGR (Blue, Green, Red)

OpenCV stores images in **BGR** format by default.

Example:

```
BGR = (255, 0, 0)
```

This represents **Blue**, not Red.

Therefore, when displaying OpenCV images using Matplotlib, color conversion is required:

```python
cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
```

---

# What are Grayscale Images?

A grayscale image contains **only intensity values** instead of color information.

- Color images have **3 channels** (BGR/RGB).
- Grayscale images have **1 channel**.

Each pixel stores a value between:

```
0   → Black
255 → White
```

---

## Why are Grayscale Images Used?

Grayscale images are commonly used because they:

- Reduce computational cost
- Require less memory
- Simplify image processing
- Improve the speed of computer vision algorithms
- Are useful for edge detection, thresholding, and object detection

Conversion:

```python
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
```

---

# OpenCV Functions Used

The following OpenCV functions were used during this project:

| Function | Purpose |
|----------|---------|
| `cv2.imread()` | Load an image |
| `cv2.imshow()` | Display an image |
| `cv2.imwrite()` | Save an image |
| `cv2.waitKey()` | Wait for keyboard input |
| `cv2.destroyAllWindows()` | Close image windows |
| `cv2.cvtColor()` | Convert image color space |
| `cv2.resize()` | Resize an image |
| `cv2.rotate()` | Rotate an image |
| `cv2.flip()` | Flip an image |
| `cv2.GaussianBlur()` | Blur an image |
| `cv2.Canny()` | Detect edges |
| `cv2.rectangle()` | Draw rectangles |
| `cv2.circle()` | Draw circles |
| `cv2.line()` | Draw lines |
| `cv2.putText()` | Add text to images |

---

# Challenges Faced

### 1. OpenCV GUI Error

**Problem**

```
cv2.imshow()

The function is not implemented
```

**Solution**

The issue occurred because the installed OpenCV package lacked GUI support. The package was reinstalled with the correct version that supports image display.

---

### 2. Understanding BGR vs RGB

**Problem**

The displayed colors appeared incorrect when using Matplotlib.

**Solution**

Converted images from BGR to RGB using:

```python
cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
```

---

### 3. File Saving

**Problem**

Users needed a simple way to save processed images.

**Solution**

Used:

```python
cv2.imwrite()
```

along with user input to specify the filename and displayed a success message after saving.

---

### 4. Image Loading Errors

**Problem**

Sometimes the image path was incorrect, causing the image to fail loading.

**Solution**

Added validation to check whether the image was successfully loaded before performing any operations.

---

# Technologies Used

- Python
- OpenCV
- NumPy
- Gradio

---


---

# Learning Outcomes

After completing this project, I learned:

- Image loading and saving using OpenCV
- BGR and RGB color formats
- Grayscale image processing
- Image transformations
- Edge detection
- Drawing shapes and adding text
- Building a professional Gradio interface
- Organizing a complete computer vision project

---

## Author

**Ashhad**  
**ML Bench Internship — Day 14**