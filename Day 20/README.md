# Day 20 - OCR with EasyOCR

## 1. Project Overview

This project demonstrates **Optical Character Recognition (OCR)** using
**EasyOCR** and **OpenCV**.

The purpose of the project is to read text from different images,
compare OCR results, and improve text extraction by applying image
preprocessing techniques before OCR.

The project was tested on multiple images, including different types of
printed/text-containing images. The application can process multiple
images from the input folder and save the extracted text separately for
each image.

------------------------------------------------------------------------

## 2. What is OCR?

**OCR (Optical Character Recognition)** is a technology used to detect
and recognize text present in images and convert that text into
machine-readable characters.

For example, if an image contains:

``` text
ABC COMPANY
Invoice No: 12345
Total: Rs. 5000
```

OCR can extract it as:

``` text
ABC COMPANY
Invoice No: 12345
Total: Rs. 5000
```

The extracted text can then be stored in a text file, searched, edited,
or processed by another application.

### Common OCR Applications

OCR is commonly used for:

-   Reading printed documents
-   Extracting information from receipts and invoices
-   Reading signboards
-   Digitizing books and documents
-   Document scanning
-   Data entry automation
-   Extracting text from photographs
-   Converting paper documents into digital text

------------------------------------------------------------------------

# 3. OCR Library Used

## EasyOCR

This project uses **EasyOCR** as the OCR library.

EasyOCR is a Python OCR library that can detect text regions in images
and recognize the text contained inside those regions.

The reader is initialized as:

``` python
import easyocr as ocr

reader = ocr.Reader(
    ["en"],
    gpu=False
)
```

### Why EasyOCR was used

EasyOCR was selected because:

-   It has a simple Python API.
-   It is easy to install and use.
-   It can automatically detect text regions.
-   It provides the detected text and bounding boxes.
-   It provides a confidence value for each detected text region.
-   It supports multiple languages.
-   It works well with different types of images.
-   It can run using the CPU.

In this project, English OCR was used:

``` python
reader = ocr.Reader(["en"], gpu=False)
```

The `["en"]` parameter specifies English text recognition.

The `gpu=False` parameter makes EasyOCR run using the CPU.

------------------------------------------------------------------------

# 4. How the OCR Process Works

The OCR workflow used in this project is:

``` text
Input Image
     |
     v
Image Resizing
     |
     v
Grayscale Conversion
     |
     v
Gaussian Blur / Denoising
     |
     v
CLAHE Contrast Enhancement
     |
     v
Adaptive Thresholding
     |
     v
Morphological Opening
     |
     v
EasyOCR
     |
     v
Text Detection and Recognition
     |
     +--------------------+
     |                    |
     v                    v
Detected Text        Bounding Boxes
     |
     v
TXT Output
```

------------------------------------------------------------------------

# 5. Image Preprocessing

Image preprocessing was an important part of this project because the
quality of the input image directly affects OCR performance.

The following preprocessing techniques were used.

------------------------------------------------------------------------

## 5.1 Image Resizing

The image was resized by a factor of 2:

``` python
scale = 2

image_resized = cv2.resize(
    image,
    None,
    fx=scale,
    fy=scale,
    interpolation=cv2.INTER_CUBIC
)
```

### Purpose

Resizing makes small characters larger and can help OCR detect text more
effectively.

`INTER_CUBIC` interpolation was used when enlarging the image.

------------------------------------------------------------------------

## 5.2 Grayscale Conversion

The resized image was converted to grayscale:

``` python
gray = cv2.cvtColor(
    image_resized,
    cv2.COLOR_BGR2GRAY
)
```

### Purpose

Grayscale removes color information and keeps the intensity information
of the image.

It can make text/background separation easier and provides a simpler
image for later preprocessing operations.

------------------------------------------------------------------------

## 5.3 Gaussian Blur / Denoising

Gaussian blur was applied:

``` python
denoised = cv2.GaussianBlur(
    gray,
    (3, 3),
    0
)
```

### Purpose

Gaussian blur reduces small amounts of image noise and unwanted
artifacts.

This can help produce a cleaner image before thresholding.

------------------------------------------------------------------------

## 5.4 CLAHE Contrast Enhancement

CLAHE (Contrast Limited Adaptive Histogram Equalization) was used to
improve local contrast:

``` python
clahe = cv2.createCLAHE(
    clipLimit=2.0,
    tileGridSize=(8, 8)
)

enhanced = clahe.apply(
    denoised
)
```

### Purpose

CLAHE can improve text visibility when the image has:

-   Low contrast
-   Uneven lighting
-   Dark and bright regions
-   Poor text/background separation

This was one of the useful enhancement techniques for improving
difficult images.

------------------------------------------------------------------------

## 5.5 Adaptive Thresholding

Adaptive thresholding was applied:

``` python
threshold = cv2.adaptiveThreshold(
    enhanced,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    31,
    11
)
```

### Purpose

Adaptive thresholding converts the image into a binary image while
calculating the threshold locally.

This is useful when an image does not have uniform lighting.

It can help separate text from the background in documents and
photographs with uneven illumination.

------------------------------------------------------------------------

## 5.6 Morphological Opening

Morphological opening was applied:

``` python
kernel = np.ones(
    (2, 2),
    np.uint8
)

processed = cv2.morphologyEx(
    threshold,
    cv2.MORPH_OPEN,
    kernel
)
```

### Purpose

Morphological opening can remove small unwanted noise from the
thresholded image.

It consists of erosion followed by dilation.

The resulting image can be cleaner and easier for OCR to process.

------------------------------------------------------------------------

# 6. EasyOCR Configuration

The processed image is passed to EasyOCR using:

``` python
result = reader.readtext(
    processed,
    detail=1,
    paragraph=False,
    min_size=10,
    text_threshold=0.5,
    low_text=0.3,
    link_threshold=0.3,
    mag_ratio=1.5
)
```

### Important Parameters

### `detail=1`

Returns detailed OCR results including:

-   Bounding box
-   Detected text
-   Confidence score

### `paragraph=False`

Keeps individual text detections separate instead of combining them into
paragraphs.

### `min_size=10`

Sets a minimum size for text detection.

### `text_threshold=0.5`

Controls the threshold used for detecting text regions.

### `low_text=0.3`

Controls detection of lower-confidence text regions.

### `link_threshold=0.3`

Controls how detected text regions can be linked together.

### `mag_ratio=1.5`

Controls the magnification ratio used during text detection.

------------------------------------------------------------------------

# 7. OCR Results

EasyOCR returns results in the following general format:

``` python
[
    [
        bounding_box,
        detected_text,
        confidence
    ]
]
```

The project reads the values as:

``` python
box = detection[0]
text = detection[1]
confidence = detection[2]
```

The bounding box is used to draw a box around detected text.

The detected text is saved in the TXT output.

The confidence value is used to evaluate the OCR result and can be
displayed in the terminal/result image.

## Important Output Rule

**Confidence values are not saved in the TXT files.**

The TXT files contain only the extracted text.

For example:

``` text
ABC COMPANY
INVOICE
Product Name
Quantity
Total: Rs. 5000
```

The TXT file does not contain:

``` text
Confidence: 0.95
Confidence: 0.89
```

------------------------------------------------------------------------

# 8. Testing Different Images

The OCR program processes images from:

``` text
Day 20/images/inputImages/
```

The project was designed to test at least 10 different images.

The images can represent different OCR conditions such as:

-   Printed documents
-   Receipts or invoices
-   Signboards
-   Book pages
-   Handwritten notes, if available
-   Other photographs containing text

Different image types can produce different OCR results because text
size, font, lighting, background, image quality, and handwriting can
affect recognition.

------------------------------------------------------------------------

# 9. OCR Result Comparison

The OCR results can be compared between the original and preprocessed
images.

### Without preprocessing

``` text
Original Image
       |
       v
EasyOCR
       |
       v
OCR Result
```

### With preprocessing

``` text
Original Image
       |
       v
Resize
       |
       v
Grayscale
       |
       v
Denoising
       |
       v
CLAHE
       |
       v
Adaptive Threshold
       |
       v
Morphological Opening
       |
       v
EasyOCR
       |
       v
Improved OCR Result
```

Preprocessing generally helps when the image contains noise, low
contrast, uneven lighting, or small text.

However, preprocessing does not guarantee better results for every
image. Excessive thresholding or morphological operations can sometimes
remove important parts of characters.

------------------------------------------------------------------------

# 10. Challenges Faced During OCR

## 10.1 Image Quality

Blurry, compressed, or low-resolution images can make characters
difficult to recognize.

Clear and high-resolution images generally produce better OCR results.

------------------------------------------------------------------------

## 10.2 Small Text

Small characters can be difficult for OCR to detect.

Image resizing was used to make the characters larger before OCR.

------------------------------------------------------------------------

## 10.3 Uneven Lighting

Photographs of documents can contain shadows or different brightness
levels.

CLAHE and adaptive thresholding were used to improve text visibility in
such cases.

------------------------------------------------------------------------

## 10.4 Image Noise

Noise, dots, and small artifacts can interfere with text recognition.

Gaussian blur and morphological opening were used to reduce unwanted
noise.

------------------------------------------------------------------------

## 10.5 Complex Backgrounds

Text placed on a complicated or textured background can be difficult to
separate from the background.

Preprocessing can help, but OCR accuracy may still decrease when the
background is very complex.

------------------------------------------------------------------------

## 10.6 Handwritten Text

Handwritten text is generally more challenging than clear printed text
because handwriting varies from person to person.

Characters may have:

-   Different shapes
-   Irregular spacing
-   Connected letters
-   Different writing styles
-   Inconsistent alignment

Therefore, handwritten notes may produce less accurate results than
printed documents.

------------------------------------------------------------------------

## 10.7 Different Fonts and Text Styles

OCR results can vary depending on:

-   Font type
-   Font size
-   Text orientation
-   Text spacing
-   Text color
-   Background color

------------------------------------------------------------------------

# 11. Output Folder Structure

The project uses the following folder structure:

``` text
Day 20/
│
├── images/
│   │
│   ├── inputImages/
│   │   ├── text (1).jpg
│   │   ├── text (2).jpg
│   │   ├── text (3).jpg
│   │   ├── text (4).jpg
│   │   ├── text (5).jpg
│   │   └── ...
│   │
│   └── outputImages/
│       │
│       ├── processed_images/
│       │   ├── text (1)_processed.png
│       │   ├── text (2)_processed.png
│       │   ├── text (3)_processed.png
│       │   └── ...
│       │
│       ├── result_images/
│       │   ├── text (1)_result.png
│       │   ├── text (2)_result.png
│       │   ├── text (3)_result.png
│       │   └── ...
│       │
│       ├── text (1).txt
│       ├── text (2).txt
│       ├── text (3).txt
│       ├── text (4).txt
│       └── ...
│
├── main.py
├── OCRPractice.py
├── README.md
└── requirements.txt
```

------------------------------------------------------------------------

# 12. Description of Project Files

## `main.py`

Contains the main OCR application/interface.

It can be used to run the OCR functionality through the application
interface.

## `OCRPractice.py`

Contains the OCR processing workflow for reading and processing multiple
images.

It performs:

-   Image loading
-   Resizing
-   Grayscale conversion
-   Denoising
-   CLAHE enhancement
-   Adaptive thresholding
-   Morphological processing
-   EasyOCR text extraction
-   Result image generation
-   TXT file generation

## `requirements.txt`

Contains the Python packages required to run the project.

Typical dependencies include:

``` text
easyocr
opencv-python
numpy
gradio
```

## `README.md`

Contains the project documentation, OCR explanation, preprocessing
explanation, challenges, and project structure.

------------------------------------------------------------------------

# 13. Output Files

For every input image, the project creates:

### Processed image

Stored in:

``` text
Day 20/images/outputImages/processed_images/
```

Example:

``` text
text (1)_processed.png
```

### OCR result image

Stored in:

``` text
Day 20/images/outputImages/result_images/
```

Example:

``` text
text (1)_result.png
```

### Extracted text

Stored in:

``` text
Day 20/images/outputImages/
```

Example:

``` text
text (1).txt
```

Each TXT file contains only the detected text.

------------------------------------------------------------------------

# 14. Installation

Install the required packages using:

``` bash
pip install -r requirements.txt
```

Or install the main packages individually:

``` bash
pip install easyocr
pip install opencv-python
pip install numpy
pip install gradio
```

------------------------------------------------------------------------

# 15. Running the Project

To run the OCR practice script:

``` bash
python OCRPractice.py
```

To run the main application:

``` bash
python main.py
```

The application processes the images and saves the results in the
configured output folders.

------------------------------------------------------------------------

# 16. Conclusion

This project demonstrates a complete OCR workflow using **EasyOCR** and
**OpenCV**.

The main preprocessing techniques used were:

1.  Image resizing
2.  Grayscale conversion
3.  Gaussian blur
4.  CLAHE contrast enhancement
5.  Adaptive thresholding
6.  Morphological opening

These techniques can improve text visibility and help OCR perform better
on images affected by noise, low contrast, uneven lighting, or small
text.

The project also demonstrates how OCR results can be saved separately
for multiple images and how processed images and OCR result images can
be generated for comparison.

The main challenges were image quality, small text, noise, uneven
lighting, complex backgrounds, different fonts, and handwritten text.

Overall, EasyOCR combined with OpenCV preprocessing provides a practical
approach for extracting text from a variety of images.

# 👨‍💻 Author

**Muhammad Ashhad**