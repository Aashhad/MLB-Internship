import cv2
import os 

# Global Variables
current_image = None
OUTPUT_FOLDER = os.path.join("Day 14", "outputImages")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# Helper Function
def check_image():
    if current_image is None:
        print("Please load an image first.")
        return False
    return True


# Load Image
def open_image():
    global current_image

    image_path = input("Enter image path: ")

    current_image = cv2.imread(image_path)

    if current_image is None:
        print("Image not found.")
    else:
        print("Image loaded successfully.")


# Convert to Gray
def convert_to_grayscale():
    global current_image

    if not check_image():
        return

    gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
    current_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    print("Converted to grayscale.")


# Resize
def resize_image():
    global current_image

    if not check_image():
        return

    new_width = int(input("Enter width: "))
    new_height = int(input("Enter height: "))

    current_image = cv2.resize(current_image, (new_width, new_height))

    print("Image resized successfully.")



# Rotate
def rotate_image():
    global current_image

    if not check_image():
        return

    print("\n1. Rotate 90°")
    print("2. Rotate 180°")
    print("3. Rotate 270°")

    option = input("Enter choice: ")

    if option == "1":
        current_image = cv2.rotate(current_image, cv2.ROTATE_90_CLOCKWISE)

    elif option == "2":
        current_image = cv2.rotate(current_image, cv2.ROTATE_180)

    elif option == "3":
        current_image = cv2.rotate(current_image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    else:
        print("Invalid choice.")
        return

    print("Image rotated successfully.")


# Flip
def flip_current_image():
    global current_image

    if not check_image():
        return

    print("\n1. Horizontal")
    print("2. Vertical")
    print("3. Both")

    option = input("Enter choice: ")

    if option == "1":
        current_image = cv2.flip(current_image, 1)

    elif option == "2":
        current_image = cv2.flip(current_image, 0)

    elif option == "3":
        current_image = cv2.flip(current_image, -1)

    else:
        print("Invalid choice.")
        return

    print("Image flipped successfully.")


# Crop
def crop_current_image():
    global current_image

    if not check_image():
        return

    start_x = int(input("Enter X: "))
    start_y = int(input("Enter Y: "))
    crop_width = int(input("Enter Width: "))
    crop_height = int(input("Enter Height: "))

    current_image = current_image[start_y:start_y + crop_height,
                                  start_x:start_x + crop_width]

    print("Image cropped successfully.")


# Draw Shapes
def draw_on_image():
    global current_image

    if not check_image():
        return

    print("\n1. Rectangle")
    print("2. Circle")
    print("3. Line")

    option = input("Enter choice: ")

    if option == "1":

        x1 = int(input("x1: "))
        y1 = int(input("y1: "))
        x2 = int(input("x2: "))
        y2 = int(input("y2: "))

        blue = int(input("Blue: "))
        green = int(input("Green: "))
        red = int(input("Red: "))

        thickness = int(input("Thickness: "))

        cv2.rectangle(
            current_image,
            (x1, y1),
            (x2, y2),
            (blue, green, red),
            thickness
        )

    elif option == "2":

        center_x = int(input("Center X: "))
        center_y = int(input("Center Y: "))
        radius = int(input("Radius: "))

        blue = int(input("Blue: "))
        green = int(input("Green: "))
        red = int(input("Red: "))

        thickness = int(input("Thickness: "))

        cv2.circle(
            current_image,
            (center_x, center_y),
            radius,
            (blue, green, red),
            thickness
        )

    elif option == "3":

        x1 = int(input("x1: "))
        y1 = int(input("y1: "))
        x2 = int(input("x2: "))
        y2 = int(input("y2: "))

        blue = int(input("Blue: "))
        green = int(input("Green: "))
        red = int(input("Red: "))

        thickness = int(input("Thickness: "))

        cv2.line(
            current_image,
            (x1, y1),
            (x2, y2),
            (blue, green, red),
            thickness
        )

    else:
        print("Invalid choice.")
        return

    print("Shape drawn successfully.")


# Add Text
def write_text():
    global current_image

    if not check_image():
        return

    user_text = input("Enter text: ")

    pos_x = int(input("X Position: "))
    pos_y = int(input("Y Position: "))

    blue = int(input("Blue: "))
    green = int(input("Green: "))
    red = int(input("Red: "))

    thickness = int(input("Thickness: "))

    cv2.putText(
        current_image,
        user_text,
        (pos_x, pos_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (blue, green, red),
        thickness
    )

    print("Text added successfully.")


# Preview
def show_image():
    global current_image

    if not check_image():
        return

    cv2.imshow("Image Preview", current_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def save_current_image():
    global current_image

    if not check_image():
        return

    filename = input("Enter file name (example: image.jpg): ").strip()

    # Automatically add .jpg if user doesn't provide extension
    if "." not in filename:
        filename += ".jpg"

    save_path = os.path.abspath(os.path.join(OUTPUT_FOLDER, filename))

    success = cv2.imwrite(save_path, current_image)

    if success:
        print(f"\nImage saved successfully.")
        print(f"Location: {save_path}")
    else:
        print("Failed to save image.")


# Delete
def remove_saved_image():

    filename = input("Enter filename to delete: ")

    delete_path = os.path.join(OUTPUT_FOLDER, filename)

    if os.path.exists(delete_path):
        os.remove(delete_path)
        print("Image deleted successfully.")
    else:
        print("File not found.")



# Main Menu
while True:

    print("\n" + "=" * 20)
    print(" IMAGE PROCESSING TOOLKIT ")
    print("=" * 20)

    print("1. Load Image")
    print("2. Grayscale")
    print("3. Resize")
    print("4. Rotate")
    print("5. Flip")
    print("6. Crop")
    print("7. Draw Shape")
    print("8. Add Text")
    print("9. Preview Image")
    print("10. Save Image")
    print("11. Delete Image")
    print("0. Exit")

    user_choice = input("\nEnter your choice: ")

    if user_choice == "1":
        open_image()

    elif user_choice == "2":
        convert_to_grayscale()

    elif user_choice == "3":
        resize_image()

    elif user_choice == "4":
        rotate_image()

    elif user_choice == "5":
        flip_current_image()

    elif user_choice == "6":
        crop_current_image()

    elif user_choice == "7":
        draw_on_image()

    elif user_choice == "8":
        write_text()

    elif user_choice == "9":
        show_image()

    elif user_choice == "10":
        save_current_image()

    elif user_choice == "11":
        remove_saved_image()

    elif user_choice == "0":
        print("Thank you for using Image Processing Toolkit.")
        break

    else:
        print("Invalid choice. Try again.")
