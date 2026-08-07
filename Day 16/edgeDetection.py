import cv2
import numpy as np

# Load Image
image = cv2.imread(r"Day 16\inputImages\flower.jpg")

if image is None:
    print("Image not found!")
    exit()

# Convert to Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian Blur
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Sobel Edge Detection
sobel_x = cv2.Sobel(blur, -1, 1, 0, ksize=3)
sobel_y = cv2.Sobel(blur, -1, 0, 1, ksize=3)

sobel = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)

# Laplacian Edge Detection
laplacian = cv2.Laplacian(blur, -1)


# Canny Edge Detection
canny = cv2.Canny(blur, 100, 200)

# Add Titles
def add_title(img, title):
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    cv2.putText(
        img,
        title,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2,
    )
    return img

original = add_title(image.copy(), "Original")
gray_img = add_title(gray.copy(), "Grayscale")
blur_img = add_title(blur.copy(), "Gaussian Blur")
sobel_img = add_title(sobel.copy(), "Sobel")
laplacian_img = add_title(laplacian.copy(), "Laplacian")
canny_img = add_title(canny.copy(), "Canny")

# Comparison
top_row = np.hstack((original, gray_img, blur_img))
bottom_row = np.hstack((sobel_img, laplacian_img, canny_img))
comparison = np.vstack((top_row, bottom_row))


cv2.imshow("Edge Detection Comparison", comparison)

# Save comparison image
cv2.imwrite(r"Day 16\outputImages\edge_detection_comparison.jpg", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()

