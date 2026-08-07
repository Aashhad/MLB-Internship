import cv2


# Read the input image
image = cv2.imread("Day 17/inputImages/shape.jpg")

# Convert the image to Grayscale
# This simplifies the image and makes contour detection easier.
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian Blur
# Removes noise and smooths the image.
# Parameters:
# gray   -> Input grayscale image
# (5,5)  -> Kernel size (must be odd)
# 0      -> Sigma value (calculated automatically)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Binary Threshold
# Parameters:
# gray               -> Input grayscale image
# 57                 -> Threshold value
# 255                -> Maximum pixel value (White)
# THRESH_BINARY      -> Pixels >57 become white, others become black
_, thresh = cv2.threshold(
    gray,
    57,
    255,
    cv2.THRESH_BINARY
)

# Find Contours
# Parameters:
# thresh                    -> Binary image
# cv2.RETR_EXTERNAL         -> Retrieve only outer contours
# cv2.CHAIN_APPROX_SIMPLE   -> Store only essential contour points
contours, hierarchy = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

# Loop through each detected contour
for cnt in contours:

    # Draw the contour
    # image        -> Image on which to draw
    # [cnt]        -> List containing one contour
    # -1           -> Draw all contours in the list
    # (0,255,0)    -> Green color (BGR)
    # 2            -> Line thickness
    cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)

    # Calculate Contour Area
    # Returns the area inside the contour (pixels²)
    area = cv2.contourArea(cnt)

    # Calculate Contour Perimeter (Arc Length)
    # Parameters:
    # cnt   -> Input contour
    # True  -> Contour is closed
    perimeter = cv2.arcLength(cnt, True)

    # Find Bounding Rectangle
    # x -> Top-left x-coordinate
    # y -> Top-left y-coordinate
    # w -> Width
    # h -> Height
    x, y, w, h = cv2.boundingRect(cnt)

    # Draw Bounding Rectangle
    # image          -> Image
    # (x,y)          -> Top-left corner
    # (x+w,y+h)      -> Bottom-right corner
    # (0,255,0)      -> Green color
    # 2              -> Thickness
    cv2.rectangle(
        image,
        (x, y),
        (x + w, y + h),
        (0, 255, 0),
        2
    )
    # Find Minimum Enclosing Circle
    # (cx,cy) -> Center coordinates
    # radius  -> Circle radius
    (cx, cy), radius = cv2.minEnclosingCircle(cnt)

    # Draw Minimum Enclosing Circle
    # image               -> Image
    # (cx,cy)             -> Center point
    # radius              -> Radius
    # (0,0,255)           -> Red color
    # 2                   -> Thickness
    cv2.circle(
        image,
        (int(cx), int(cy)),
        int(radius),
        (0, 0, 255),
        2
    )

    # Print contour measurements
    print("Area:", area)
    print("Perimeter:", perimeter)
    print("-" * 30)

cv2.imshow("Contours", image)
cv2.imwrite("Day 17/outputImages/Contours.jpg", image)
cv2.waitKey(0)
cv2.destroyAllWindows()