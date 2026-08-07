import cv2

# Read the input image
image = cv2.imread("Day 17/inputImages/shape.jpg")

# Convert the image to grayscale
# Shape detection works better on grayscale images.
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian Blur to remove noise
# Kernel Size = (5,5)
# Sigma = 0 (OpenCV calculates automatically)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Binary Threshold
# Pixels > 57 become White (255)
# Pixels <= 57 become Black (0)
_, thresh = cv2.threshold(
    gray,
    57,
    255,
    cv2.THRESH_BINARY
)

# Find contours in the threshold image
#
# thresh                -> Binary image
# cv2.RETR_EXTERNAL     -> Retrieve only outer contours
# cv2.CHAIN_APPROX_SIMPLE -> Compress contour points
contours, hierarchy = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

# Draw all detected contours in Green
#
# image     -> Image to draw on
# contours  -> List of contours
# -1        -> Draw all contours
# (0,255,0)-> Green color (BGR)
# 2         -> Thickness
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

# Loop through each detected contour
for contour in contours:
    # -----------------------------------------------
    # Approximate the contour into a polygon
    # contour                        -> Input contour
    # 0.02 * arcLength               -> Approximation accuracy
    # True                           -> Closed contour
    approx = cv2.approxPolyDP(
        contour,
        0.02 * cv2.arcLength(contour, True),
        True
    )
    # Count the number of polygon corners (vertices)
    corners = len(approx)
    # Identify the shape based on number of corners
    if corners == 3:
        shape_name = "Triangle"

    elif corners == 4:
        shape_name = "Rectangle"

    elif corners == 5:
        shape_name = "Pentagon"

    elif corners == 6:
        shape_name = "Hexagon"

    elif corners > 6:
        shape_name = "Circle"

    else:
        shape_name = "Unknown"
    # Draw the approximated polygon in Red
    #
    # image        -> Image
    # [approx]     -> Polygon contour
    # 0            -> First contour in list
    # (0,0,255)    -> Red color
    # 2            -> Thickness
    cv2.drawContours(image, [approx], 0, (0, 0, 255), 2)

    # Get the first vertex position
    # This will be used to display the shape name
    x = approx.ravel()[0]
    y = approx.ravel()[1] - 10

    # Write the detected shape name
    # image                       -> Image
    # shape_name                  -> Text
    # (x,y)                       -> Text position
    # FONT_HERSHEY_SIMPLEX        -> Font style
    # 0.5                         -> Font size
    # (0,0,255)                   -> Red color
    # 2                           -> Thickness
    cv2.putText(
        image,
        shape_name,
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 255),
        2
    )
cv2.imwrite("Day 17/outputImages/shapeDetection.jpg", image)
cv2.imshow("Shape Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()