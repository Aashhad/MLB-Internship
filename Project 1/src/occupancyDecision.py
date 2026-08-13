import cv2
import numpy as np


# DEFAULT SETTINGS

DEFAULT_THRESHOLD = 0.10


# AUTO CANNY

def auto_canny(gray, sigma=0.33):

    median = np.median(gray)

    lower = int(
        max(
            0,
            (1.0 - sigma) * median
        )
    )

    upper = int(
        min(
            255,
            (1.0 + sigma) * median
        )
    )

    return cv2.Canny(
        gray,
        lower,
        upper
    )


# ============================================================
# CALCULATE EDGE DENSITY FOR ONE PARKING SLOT
# ============================================================

def get_slot_edge_density(image, points):

    # Convert points to NumPy array
    polygon = np.array(
        points,
        dtype=np.int32
    )

    # Get bounding rectangle around polygon
    x, y, w, h = cv2.boundingRect(
        polygon
    )

    image_height, image_width = image.shape[:2]

    # Make sure coordinates stay inside image
    x = max(0, x)
    y = max(0, y)

    w = min(
        w,
        image_width - x
    )

    h = min(
        h,
        image_height - y
    )

    if w <= 0 or h <= 0:
        return 0.0

    # ========================================================
    # CROP SLOT
    # ========================================================

    crop = image[
        y:y + h,
        x:x + w
    ]

    # ========================================================
    # GRAYSCALE
    # ========================================================

    gray = cv2.cvtColor(
        crop,
        cv2.COLOR_BGR2GRAY
    )

    # ========================================================
    # GAUSSIAN BLUR
    # ========================================================

    blurred = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    # ========================================================
    # CANNY EDGE DETECTION
    # ========================================================

    edges = auto_canny(
        blurred
    )

    # ========================================================
    # MORPHOLOGICAL CLOSING
    # ========================================================

    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (3, 3)
    )

    edges = cv2.morphologyEx(
        edges,
        cv2.MORPH_CLOSE,
        kernel
    )

    # ========================================================
    # CREATE SLOT MASK
    # ========================================================

    mask = np.zeros(
        (h, w),
        dtype=np.uint8
    )

    # Move polygon coordinates relative to crop
    shifted_polygon = polygon.copy()

    shifted_polygon[:, 0] -= x
    shifted_polygon[:, 1] -= y

    cv2.fillPoly(
        mask,
        [shifted_polygon],
        255
    )

    # ========================================================
    # GET ONLY EDGES INSIDE SLOT
    # ========================================================

    slot_edges = cv2.bitwise_and(
        edges,
        edges,
        mask=mask
    )

    edge_pixel_count = cv2.countNonZero(
        slot_edges
    )

    slot_pixel_count = cv2.countNonZero(
        mask
    )

    if slot_pixel_count == 0:
        return 0.0

    # ========================================================
    # EDGE DENSITY
    # ========================================================

    density = (
        edge_pixel_count /
        slot_pixel_count
    )

    return density


# ============================================================
# AUTOMATIC THRESHOLD
# ============================================================

def compute_auto_threshold(ratios):

    if len(ratios) == 0:
        return DEFAULT_THRESHOLD

    scaled = np.clip(
        np.array(ratios) * 255,
        0,
        255
    ).astype(np.uint8)

    # If all slots have the same value
    if scaled.max() == scaled.min():
        return DEFAULT_THRESHOLD

    otsu_value, _ = cv2.threshold(
        scaled.reshape(-1, 1),
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return otsu_value / 255.0


# ============================================================
# CHECK OCCUPANCY
# ============================================================

def check_occupancy(
    image,
    slots,
    threshold=None
):

    ratios = []

    # ========================================================
    # CALCULATE DENSITY FOR EVERY SLOT
    # ========================================================

    for slot in slots:

        ratio = get_slot_edge_density(
            image,
            slot["points"]
        )

        # Save density inside slot
        slot["edge_ratio"] = ratio

        ratios.append(
            ratio
        )

    # ========================================================
    # DETERMINE THRESHOLD
    # ========================================================

    if threshold is None:

        used_threshold = compute_auto_threshold(
            ratios
        )

    else:

        used_threshold = threshold

    # ========================================================
    # CLASSIFY
    # ========================================================

    occupied = []
    vacant = []

    for slot in slots:

        ratio = slot["edge_ratio"]

        if ratio > used_threshold:

            occupied.append(
                slot
            )

        else:

            vacant.append(
                slot
            )

    # ========================================================
    # PRINT DEBUG INFORMATION
    # ========================================================

    print()
    print("=" * 50)
    print("PARKING OCCUPANCY ANALYSIS")
    print("=" * 50)

    print(
        f"Threshold : {used_threshold:.4f}"
    )

    print(
        f"Total     : {len(slots)}"
    )

    print(
        f"Occupied  : {len(occupied)}"
    )

    print(
        f"Vacant    : {len(vacant)}"
    )

    if len(slots) > 0:

        percentage = (
            len(occupied) /
            len(slots)
        ) * 100

    else:

        percentage = 0

    print(
        f"Occupancy : {percentage:.1f}%"
    )

    print("=" * 50)

    # Print individual slots
    print()

    for slot in slots:

        status = (
            "OCCUPIED"
            if slot["edge_ratio"] > used_threshold
            else "VACANT"
        )

        print(
            f"Slot {slot['id']:3d} | "
            f"Density: {slot['edge_ratio']:.4f} | "
            f"{status}"
        )

    print()

    return (
        occupied,
        vacant,
        used_threshold
    )