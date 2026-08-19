# Day 22 Document & Object Segmentation Tool

## 📌 Project Overview

This mini project is a **Document & Object Segmentation Tool** built using **Python, OpenCV, NumPy, and Gradio**.

The application accepts an input image and applies different thresholding techniques to separate the main foreground object or document from its background.

The implemented methods are:

* Binary Thresholding
* Adaptive Thresholding
* Otsu Thresholding
* Foreground/Background Segmentation
* Morphological Cleaning
* Main Object Detection 
* Transparent Background Extraction

The application also provides a Gradio interface where users can upload an image or select sample images and view the results of different segmentation methods.

---

## 🎯 Objectives

The main objectives of this project are:

* Read and process an input image.
* Convert the image to grayscale.
* Apply different thresholding techniques.
* Compare Binary, Adaptive, and Otsu Thresholding.
* Create a foreground mask.
* Extract the main object/document.
* Remove the background.
* Save the best segmentation result.
* Provide an easy-to-use Gradio interface.

---

# 🖼️ What is Image Segmentation?

**Image segmentation** is the process of dividing an image into meaningful regions or separating the important parts of an image from its background.

In this project, segmentation is used to identify the **main foreground object or document** and separate it from the background.

A simple segmentation workflow is:

```text
Input Image
     ↓
Grayscale
     ↓
Thresholding
     ↓
Binary Mask
     ↓
Noise Removal
     ↓
Main Object Detection
     ↓
Foreground Extraction
     ↓
Background Removal
```

The resulting mask contains two main regions:

```text
255 → Foreground
0   → Background
```

The foreground mask is then used to extract the main object from the original image.

---

# 🔍 Thresholding Methods

This project uses three different thresholding techniques.

## 1. Binary Thresholding

Binary thresholding uses a **fixed threshold value**.

For example, if the threshold is `127`:

```text
Pixel > 127  → 255 (White)
Pixel ≤ 127  → 0   (Black)
```

OpenCV implementation:

```python
_, binary = cv2.threshold(
    gray,
    127,
    255,
    cv2.THRESH_BINARY
)
```

### Advantages

* Simple and fast.
* Easy to understand.
* Works well when the image has good lighting.
* Useful when foreground and background have clearly different intensity values.

### Limitations

* Uses one global threshold.
* Can perform poorly with uneven lighting.
* The correct threshold may need to be selected manually.

---

## 2. Adaptive Thresholding

Adaptive thresholding calculates a **different threshold for different regions** of an image.

This makes it more suitable for images with uneven illumination.

OpenCV implementation:

```python
adaptive = cv2.adaptiveThreshold(
    gray,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11,
    2
)
```

Important parameters include:

* **Block Size:** Determines the local neighborhood used to calculate the threshold.
* **C:** A constant subtracted from the calculated threshold.
* **GAUSSIAN_C:** Uses a Gaussian-weighted neighborhood.

### Advantages

* Handles uneven lighting better.
* Useful for documents and text.
* Calculates thresholds locally.
* Often produces better results when different parts of an image have different brightness.

### Limitations

* More computationally expensive than simple binary thresholding.
* Requires tuning parameters such as block size and `C`.
* Can produce unwanted noise in some images.

---

## 3. Otsu Thresholding

Otsu Thresholding automatically determines an appropriate threshold from the image histogram.

Instead of manually selecting a threshold, OpenCV calculates it automatically.

```python
otsu_value, otsu = cv2.threshold(
    gray,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)
```

### Advantages

* Automatically determines the threshold.
* No need to manually select the threshold value.
* Works well when foreground and background have clearly separated intensity distributions.
* Simple to implement.

### Limitations

* May not perform well with uneven illumination.
* Can struggle when foreground and background have similar intensity values.
* Works best when the image has a relatively clear separation between foreground and background.

---

# 📊 Binary vs Adaptive vs Otsu

| Feature                       | Binary    | Adaptive | Otsu             |
| ----------------------------- | --------- | -------- | ---------------- |
| Threshold type                | Fixed     | Local    | Automatic global |
| Threshold selected manually   | Yes       | No       | No               |
| Handles uneven lighting       | Poor      | Good     | Limited          |
| Computational complexity      | Low       | Medium   | Low/Medium       |
| Parameter tuning              | Low       | Higher   | Very low         |
| Good for documents            | Sometimes | Yes      | Yes              |
| Good for simple objects       | Yes       | Yes      | Yes              |
| Automatic threshold selection | No        | Yes      | Yes              |

---

# 🏆 Which Method Worked Best?

For the dataset used in this project, **Otsu Thresholding worked best for images where the foreground object/document had a clear intensity difference from the background**.

Otsu was useful because it automatically selected the threshold instead of requiring a manually chosen value.

For images with **uneven lighting**, however, **Adaptive Thresholding produced better results** because it calculates the threshold locally.

Therefore, there is no single thresholding method that is best for every image.

The results can generally be summarized as:

```text
Good and uniform lighting
        ↓
      Otsu
        ↓
Automatic threshold selection


Uneven lighting
        ↓
    Adaptive
        ↓
Local threshold calculation


Simple high-contrast image
        ↓
     Binary
        ↓
Fast and simple
```

The application therefore includes an **Automatic** option that compares the available thresholding approaches using a simple heuristic and selects a suitable segmentation mask.

---

# 🧹 Morphological Processing

Thresholding can sometimes produce small noise or holes in the segmentation mask.

To improve the mask, morphological operations are applied.

## Opening

Opening helps remove small noise:

```python
cv2.MORPH_OPEN
```

## Closing

Closing helps fill small gaps and holes:

```python
cv2.MORPH_CLOSE
```

The project uses a `5 × 5` morphological kernel:

```python
kernel = np.ones(
    (5, 5),
    np.uint8
)
```

The workflow becomes:

```text
Thresholded Image
       ↓
Morphological Opening
       ↓
Remove Small Noise
       ↓
Morphological Closing
       ↓
Fill Small Gaps
       ↓
Cleaner Mask
```

---

# ✂️ Main Object Detection

After cleaning the mask, contours are detected using OpenCV:

```python
contours, _ = cv2.findContours(
    mask,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)
```

The largest contour is selected:

```python
largest_contour = max(
    contours,
    key=cv2.contourArea
)
```

This allows the application to focus on the **main object or document** rather than small unwanted regions.

The largest contour is then filled to create the final foreground mask.

---

# 🎨 Foreground Extraction

The foreground is extracted using the segmentation mask:

```python
foreground = cv2.bitwise_and(
    image,
    image,
    mask=mask
)
```

The mask determines which pixels from the original image remain visible.

```text
Mask = 255
     ↓
Keep original pixel


Mask = 0
     ↓
Remove pixel
```

---

# 🔳 Transparent Background

The application also creates a PNG with a transparent background.

The segmentation mask is placed into the image's alpha channel:

```python
rgba[:, :, 3] = mask
```

This produces:

```text
best_segmentation.png
```

where:

```text
Foreground → Visible
Background → Transparent
```

This is useful for extracting objects that can later be placed on another background.

---

# 🖥️ Gradio Interface

The project uses **Gradio** to provide an interactive interface.

Users can:

1. Upload an image.
2. Select a sample image.
3. Select a segmentation method.
4. Adjust Binary Threshold.
5. Adjust Adaptive Block Size.
6. Adjust Adaptive `C`.
7. Run segmentation.
8. View all thresholding results.
9. View the foreground mask.
10. View the extracted foreground.
11. View the transparent result.

The interface provides:

```text
Input Image
     ↓
Thresholding Results
     ↓
Segmentation Mask
     ↓
Extracted Foreground
     ↓
Transparent Background
```

---

# 🖼️ Sample Images

The application supports sample images stored in:

```text
Day 22/images/inputImages/
```

Example:

```text
inputImages/
│
├── document.jpg
├── object.jpg
├── book.jpg
└── receipt.jpg
```

Users can click a sample image directly from the Gradio interface instead of uploading an image manually.

---

# 📁 Project Structure

```text
Day 22/
│
├── app.py
│
├── images/
│   │
│   ├── inputImages/
│   │   ├── document.jpg
│   │   ├── object.jpg
│   │   ├── book.jpg
│   │   └── receipt.jpg
│   │
│   └── outputImages/
│
└── README.md
```

---

# 📦 Requirements

Install the required Python libraries:

```bash
pip install opencv-python numpy gradio
```

Or create a `requirements.txt` file:

```text
opencv-python
numpy
gradio
```

Then install:

```bash
pip install -r requirements.txt
```

---

# ▶️ How to Run

Open the terminal in the project directory.

Run:

```bash
python app.py
```

The Gradio application will start locally.

The application can also generate a temporary public Gradio link when `share=True` is used.

---

# 💾 Output Files

After processing an image, the application saves the results in:

```text
Day 22/images/outputImages/
```

The output files include:

```text
original.png
grayscale.png
binary.png
adaptive.png
otsu.png
foreground_mask.png
foreground.png
best_segmentation.png
comparison.png
```

The most important output is:

```text
best_segmentation.png
```

because it contains the selected segmentation result with a transparent background.

---

# ⚠️ Challenges Faced During Implementation

Several challenges were encountered while implementing the segmentation tool.

### 1. Uneven Lighting

Different areas of an image can have different brightness levels.

A fixed Binary Threshold may fail in this situation.

**Solution:** Adaptive Thresholding was used for images with uneven illumination.

---

### 2. Noise in Thresholded Images

Thresholding can create small unwanted regions and noise.

**Solution:** Morphological opening and closing were applied to clean the segmentation mask.

---

### 3. Selecting the Main Object

An image may contain several foreground regions.

**Solution:** Contours were detected and the largest contour was selected as the main object/document.

---

### 4. Choosing the Best Thresholding Method

Different images produce different results with different thresholding methods.

**Solution:** The application supports Binary, Adaptive, Otsu, and Automatic selection so that the user can compare the results.

---

### 5. Background Removal

Simply creating a binary mask is not enough to produce a useful extracted object.

**Solution:** The final mask was applied to the original image using `cv2.bitwise_and()` and was also used as the alpha channel for a transparent PNG.

---

### 6. Parameter Selection

Adaptive Thresholding requires parameters such as:

```text
Block Size
C
```

Finding suitable values can require experimentation.

**Solution:** These parameters were added as Gradio sliders so that users can interactively adjust them.

---

# 🚀 Future Improvements

The project can be improved further by adding:

* GrabCut segmentation.
* Watershed segmentation.
* Edge-based segmentation.
* Background subtraction.
* Deep-learning-based segmentation.
* SAM (Segment Anything Model).
* YOLO-based object detection.
* Automatic document corner detection.
* Perspective transformation for scanned documents.
* Better segmentation quality evaluation.
* Multiple-object segmentation.
* Batch image processing.

---

# 📚 Technologies Used

| Technology | Purpose                              |
| ---------- | ------------------------------------ |
| Python     | Programming language                 |
| OpenCV     | Image processing and segmentation    |
| NumPy      | Numerical and image-array operations |
| Gradio     | Interactive web interface            |

---

# 📝 Conclusion

This project demonstrates how **image thresholding can be used for basic foreground and background segmentation**.

Binary Thresholding is simple and fast, Adaptive Thresholding is useful for uneven lighting, and Otsu Thresholding automatically determines a suitable global threshold.

The project combines these techniques with **morphological operations and contour detection** to extract the main document or object. A Gradio interface makes it easy to upload images, test different methods, compare their results, and save the best segmentation output.

Overall, this project provides a practical introduction to **image segmentation using OpenCV** and demonstrates how traditional computer vision techniques can be combined to build an interactive segmentation application.

---

## 👨‍💻 Author

**Muhammad Ashhad**

