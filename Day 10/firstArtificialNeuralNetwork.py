import os
# Disable oneDNN optimizations
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.layers import Flatten

# load the dataset
(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()

# Explore the data set
print("X_train shape:", X_train.shape)
print("y_train shape:", y_train.shape)

print("X_test shape:", X_test.shape)
print("y_test shape:", y_test.shape)


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

print("First label:", y_train[0])
print("Class name:", class_names[y_train[0]])

plt.imshow(X_train[0], cmap="gray")
plt.title(class_names[y_train[0]])
plt.axis("off")
plt.savefig("DAY 10/predicted sample.png",dpi=300)
plt.show()

# Normalize the pixel value
X_train = X_train / 255.0
X_test = X_test / 255.0


# Build ANN model

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dense(10, activation="softmax")
])

model.summary()

# Compile the model
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Train the model
history = model.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2
)
predictions = model.predict(X_test)


# Ealuate the model
test_loss, test_accuracy = model.evaluate(X_test,y_test)
print("Test Loss:", test_loss)
print("Test Accuracy:", test_accuracy)

# training and validation accuracy
print(f"Final Training Accuracy: {history.history['accuracy'][-1]:.4f}")
print(f"Final Validation Accuracy: {history.history['val_accuracy'][-1]:.4f}")


# plot accuracy
plt.plot(history.history["accuracy"],label="Training Accuracy", marker = "o")
plt.plot(history.history["val_accuracy"],label="Validation Accuracy", marker = "o")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("Training vs Validation Accuracy")
plt.grid(True)
plt.savefig("DAY 10/Training vs Validation Accuracy.png",dpi=300)
plt.legend()
plt.show()

# predcictions of the models
predictions = model.predict(X_test[:10])
predicted_labels = predictions.argmax(axis=1)
for i in range(10):
    print(
        "Image:", i,
        "| Actual:",class_names[y_test[i]],
        "| Predicted:",class_names[predicted_labels[i]]
        )
    
# Display predictions images
plt.figure(figsize=(12, 6))

for i in range(10):
    plt.subplot(2, 5, i + 1)
    plt.imshow(X_test[i], cmap="gray")
    actual = class_names[y_test[i]]
    predicted = class_names[predicted_labels[i]]
    plt.title(f"Actual: {actual}\nPredicted: {predicted}")

plt.axis("off")
plt.savefig("DAY 10/Top 10 predicted images.png",dpi=300)
plt.tight_layout()
plt.show()