# Day 15 – Document Image Transformation & Enhancement

## 📌 Project Overview

This project focuses on **document image transformation and enhancement using OpenCV**. The goal is to improve the quality, readability, and usability of document images before they are used for further processing such as OCR, document analysis, or computer vision tasks.

The project contains image transformation techniques as well as document enhancement techniques. The processed images are saved in the `outputImages` folder.

---


# 🔄 Image Transformations Implemented

## 1. Grayscale Conversion

The original color image is converted into a grayscale image.

### Purpose

- Removes unnecessary color information.
- Reduces image complexity.
- Makes document text easier to process.
- Provides a suitable input for thresholding and other enhancement techniques.

### OpenCV Function

```python
cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
```

---

## 2. Image Resizing

The image dimensions are changed to a required size.

### Purpose

- Standardizes image dimensions.
- Makes processing more consistent.
- Can reduce processing time when very large images are used.
- Can improve readability when a low-resolution document is enlarged appropriately.

### OpenCV Function

```python
cv2.resize()
```

---

## 3. Image Rotation

The document image can be rotated to change its orientation.

### Purpose

- Corrects incorrectly oriented images.
- Makes documents easier to read.
- Helps prepare images for OCR and further processing.

### OpenCV Functions

```python
cv2.getRotationMatrix2D()
cv2.warpAffine()
```

---

## 4. Image Flipping

The image can be flipped horizontally or vertically.

### Purpose

- Corrects mirrored images.
- Provides different orientations when required.
- Useful as a basic image transformation technique.

### OpenCV Function

```python
cv2.flip()
```

---

## 5. Cropping

Only the required region of the document is selected.

### Purpose

- Removes unnecessary areas.
- Focuses processing on the document or text region.
- Reduces the amount of irrelevant information.

### Technique

Cropping is performed using NumPy array slicing.

```python
cropped = image[y1:y2, x1:x2]
```

---

# ✨ Document Enhancement Techniques

## 6. Brightness and Contrast Enhancement

Brightness and contrast are adjusted to make the document clearer.

### Purpose

- Improves visibility of text.
- Makes faded documents easier to read.
- Increases separation between foreground text and background.

### OpenCV Function

```python
cv2.convertScaleAbs()
```

---

## 7. Gaussian Blur / Noise Reduction

Gaussian filtering is used to reduce unwanted noise from the image.

### Purpose

- Removes small variations and noise.
- Produces a smoother image.
- Helps improve the result of later thresholding operations.

### OpenCV Function

```python
cv2.GaussianBlur()
```

---

## 8. Median Blur

Median filtering is another noise-reduction technique used to remove small noise while preserving important edges.

### Purpose

- Reduces salt-and-pepper noise.
- Preserves document edges better than some simple smoothing methods.
- Produces cleaner document images.

### OpenCV Function

```python
cv2.medianBlur()
```

---

## 9. Image Sharpening

Sharpening is applied to make text and document edges more distinct.

### Purpose

- Improves text clarity.
- Makes blurred characters more visible.
- Enhances edges and fine details.

### Technique

A sharpening kernel is applied using convolution.

```python
cv2.filter2D()
```

---

## 10. Binary Thresholding

A grayscale document is converted into a binary image containing mainly black and white pixels.

### Purpose

- Separates text from the background.
- Makes document text more prominent.
- Produces a cleaner image for OCR.
- Removes some background variations.

### OpenCV Function

```python
cv2.threshold()
```

---

## 11. Adaptive Thresholding

Adaptive thresholding calculates the threshold value for different regions of the image instead of using one global threshold.

### Purpose

- Handles uneven lighting.
- Works well with documents containing shadows.
- Improves text visibility when the background is not uniform.

### OpenCV Function

```python
cv2.adaptiveThreshold()
```

---

## 12. Morphological Operations

Morphological processing is used to refine the binary document image.

Operations such as opening and closing can be used depending on the document condition.

### Purpose

- Removes small unwanted noise.
- Fills small gaps in text.
- Connects broken parts of characters.
- Produces a cleaner document structure.

### OpenCV Functions

```python
cv2.morphologyEx()
cv2.getStructuringElement()
```

---

## 🧾 Document Enhancement Workflow

The general document enhancement workflow used in this project is:

```text
Input Document
      ↓
Read Image
      ↓
Grayscale Conversion
      ↓
Noise Reduction
      ↓
Brightness / Contrast Adjustment
      ↓
Sharpening
      ↓
Thresholding
      ↓
Morphological Processing
      ↓
Enhanced Document
      ↓
Save Output Image
```

This workflow helps convert a raw document image into a cleaner and more readable image.

---

# ⭐ Transformation With the Biggest Impact

Among the implemented enhancement techniques, **thresholding had the biggest impact on document quality**, especially for text-based documents.

Thresholding converts the document into a clearer foreground/background representation. Text becomes much more distinct from the background, which significantly improves readability.

### Why Thresholding Was Important

- Makes text more prominent.
- Reduces background variations.
- Produces a cleaner black-and-white document.
- Helps prepare the document for OCR.
- Makes the overall document structure easier to analyze.

**Adaptive thresholding** can be particularly effective when the document has uneven lighting or shadows because it calculates threshold values locally.

---

# 🛠️ Challenges Faced During Implementation

## 1. Handling Different Image Sizes

Input images can have different dimensions and resolutions.

### Solution

Image resizing was used when a consistent image size was required.

---

## 2. Noise in Document Images

Some document images contain noise, spots, or unwanted small details.

### Solution

Blur and filtering techniques such as Gaussian Blur and Median Blur were used to reduce unwanted noise before further processing.

---

## 3. Uneven Lighting

Some documents may have shadows or different brightness levels across the page.

### Solution

Adaptive thresholding was used because it calculates threshold values for different local regions of the image.

---

## 4. Maintaining Text Quality

Excessive enhancement can remove important details or make text look unnatural.

### Solution

Enhancement operations were applied carefully and in a suitable sequence so that text remained readable while unwanted noise was reduced.

---

## 5. Choosing Suitable Threshold Values

A threshold value that works well for one image may not work equally well for another image.

### Solution

Different thresholding approaches were considered, including global and adaptive thresholding, to achieve better results for different document conditions.

---

## 6. Saving Processed Images

Processed images need to be saved correctly without losing the expected output.

### Solution

The project uses the `outputImages` directory to store generated results and keeps input images separately inside `inputImages`.

---

# 💻 Technologies Used

- **Python**
- **OpenCV**
- **NumPy**
- **VS Code**

---
## 📁 Project Structure

```text
Day 15/
│
├── dataset/
│   └── # Dataset / source document images
│
├── inputImages/
│   └── # Input images used for processing
│
├── outputImages/
│   └── # Enhanced and transformed output images
│
├── documentEnhancement.py
│   └── # Script for document image enhancement
│
├── imageTransformation&Enhancement.py
│   └── # Script containing image transformations and enhancement techniques
│
├── README.md
│   └── # Project documentation
│
└── requirements.txt
    └── # Required Python libraries
```

---


# 📦 Main OpenCV Functions Used

| Function | Purpose |
|---|---|
| `cv2.imread()` | Read an image |
| `cv2.imwrite()` | Save an image |
| `cv2.cvtColor()` | Convert color spaces |
| `cv2.resize()` | Resize images |
| `cv2.getRotationMatrix2D()` | Create rotation matrix |
| `cv2.warpAffine()` | Apply rotation |
| `cv2.flip()` | Flip an image |
| `cv2.GaussianBlur()` | Reduce noise |
| `cv2.medianBlur()` | Reduce salt-and-pepper noise |
| `cv2.convertScaleAbs()` | Adjust brightness and contrast |
| `cv2.filter2D()` | Apply sharpening/filter kernels |
| `cv2.threshold()` | Perform binary thresholding |
| `cv2.adaptiveThreshold()` | Perform adaptive thresholding |
| `cv2.morphologyEx()` | Perform morphological operations |
| `cv2.getStructuringElement()` | Create morphology kernels |

---

# 🎯 Project Objectives

The main objectives of this project were:

1. Learn how document images can be transformed using OpenCV.
2. Understand different image enhancement techniques.
3. Improve document readability.
4. Reduce image noise.
5. Improve text and edge visibility.
6. Understand the importance of thresholding for document processing.
7. Save enhanced document images for further computer vision or OCR tasks.

---

# 📊 Expected Results

After processing, the enhanced document should have:

- Better text visibility.
- Reduced unwanted noise.
- Improved contrast.
- Cleaner background.
- Sharper document details.
- Better separation between text and background.
- Improved suitability for OCR and document analysis.

The generated images are stored in:

```text
Day 15/outputImages/
```

---

# 🧠 Learning Outcomes

Through this project, I learned:

- How to load and save images with OpenCV.
- How grayscale conversion simplifies document processing.
- How resizing, rotation, flipping, and cropping transform images.
- How noise reduction improves document quality.
- How brightness and contrast affect readability.
- How sharpening improves text and edge visibility.
- How global and adaptive thresholding work.
- How morphological operations can refine document images.
- How a sequence of preprocessing techniques can improve document quality.

---

# ✅ Conclusion

Day 15 focused on **Image Transformation and Document Enhancement using OpenCV**. Different transformation techniques were implemented to manipulate images, while enhancement techniques were used to improve document readability and quality.

The most significant improvement came from **thresholding**, because it clearly separated document text from the background. Noise reduction, contrast enhancement, sharpening, and morphological processing further improved the final document quality.

This project provides a practical foundation for **OCR, document scanning, document analysis, and other computer vision applications**.

---

## 👨‍💻 Project

**Day:** 15  
**Topic:** Image Transformation & Document Enhancement  
**Language:** Python  
**Library:** OpenCV  
**IDE:** VS Code
