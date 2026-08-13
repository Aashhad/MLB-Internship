import cv2
import numpy as np


# DRAW RESULT

def draw(
    image,
    occupied,
    vacant,
    threshold=None,
    show_labels=False
):

    overlay = image.copy()

    # Fill Vacant Slots (Green tint)

    for slot in vacant:

        pts = np.array(
            slot["points"],
            dtype=np.int32
        )

        cv2.fillPoly(
            overlay,
            [pts],
            (0, 200, 0)
        )

    # Fill Occupied Slots (Red tint)

    for slot in occupied:

        pts = np.array(
            slot["points"],
            dtype=np.int32
        )

        cv2.fillPoly(
            overlay,
            [pts],
            (0, 0, 200)
        )

    # Blend the tinted overlay onto the original image
    image = cv2.addWeighted(
        overlay,
        0.35,
        image,
        0.65,
        0
    )

    # Borders on top of the tint

    for slot in vacant:

        pts = np.array(
            slot["points"],
            dtype=np.int32
        )

        cv2.polylines(
            image,
            [pts],
            True,
            (0, 255, 0),
            1
        )

    for slot in occupied:

        pts = np.array(
            slot["points"],
            dtype=np.int32
        )

        cv2.polylines(
            image,
            [pts],
            True,
            (0, 0, 255),
            1
        )

    # Optional tiny ID labels (small lots only)

    if show_labels:

        for slot in vacant + occupied:

            pts = np.array(
                slot["points"],
                dtype=np.int32
            )

            center = pts.mean(axis=0).astype(int)

            cv2.putText(
                image,
                str(slot["id"]),
                (center[0] - 6, center[1] + 4),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.35,
                (255, 255, 255),
                1
            )


    total = len(occupied) + len(vacant)
    occupied_count = len(occupied)
    vacant_count = len(vacant)

    if total > 0:
        percentage = occupied_count * 100 / total
    else:
        percentage = 0

    # Background Panel

    cv2.rectangle(
        image,
        (5, 5),
        (150, 155),
        (0, 0, 0),
        -1
    )

    # Text

    cv2.putText(
        image,
        f"Total Slots : {total}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.4,
        (255, 255, 255),
        2
    )

    cv2.putText(
        image,
        f"Occupied : {occupied_count}",
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.4,
        (0, 0, 255),
        2
    )

    cv2.putText(
        image,
        f"Vacant : {vacant_count}",
        (20, 95),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.4,
        (0, 255, 0),
        2
    )

    cv2.putText(
        image,
        f"Occupancy : {percentage:.1f}%",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        2
    )

    if threshold is not None:

        cv2.putText(
            image,
            f"Threshold : {threshold:.3f}",
            (20, 145),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (200, 200, 200),
            1
        )

    return image