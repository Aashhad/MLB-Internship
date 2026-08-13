import cv2
import glob
import os

from src.slotDetection import load_slots
from src.occupancyDecision import check_occupancy
from src.visualization import draw


OCCUPANCY_THRESHOLD = 0.10

IMAGE_FOLDER = os.path.join(
    "Project 1",
    "dataset",
    "inputImages"
)

# Output folder
OUTPUT_FOLDER = os.path.join(
    "Project 1",
    "dataset",
    "outputImages"
)



# CREATE OUTPUT FOLDER

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


# FIND ALL IMAGES

image_files = []

for extension in [
    "*.jpg",
    "*.jpeg",
    "*.png",
    "*.JPG",
    "*.JPEG",
    "*.PNG"
]:

    image_files.extend(
        glob.glob(
            os.path.join(
                IMAGE_FOLDER,
                extension
            )
        )
    )


# CHECK IMAGES

if len(image_files) == 0:

    print()
    print("ERROR: No images found!")

    print(
        "Looking in:"
    )

    print(
        os.path.abspath(
            IMAGE_FOLDER
        )
    )

    print()

    exit()


# SORT IMAGES

image_files = sorted(
    image_files
)


print()
print("SMART PARKING LOT OCCUPANCY ANALYZER")

print(
    "Image folder:",
    os.path.abspath(IMAGE_FOLDER)
)

print(
    "Total images found:",
    len(image_files)
)

print()


# LOAD PARKING SLOTS

try:

    slots = load_slots()

except Exception as error:

    print()
    print("ERROR: Could not load parking slots")

    print(
        "Error:",
        error
    )

    exit()


# CHECK PARKING SLOTS

print(
    "Parking slots:",
    len(slots)
)

if len(slots) == 0:

    print()
    print("WARNING: No parking slots found.")
    print()
    print(
        "Run createSlots.py first."
    )

    exit()


print()
print("Parking slots loaded successfully.")
print()


# PROCESS EACH IMAGE

all_summaries = []


for image_index, image_path in enumerate(
    image_files,
    start=1
):

    print()
    print()
    print("==========================================")
    print(
        f"PROCESSING IMAGE {image_index}/{len(image_files)}"
    )
    print("==========================================")

    print(
        "Image:",
        image_path
    )

    # READ IMAGE

    image = cv2.imread(
        image_path
    )

    if image is None:

        print(
            "ERROR: Could not load image."
        )

        continue


    # OCCUPANCY DETECTION

    try:

        occupied, vacant, used_threshold = check_occupancy(
            image,
            slots,
            threshold=OCCUPANCY_THRESHOLD
        )

    except Exception as error:

        print()
        print(
            "ERROR during occupancy detection:"
        )

        print(
            error
        )

        continue


    # COUNTS

    total_slots = len(slots)

    occupied_count = len(
        occupied
    )

    vacant_count = len(
        vacant
    )


    if total_slots > 0:

        occupancy_percentage = (
            occupied_count /
            total_slots
        ) * 100

    else:

        occupancy_percentage = 0


    # SLOT IDs

    occupied_ids = sorted(
        slot["id"]
        for slot in occupied
    )

    vacant_ids = sorted(
        slot["id"]
        for slot in vacant
    )


    # PRINT RESULTS

    print()
    print("RESULT")

    print(
        "Total Slots:",
        total_slots
    )

    print(
        "Occupied:",
        occupied_count
    )

    print(
        "Vacant:",
        vacant_count
    )

    print(
        "Occupancy:",
        f"{occupancy_percentage:.1f}%"
    )

    print(
        "Threshold:",
        round(
            used_threshold,
            4
        )
    )

    print()

    print(
        "Occupied Slot IDs:"
    )

    print(
        occupied_ids
    )

    print()

    print(
        "Vacant Slot IDs:"
    )

    print(
        vacant_ids
    )



    # DRAW RESULT
    try:

        result = draw(
            image.copy(),
            occupied,
            vacant,
            threshold=used_threshold
        )

    except TypeError:

        # If your visualization.py does not have
        # the threshold parameter, use this version.

        result = draw(
            image.copy(),
            occupied,
            vacant
        )


    # GET ORIGINAL IMAGE NAME

    image_name = os.path.basename(
        image_path
    )

    image_name_without_extension = os.path.splitext(
        image_name
    )[0]


    # OUTPUT IMAGE PATH

    output_image_path = os.path.join(
        OUTPUT_FOLDER,
        f"{image_name_without_extension}_result.jpg"
    )


    # SAVE RESULT IMAGE

    saved = cv2.imwrite(
        output_image_path,
        result
    )

    if saved:

        print()
        print(
            "Result saved:"
        )

        print(
            output_image_path
        )

    else:

        print(
            "ERROR: Could not save result image."
        )


    # SAVE INDIVIDUAL SUMMARY

    summary_path = os.path.join(
        OUTPUT_FOLDER,
        f"{image_name_without_extension}_summary.txt"
    )


    with open(
        summary_path,
        "w",
        encoding="utf-8"
    ) as summary_file:

        summary_file.write(
            "SMART PARKING LOT OCCUPANCY ANALYZER\n"
        )

        summary_file.write(
            "========================================\n\n"
        )

        summary_file.write(
            f"Image: {image_path}\n"
        )

        summary_file.write(
            f"Total Slots: {total_slots}\n"
        )

        summary_file.write(
            f"Occupied: {occupied_count}\n"
        )

        summary_file.write(
            f"Vacant: {vacant_count}\n"
        )

        summary_file.write(
            f"Occupancy: {occupancy_percentage:.1f}%\n"
        )

        summary_file.write(
            f"Threshold: {used_threshold:.4f}\n\n"
        )

        summary_file.write(
            f"Occupied Slot IDs ({occupied_count}):\n"
        )

        summary_file.write(
            f"{occupied_ids}\n\n"
        )

        summary_file.write(
            f"Vacant Slot IDs ({vacant_count}):\n"
        )

        summary_file.write(
            f"{vacant_ids}\n"
        )


    print(
        "Summary saved:",
        summary_path
    )


    # STORE SUMMARY

    all_summaries.append(
        {
            "image": image_name,
            "total": total_slots,
            "occupied": occupied_count,
            "vacant": vacant_count,
            "occupancy": occupancy_percentage,
            "threshold": used_threshold
        }
    )


    # DISPLAY RESULT

    window_name = (
        f"Parking Result - {image_name}"
    )

    cv2.imshow(
        window_name,
        result
    )

    print()
    print(
        "Press any key to continue to next image..."
    )

    cv2.waitKey(0)

    cv2.destroyAllWindows()


# SAVE OVERALL SUMMARY

overall_summary_path = os.path.join(
    OUTPUT_FOLDER,
    "all_images_summary.txt"
)


with open(
    overall_summary_path,
    "w",
    encoding="utf-8"
) as summary_file:

    summary_file.write(
        "SMART PARKING LOT OCCUPANCY ANALYZER\n"
    )

    summary_file.write(
        "ALL IMAGES SUMMARY\n"
    )

    summary_file.write(
        "==========================================\n\n"
    )


    for item in all_summaries:

        summary_file.write(
            f"Image: {item['image']}\n"
        )

        summary_file.write(
            f"Total Slots: {item['total']}\n"
        )

        summary_file.write(
            f"Occupied: {item['occupied']}\n"
        )

        summary_file.write(
            f"Vacant: {item['vacant']}\n"
        )

        summary_file.write(
            f"Occupancy: {item['occupancy']:.1f}%\n"
        )

        summary_file.write(
            f"Threshold: {item['threshold']:.4f}\n"
        )

        summary_file.write(
            "------------------------------------------\n"
        )


# FINAL MESSAGE

print()
print("ALL IMAGES PROCESSED")

print(
    "Images processed:",
    len(all_summaries)
)

print(
    "Output folder:",
    os.path.abspath(
        OUTPUT_FOLDER
    )
)

print(
    "Overall summary:",
    overall_summary_path
)

print("==========================================")