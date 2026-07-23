import os

#Disable oneDNN optimization messages
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras import layers


#Load Fashion-MNIST Dataset
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()

print("Training Images Shape:", X_train.shape)
print("Training Labels Shape:", y_train.shape)

print("Testing Images Shape:", X_test.shape)
print("Testing Labels Shape:", y_test.shape)


class_names = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot"
]



#Visualize 10 Sample Images

plt.figure(figsize=(12, 6))
for i in range(10):
    plt.subplot(2, 5, i + 1)
    plt.imshow(X_train[i], cmap="gray")
    plt.title(class_names[y_train[i]])
    plt.axis("off")
plt.tight_layout()
plt.show()


#Normalize Dataset

# Pixel values are originally between 0 and 255.
# We convert them to values between 0 and 1.

X_train = X_train / 255.0
X_test = X_test / 255.0
print("Minimum Pixel Value:", X_train.min())
print("Maximum Pixel Value:", X_train.max())


# Reshape Data for CNN
X_train = X_train.reshape(-1, 28, 28, 1)
X_test = X_test.reshape(-1, 28, 28, 1)

print("New Training Shape:", X_train.shape)
print("New Testing Shape:", X_test.shape)


#Build CNN Model

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(28, 28, 1)),
    tf.keras.layers.Conv2D(filters=32,kernel_size=(3, 3),activation="relu"),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Conv2D(filters=64,kernel_size=(3, 3),activation="relu"),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128,activation="relu"),
    tf.keras.layers.Dense(10,activation="softmax")
])

model.summary()



#Compile the Model

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


#Train the Model
history = model.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2
)
# Make Predictions
predictions = model.predict(X_test[:10])

# Get the predicted class number
predicted_labels = np.argmax(predictions,axis=1)

#Display Predictions
plt.figure(figsize=(12, 6))

for i in range(10):
    plt.subplot(2, 5, i + 1)
    plt.imshow(X_test[i].reshape(28, 28),cmap="gray")
    actual_label = class_names[y_test[i]]
    predicted_label = class_names[predicted_labels[i]]
    plt.title(f"Actual: {actual_label}\n"f"Predicted: {predicted_label}")
plt.axis("off")
plt.tight_layout()
plt.show()

#Model Evaluation Final Training Accuracy
final_training_accuracy = history.history["accuracy"][-1]
print(f"Final Training Accuracy: {final_training_accuracy:.4f}")


# Evaluate on Test Dataset
test_loss, test_accuracy = model.evaluate(
    X_test,
    y_test,
    verbose=1
)
print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")



plt.figure(figsize=(12, 5))
#Accuracy Graph
plt.subplot(1, 2, 1)
plt.plot(history.history["accuracy"],label="Training Accuracy",  marker="o")
plt.plot(history.history["val_accuracy"],label="Validation Accuracy",  marker="o")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("Training vs Validation Accuracy")
plt.legend()
plt.grid(True)


#Loss Graph
plt.subplot(1, 2, 2)
plt.plot(history.history["loss"],label="Training Loss",  marker="o")
plt.plot(history.history["val_loss"],label="Validation Loss",  marker="o")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training vs Validation Loss")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

