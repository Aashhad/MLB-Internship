import cv2
import numpy as np
import os


# FOLDER PATHS

input_folder = "Day 15/inputImages"
output_folder = "Day 15/outputImages"

os.makedirs(output_folder, exist_ok=True)


# LOAD IMAGE
image_path = os.path.join(input_folder, "natrure.jpg")
image = cv2.imread(image_path)

if image is None:
    print("Error: Image not found!")
    print("Please put sample.jpg inside the inputImages folder.")
    exit()

print("Image loaded successfully!")

height, width = image.shape[:2]
print("Image width:", width)
print("Image height:", height)


# TRANSLATION

# Move image 100 pixels right
# Move image 50 pixels down

translation_matrix = np.float32([
    [1, 0, 100],
    [0, 1, 50]
])

translated = cv2.warpAffine(
    image,
    translation_matrix,
    (width, height)
)

cv2.imwrite(
    os.path.join(output_folder, "translated.jpg"),
    translated
)

print("Translation completed.")


# ROTATION

center = (width // 2, height // 2)


# Rotate 45 degrees

rotation_matrix = cv2.getRotationMatrix2D(center, 45, 1)
rotated_45 = cv2.warpAffine(image, rotation_matrix, (width, height))
cv2.imwrite(os.path.join(output_folder, "rotated_45.jpg"), rotated_45)


# Rotate 90 degrees

rotation_matrix = cv2.getRotationMatrix2D(center, 90, 1)

rotated_90 = cv2.warpAffine(image, rotation_matrix,(width, height))

cv2.imwrite(os.path.join(output_folder, "rotated_90.jpg"), rotated_90)
print("Rotation completed.")


# SCALING

# Increase image size
scaled_up = cv2.resize(image, None, fx=1.5, fy=1.5)
cv2.imwrite(os.path.join(output_folder, "scaled_up.jpg"), scaled_up)


# Decrease image size
scaled_down = cv2.resize(image, None, fx=0.5, fy=0.5)
cv2.imwrite( os.path.join(output_folder, "scaled_down.jpg"), scaled_down)
print("Scaling completed.")


# AFFINE TRANSFORMATION

# Three points from original image
points1 = np.float32([
    [50, 50],
    [200, 50],
    [50, 200]
])


# New positions of those three points
points2 = np.float32([
    [50, 100],
    [200, 50],
    [100, 200]
])

affine_matrix = cv2.getAffineTransform(points1, points2)

affine = cv2.warpAffine(image, affine_matrix, (width, height))

cv2.imwrite(os.path.join(output_folder, "affine.jpg"), affine)
print("Affine transformation completed.")


# PERSPECTIVE TRANSFORMATION

# Four points from original image
points1 = np.float32([
    [100, 100],
    [400, 100],
    [400, 400],
    [100, 400]
])

# Destination points
points2 = np.float32([
    [0, 0],
    [300, 0],
    [300, 300],
    [0, 300]
])


perspective_matrix = cv2.getPerspectiveTransform(points1, points2)
perspective = cv2.warpPerspective(image, perspective_matrix,(300, 300))
cv2.imwrite(os.path.join(output_folder, "perspective.jpg"), perspective)

print("Perspective transformation completed.")


# BRIGHTNESS ADJUSTMENT

# Increase brightness
bright = cv2.convertScaleAbs(image, alpha=1, beta=50)

cv2.imwrite(os.path.join(output_folder, "bright.jpg"), bright)


# Decrease brightness
dark = cv2.convertScaleAbs(image, alpha=1, beta=-50)
cv2.imwrite(os.path.join(output_folder, "dark.jpg"), dark)

print("Brightness adjustment completed.")


# CONTRAST ADJUSTMENT

contrast = cv2.convertScaleAbs(image, alpha=1.5, beta=0)
cv2.imwrite(os.path.join(output_folder, "contrast.jpg"), contrast)
print("Contrast adjustment completed.")



# GAUSSIAN BLUR

gaussian_blur = cv2.GaussianBlur(image, (5, 5),0 )
cv2.imwrite(os.path.join(output_folder, "gaussian_blur.jpg"), gaussian_blur)
print("Gaussian blur completed.")


# MEDIAN BLUR

median_blur = cv2.medianBlur(image, 5)
cv2.imwrite(os.path.join(output_folder, "median_blur.jpg"), median_blur)
print("Median blur completed.")


# BILATERAL FILTER

bilateral = cv2.bilateralFilter(image,9,75,75)
cv2.imwrite(os.path.join(output_folder, "bilateral.jpg"), bilateral)
print("Bilateral filter completed.")


# IMAGE SHARPENING
sharpening_kernel = np.array([
    [0, -1, 0],
    [-1, 9, -1],
    [0, -1, 0]
])

sharpened = cv2.filter2D( image, -1, sharpening_kernel)

cv2.imwrite(os.path.join(output_folder, "sharpened.jpg"),sharpened)
print("Image sharpening completed.")


# FINAL MESSAGE
print("\n====================================")
print("All Image Operations Can Run Successfully!")
print("Check the outputImages folder.")
print("====================================")