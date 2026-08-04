# 📄 Day 16 - Document Boundary Detection Tool

## Overview

This project is a Document Boundary Detection Tool built using **Python**, **OpenCV**, and **Gradio**. It detects the boundary of a document by applying image preprocessing, edge detection, morphological operations, and contour detection. The application allows users to upload document images, choose different edge detection and morphology techniques, and visualize the detected document boundary.

---

## Difference Between Sobel, Laplacian, and Canny

### Sobel Operator
- Detects edges by calculating image gradients in the horizontal and vertical directions.
- Provides information about the edge direction.
- More sensitive to noise than Canny.
- Suitable for highlighting gradual intensity changes.

### Laplacian Operator
- Detects edges by calculating the second derivative of the image.
- Finds edges in all directions without considering orientation.
- Highly sensitive to image noise, so Gaussian Blur is usually applied before using it.
- Best for detecting fine details.

### Canny Edge Detection
- A multi-stage edge detection algorithm.
- Includes Gaussian Blur, gradient calculation, non-maximum suppression, and hysteresis thresholding.
- Produces thin, clean, and continuous edges.
- More accurate and robust than Sobel and Laplacian for document detection.

---

## Purpose of Each Morphological Operation

### Erosion
- Removes small white noise.
- Shrinks white regions and separates connected objects.

### Dilation
- Expands white regions.
- Restores object size after erosion and fills small gaps.

### Opening
- Performs erosion followed by dilation.
- Removes small noise while preserving the main object shape.

### Closing
- Performs dilation followed by erosion.
- Fills small holes and connects broken edges in the document boundary.

### Morphological Gradient
- Calculates the difference between dilation and erosion.
- Highlights the outline of objects.

### Top Hat
- Computes the difference between the original image and its opening.
- Highlights small bright regions in the image.

### Black Hat
- Computes the difference between the closing result and the original image.
- Highlights small dark regions and shadows.

---

## Best Combination of Techniques

After testing multiple combinations, the following pipeline produced the most accurate document boundary detection:

- Convert image to Grayscale
- Apply Gaussian Blur
- Use **Canny Edge Detection**
- Apply **Closing Morphological Operation**
- Detect the largest contour
- Approximate the contour using Polygon Approximation
- Draw the detected boundary on the original image

This combination worked best because:
- Gaussian Blur reduced image noise.
- Canny produced clear and continuous edges.
- Closing filled small gaps in document boundaries.
- Contour approximation accurately detected the document corners.

---

## Challenges Faced During Document Boundary Detection

During implementation, several challenges were encountered:

- Documents with shadows sometimes caused the shadow to be detected instead of the document.
- Uneven lighting reduced edge quality in some images.
- Blurred images produced weak edges, making contour detection difficult.
- Selecting appropriate Canny threshold values required experimentation.
- Different morphological operations performed differently depending on the image quality.
- Some images contained multiple large contours, making it necessary to detect the largest valid document contour.

These challenges were reduced by applying Gaussian Blur, using suitable Canny thresholds, and selecting the largest quadrilateral contour after morphological processing.

---

## Technologies Used

- Python
- OpenCV
- NumPy
- Gradio

---

## Project Workflow

1. Upload a document image.
2. Convert the image to grayscale.
3. Apply Gaussian Blur.
4. Perform edge detection (Canny, Sobel, or Laplacian).
5. Apply the selected morphological operation.
6. Detect the largest document contour.
7. Draw the detected boundary.
8. Display and save the final output image.

---

## Author

**Muhammad Ashhad**