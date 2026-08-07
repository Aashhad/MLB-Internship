import cv2
import numpy as np
import os

# Create Output Folder
os.makedirs(r"Day 16\outputImages", exist_ok=True)
# Load Image
image = cv2.imread(r"Day 16\inputImages\tilted.jpg")
if image is None:
    print("Image not found!")
    exit()
# Convert to Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Binary Image
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Kernel
kernel = np.ones((5, 5), np.uint8)

# Morphological Operations
erosion = cv2.erode(binary, kernel, iterations=1)
dilation = cv2.dilate(binary, kernel, iterations=1)
opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)
top_hat = cv2.morphologyEx(binary, cv2.MORPH_TOPHAT, kernel)
black_hat = cv2.morphologyEx(binary, cv2.MORPH_BLACKHAT, kernel)

# Function to Add Title
def prepare(img, title):
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Resize every image to same size
    img = cv2.resize(img, (350, 450))

    cv2.putText(
        img,
        title,
        (15, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )

    return img

# Prepare Images
images = [
    prepare(binary, "Original"),
    prepare(erosion, "Erosion"),
    prepare(dilation, "Dilation"),
    prepare(opening, "Opening"),
    prepare(closing, "Closing"),
    prepare(gradient, "Gradient"),
    prepare(top_hat, "Top Hat"),
    prepare(black_hat, "Black Hat"),
]

# Merge into 2 x 4 Grid
row1 = np.hstack(images[:4])
row2 = np.hstack(images[4:])

comparison = np.vstack((row1, row2))

# Save & Show
save_path = r"Day 16\outputImages\morphology_operations_comparison.jpg"
cv2.imwrite(save_path, comparison)
cv2.imshow("Morphological Operations Comparison", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(f"Saved successfully:\n{save_path}")