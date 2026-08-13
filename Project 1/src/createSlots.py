import cv2
import glob
import os
import json


IMAGE_FOLDER = os.path.join(
    "Day 19",
    "dataset",
    "test",
    "images"
)

JSON_FILE = os.path.join(
    "Day 19",
    "parking_slots.json"
)

# FIND IMAGE

image_files = []

for ext in ["*.jpg", "*.jpeg", "*.png"]:
    image_files.extend(
        glob.glob(
            os.path.join(IMAGE_FOLDER, ext)
        )
    )

if len(image_files) == 0:
    print("ERROR: No images found!")
    print(os.path.abspath(IMAGE_FOLDER))
    exit()

image_path = image_files[0]

print("Selected Image:")
print(image_path)

image = cv2.imread(image_path)

if image is None:
    print("Cannot load image.")
    exit()

# LOAD EXISTING JSON

if os.path.exists(JSON_FILE):

    try:
        with open(JSON_FILE, "r") as f:
            slots = json.load(f)

        if not isinstance(slots, list):
            slots = []

    except Exception:
        slots = []

else:
    slots = []

# CURRENT SLOT
current_points = []

# MOUSE CALLBACK

def mouse_callback(event, x, y, flags, param):

    global current_points
    global slots

    if event == cv2.EVENT_LBUTTONDOWN:

        current_points.append([x, y])

        print(
            f"Point {len(current_points)}: ({x}, {y})"
        )

        # 4 points completed
        if len(current_points) == 4:

            slot = {
                "id": len(slots) + 1,
                "points": current_points.copy()
            }

            slots.append(slot)

            print()
            print("Slot Added")
            print(slot)
            print()

            current_points.clear()

# WINDOW
window_name = "Parking Slot Annotation"

cv2.namedWindow(window_name)

cv2.setMouseCallback(
    window_name,
    mouse_callback
)

# LOOP

while True:

    display = image.copy()

    # DRAW SAVED SLOTS

    for slot in slots:

        pts = slot["points"]

        for i in range(4):

            cv2.line(
                display,
                tuple(pts[i]),
                tuple(pts[(i + 1) % 4]),
                (0, 255, 0),
                2
            )

            cv2.circle(
                display,
                tuple(pts[i]),
                4,
                (0, 0, 255),
                -1
            )

        x, y = pts[0]

        cv2.putText(
            display,
            f"Slot {slot['id']}",
            (x, y - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2
        )

    # DRAW CURRENT POINTS

    for i, pt in enumerate(current_points):

        cv2.circle(
            display,
            tuple(pt),
            5,
            (255, 0, 0),
            -1
        )

        cv2.putText(
            display,
            str(i + 1),
            (pt[0] + 5, pt[1] - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 0),
            2
        )

    # Draw temporary lines
    if len(current_points) > 1:

        for i in range(len(current_points) - 1):

            cv2.line(
                display,
                tuple(current_points[i]),
                tuple(current_points[i + 1]),
                (255, 255, 0),
                2
            )

    
    # HELP BOX

    cv2.rectangle(
        display,
        (10, 10),
        (430, 90),
        (0, 0, 0),
        -1
    )

    cv2.putText(
        display,
        "Click 4 corners to add a slot",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
        display,
        "S = Save   U = Undo   C = Clear All",
        (20, 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1
    )

    cv2.putText(
        display,
        "ESC = Exit without saving",
        (20, 78),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1
    )

    cv2.imshow(window_name, display)

    key = cv2.waitKey(1) & 0xFF

    # SAVE

    if key == ord("s"):

        with open(JSON_FILE, "w") as f:
            json.dump(
                slots,
                f,
                indent=4
            )

        print()
        print("==========================")
        print("Saved Successfully")
        print("Total Slots:", len(slots))
        print(JSON_FILE)
        print("==========================")

        break

    # UNDO

    elif key == ord("u"):

        if current_points:
            current_points.pop()
            print("Removed last clicked point.")

        elif slots:
            removed = slots.pop()
            print("Removed Slot", removed["id"])

        else:
            print("Nothing to undo.")

    # CLEAR

    elif key == ord("c"):

        current_points.clear()
        slots.clear()

        print("All slots cleared.")

    # EXIT

    elif key == 27:

        print("Exited without saving.")
        break

cv2.destroyAllWindows()