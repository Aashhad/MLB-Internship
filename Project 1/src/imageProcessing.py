import cv2


def preprocess(image):

    # Grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # Gaussian Blur
    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    # Canny Edge Detection
    edges = cv2.Canny(
        blur,
        50,
        150
    )

    # Morphological Closing
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (3, 3)
    )

    processed = cv2.morphologyEx(
        edges,
        cv2.MORPH_CLOSE,
        kernel
    )

    return processed