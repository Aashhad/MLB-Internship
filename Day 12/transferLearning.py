import os
import pathlib
import tensorflow as tf
# from tensorflow.keras.applications import MobileNetV2
# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
# from tensorflow.keras import layers, models

#Constants

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
AUTOTUNE = tf.data.AUTOTUNE


#Load Pre-trained MobileNetV2

base_model = MobileNetV2(
    input_shape=IMG_SIZE + (3,),
    include_top=False,
    weights="imagenet"
)

#Explore Architecture

print(f"\nTotal Layers : {len(base_model.layers)}")

print("\nFirst 5 Layers")
for layer in base_model.layers[:5]:
    print(f"{layer.name:30} {layer.__class__.__name__}")

print("\nLast 5 Layers")
for layer in base_model.layers[-5:]:
    print(f"{layer.name:30} {layer.__class__.__name__}")

print(f"\nTotal Parameters : {base_model.count_params():,}")

base_model.summary()

#Freeze Base Model
base_model.trainable = False

print("\nBase Model Trainable:", base_model.trainable)

#Add Custom Classification Head

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.2),
    layers.Dense(1, activation="sigmoid")
])

print("\nCustom Model Summary\n")
model.summary()
print("LOAD CATS VS DOGS DATASET")


#Dataset URL

_URL = ("https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_5340.zip")

#Download Dataset

path_to_zip = tf.keras.utils.get_file(
    "cats_and_dogs.zip",
    origin=_URL,
    extract=True
)

#Locate Dataset Folder

dataset_root = pathlib.Path(path_to_zip).parent

data_dir = None

for root, dirs, files in os.walk(dataset_root):
    if "Cat" in dirs and "Dog" in dirs:
        data_dir = pathlib.Path(root)
        break

if data_dir is None:
    raise FileNotFoundError("Cat and Dog folders were not found.")

print(f"\nDataset Found At:\n{data_dir}")

#Remove Corrupted Images

num_skipped = 0

for category in ["Cat", "Dog"]:

    folder = data_dir / category

    for file_name in os.listdir(folder):

        file_path = folder / file_name

        try:
            with open(file_path, "rb") as f:
                is_jfif = b"JFIF" in f.peek(10)
        except Exception:
            is_jfif = False

        if not is_jfif:
            num_skipped += 1
            os.remove(file_path)

print(f"\nRemoved {num_skipped} corrupted images.")

#Load Dataset

train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

print("\nClass Names:", train_ds.class_names)

#Preprocess Images

train_ds = (
    train_ds
    .map(lambda x, y: (preprocess_input(x), y))
    .prefetch(AUTOTUNE)
)

val_ds = (
    val_ds
    .map(lambda x, y: (preprocess_input(x), y))
    .prefetch(AUTOTUNE)
)

print("\nDataset Information")
print("Image Size      :", IMG_SIZE)
print("Batch Size      :", BATCH_SIZE)
print("\nImages resized and preprocessed successfully.")
print("Dataset is ready for transfer learning with MobileNetV2.")