import json
import os


def load_slots():

    file_path = os.path.join(
        "Project 1",
        "annotation",
        "parking_slots.json"
    )

    # Check file
    if not os.path.exists(file_path):

        raise FileNotFoundError(
            "parking_slots.json not found!"
        )

    # Check empty file
    if os.path.getsize(file_path) == 0:

        raise ValueError(
            "parking_slots.json is empty. "
            "It should contain [] or parking slots."
        )

    # Load JSON
    with open(
        file_path,
        "r"
    ) as file:

        slots = json.load(file)


    # Check format
    if not isinstance(slots, list):

        raise ValueError(
            "parking_slots.json must contain a list."
        )


    return slots