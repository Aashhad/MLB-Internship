import os
#Disable oneDNN optimization messages
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import seaborn as sns
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras import layers
from sklearn.metrics import confusion_matrix

# load dataset
(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
print(X_train.shape)
print(X_test.shape)

# create class names
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

# visualize display image
plt.figure(figsize=(12,6))
for i in range(10):
    plt.subplot(2,5,i+1)
    plt.imshow(X_train[i], cmap="gray")
    plt.title(class_names[y_train[i]])
    plt.axis("off")
plt.tight_layout()
plt.savefig("Day 11/genratedImages/checking_sample_predictions.png")
plt.show()

# normalize the images
X_train = X_train/255.0
X_test = X_test/255.0
# reshape the images
X_train = X_train.reshape(-1,28,28,1)
X_test = X_test.reshape(-1,28,28,1)

#  build cnn using maxpooling,filters,flatten
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

# compile the model
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
    )

# train the model
history = model.fit(
    X_train,
    y_train,
    validation_split=0.2,
    epochs=10,
    batch_size=32
)

# evaluate the model 
test_loss, test_accuracy = model.evaluate(X_test,y_test)
print(f"Test Loss : {test_loss:.4f}")
print(f"Test Accuracy : {test_accuracy:.4f}")

# plot accuracy & loss in one image
plt.figure(figsize=(12,5))

# Accuracy
plt.subplot(1,2,1)
plt.plot(history.history["accuracy"], label="Training", marker="o")
plt.plot(history.history["val_accuracy"], label="Validation", marker="o")
plt.title("Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)

# Loss
plt.subplot(1,2,2)
plt.plot(history.history["loss"], label="Training", marker="o")
plt.plot(history.history["val_loss"], label="Validation", marker="o")
plt.title("Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("Day 11/genratedImages/Accuracy_and_Loss.png")
plt.show()


# make predictions
predictions = model.predict(X_test)
predicted_labels = np.argmax(predictions,axis=1)

# visualize the sample of predictions
plt.figure(figsize=(12,6))

for i in range(10):
    plt.subplot(2,5,i+1)
    plt.imshow(X_test[i].reshape(28,28),cmap="gray")
    actual = class_names[y_test[i]]
    predicted = class_names[predicted_labels[i]]
    plt.title(f"P:{predicted}\nA:{actual}")
    plt.axis("off")
plt.tight_layout()
plt.savefig("Day 11/genratedImages/Sample_Predictions.png")
plt.show()

# confusion matrix
con_matrix=confusion_matrix(y_test,predicted_labels)
print(con_matrix)

#Visualize Confusion matrix
plt.figure(figsize=(10,8))
sns.heatmap(
    con_matrix,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=class_names,
    yticklabels=class_names
)
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")
plt.savefig("Day 11/genratedImages/Confusion_Matrix.png") 
plt.show()



# show correct predictions
correct = np.where( predicted_labels == y_test)[0]
plt.figure(figsize=(12,6))
for i,index in enumerate(correct[:10]):
    plt.subplot(2,5,i+1)
    plt.imshow(X_test[index].reshape(28,28),cmap="gray")
    plt.title(class_names[predicted_labels[index]])
    plt.axis("off")
plt.tight_layout()
plt.savefig("Day 11/genratedImages/Correct_Predictions.png")
plt.show()

# show incorrect predictions
incorrect = np.where(predicted_labels != y_test)[0]
plt.figure(figsize=(12,6))

for i,index in enumerate(incorrect[:10]):
    plt.subplot(2,5,i+1)
    plt.imshow(X_test[index].reshape(28,28),cmap="gray")
    plt.title(
        f"P:{class_names[predicted_labels[index]]}\n"
        f"A:{class_names[y_test[index]]}"
    )
    plt.axis("off")
plt.tight_layout()
plt.savefig("Day 11/genratedImages/Incorrect_Predictions.png")
plt.show()

