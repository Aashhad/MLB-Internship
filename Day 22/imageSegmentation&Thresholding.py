import cv2
import numpy as np
import os


# PATHS

# Input image path
input_path = "Day 22/images/inputImages/Tools.jpg"

# Output folder
output_folder = "Day 22/images/outputImages"

# Create output folder if it does not exist
os.makedirs(output_folder, exist_ok=True)


# READ IMAGE
image = cv2.imread(input_path)
# Check whether image was loaded successfully
if image is None:
    print("ERROR: Image could not be loaded.")
    print("Please check the input image path:")
    print(input_path)
    exit()

print("Image loaded successfully!")
print("Image shape:", image.shape)


# CONVERT IMAGE TO GRAYSCALE
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Save grayscale image
cv2.imwrite(os.path.join(output_folder, "01_grayscale.jpg"), gray)
print("Grayscale image saved.")


# BINARY THRESHOLDING

# Threshold value
threshold_value = 135

# Maximum value
max_value = 255

# Apply binary thresholding
binary_threshold_value, binary = cv2.threshold(
    gray,
    threshold_value,
    max_value,
    cv2.THRESH_BINARY
)

print("Binary threshold value:", binary_threshold_value)

# Save binary threshold image
cv2.imwrite(os.path.join(output_folder, "02_binary_threshold.jpg"), binary)
print("Binary threshold image saved.")


# ADAPTIVE THRESHOLDING

# Block size must be an odd number
block_size = 5

# Constant subtracted from calculated threshold
C = 3

# Apply adaptive thresholding
adaptive = cv2.adaptiveThreshold(
    gray,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    block_size,
    C
)

# Save adaptive threshold image
cv2.imwrite(os.path.join(output_folder, "03_adaptive_threshold.jpg"), adaptive)
print("Adaptive threshold image saved.")


# OTSU THRESHOLDING

# Otsu automatically calculates the best threshold
otsu_threshold_value, otsu = cv2.threshold(
    gray,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)
print("Otsu automatically selected threshold:", otsu_threshold_value)

# Save Otsu threshold image
cv2.imwrite(os.path.join(output_folder, "04_otsu_threshold.jpg"), otsu)
print("Otsu threshold image saved.")


# SIMPLE FOREGROUND / BACKGROUND SEGMENTATION

# We use Otsu's threshold result as the segmentation mask.
foreground_mask = otsu.copy()

# Save foreground mask
cv2.imwrite(os.path.join(output_folder, "05_foreground_mask.jpg"), foreground_mask)
print("Foreground mask saved.")


# EXTRACT FOREGROUND

foreground = cv2.bitwise_and(
    image,
    image,
    mask=foreground_mask
)

# Save foreground
cv2.imwrite(os.path.join(output_folder, "06_foreground.jpg"), foreground)
print("Foreground image saved.")


# CREATE BACKGROUND MASK

# Invert the foreground mask
background_mask = cv2.bitwise_not( foreground_mask)

# Save background mask
cv2.imwrite(os.path.join(output_folder, "07_background_mask.jpg"), background_mask)
print("Background mask saved.")


# EXTRACT BACKGROUND
background = cv2.bitwise_and(
    image,
    image,
    mask=background_mask
)

# Save background
cv2.imwrite(os.path.join(output_folder, "08_background.jpg"), background)
print("Background image saved.")


# CREATE COMPARISON IMAGE

# Resize all images to the same size
display_width = 400
display_height = 300

original_display = cv2.resize(image, (display_width, display_height))
binary_display = cv2.resize(binary, (display_width, display_height))
adaptive_display = cv2.resize(adaptive, (display_width, display_height))
otsu_display = cv2.resize(otsu,(display_width, display_height))

# CONVERT GRAYSCALE IMAGES TO BGR
binary_display = cv2.cvtColor(binary_display,cv2.COLOR_GRAY2BGR)
adaptive_display = cv2.cvtColor(adaptive_display,cv2.COLOR_GRAY2BGR)
otsu_display = cv2.cvtColor(otsu_display,cv2.COLOR_GRAY2BGR)

# ADD LABELS
cv2.putText(
    original_display,
    "Original",
    (10, 30),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (0, 255, 0),
    2
)

cv2.putText(
    binary_display,
    "Binary Threshold",
    (10, 30),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (0, 255, 0),
    2
)

cv2.putText(
    adaptive_display,
    "Adaptive Threshold",
    (10, 30),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (0, 255, 0),
    2
)

cv2.putText(
    otsu_display,
    "Otsu Threshold",
    (10, 30),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (0, 255, 0),
    2
)


# COMBINE IMAGES

# First row
top_row = np.hstack([original_display, binary_display])
# Second row
bottom_row = np.hstack([adaptive_display, otsu_display])
# Combine both rows
comparison = np.vstack([top_row, bottom_row])


# SAVE COMPARISON IMAGE
cv2.imwrite(os.path.join(output_folder, "09_comparison.jpg"), comparison)
print("Comparison image saved.")


# DISPLAY RESULTS
cv2.imshow("Original Image", image)
cv2.imshow("Grayscale Image", gray)
cv2.imshow("Binary Threshold", binary)
cv2.imshow("Adaptive Threshold", adaptive)
cv2.imshow("Otsu Threshold", otsu)
cv2.imshow("Foreground", foreground)
cv2.imshow("Background", background)
cv2.imshow("Thresholding Comparison", comparison)


# PRINT SUMMARY
print("\n" + "=" * 60)
print("PROCESSING COMPLETED")
print("=" * 60)

print("\nMethods applied:")
print("1. Grayscale Conversion")
print("2. Binary Thresholding")
print("3. Adaptive Thresholding")
print("4. Otsu Thresholding")
print("5. Foreground Segmentation")
print("6. Background Segmentation")
print("7. Thresholding Comparison")

print("\nOtsu Threshold Value:")
print(otsu_threshold_value)

print("\nOutput files:")
print("\nAll files are saved inside:")
print(output_folder)


# WAIT FOR KEY PRESS
print("\nPress any key on an image window to close the program.")
cv2.waitKey(0)
cv2.destroyAllWindows()