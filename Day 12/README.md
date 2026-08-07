#🐱🐶 Cats vs Dogs Image Classifier Using Transfer Learning

## 📌 Project Overview

This project is a **binary image classification system** that classifies images into two categories:

* 🐱 **Cat**
* 🐶 **Dog**

The project demonstrates the use of **Transfer Learning**, a powerful Deep Learning technique that allows a pre-trained model to be reused for a new image classification task.

Instead of training a Convolutional Neural Network (CNN) completely from scratch, this project uses **MobileNetV2**, a lightweight and efficient CNN architecture pre-trained on the **ImageNet** dataset.

The pre-trained MobileNetV2 model is used as a feature extractor, and a custom classification layer is added to classify images as either cats or dogs.

---

# 📚 Day 12 Task

## 🎯 Learning Objective

The main objective of this task was to understand **Transfer Learning** and learn how pre-trained Deep Learning models can be used to solve real-world image classification problems efficiently.

### Topics Covered

* Transfer Learning
* Pre-trained CNN models
* MobileNetV2
* Feature Extraction
* Image Preprocessing
* Data Augmentation
* Binary Image Classification
* Model Training
* Model Evaluation
* Accuracy and Loss
* Training vs Validation Performance
* Image Prediction

---

# 🧠 What is Transfer Learning?

**Transfer Learning** is a Deep Learning technique where a model that has already been trained on a large dataset is reused for a different but related task.

Training a Deep Learning model from scratch requires:

* A large amount of data
* Significant computational resources
* Long training time
* Powerful hardware

Transfer Learning allows us to reuse knowledge learned by an existing model.

A pre-trained CNN has already learned to identify general visual features such as:

* Edges
* Lines
* Shapes
* Textures
* Patterns
* Object structures

These learned features can then be reused for a new task such as classifying **cats and dogs**.

### Basic Transfer Learning Workflow

```text
Pre-trained Model
      ↓
Reuse Learned Features
      ↓
Add Custom Classification Layer
      ↓
Train on New Dataset
      ↓
Evaluate Model
      ↓
Make Predictions
```

---

# 📊 Dataset

This project uses a **Cats vs Dogs image dataset downloaded using a dataset URL**.

The dataset contains images belonging to two classes:

| Class  | Description    |
| ------ | -------------- |
| 🐱 Cat | Images of cats |
| 🐶 Dog | Images of dogs |

The dataset is obtained from the provided dataset URL and then loaded and processed for training.

### Dataset Workflow

```text
Dataset URL
    ↓
Download Dataset
    ↓
Extract Dataset
    ↓
Organize Images
    ↓
Create Training Dataset
    ↓
Create Validation Dataset
    ↓
Preprocess Images
    ↓
Train Model
```

The dataset contains two main categories:

```text
cats/
    ├── cat_image_1
    ├── cat_image_2
    ├── cat_image_3
    └── ...

dogs/
    ├── dog_image_1
    ├── dog_image_2
    ├── dog_image_3
    └── ...
```

> **Note:** The exact dataset URL can be added to this README in the section below.

### Dataset URL

```text
"https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_5340.zip"

```

---

# 🛠️ Technologies Used

The project was developed using the following technologies:

### Programming Language

* Python

### Deep Learning Framework

* TensorFlow
* Keras

### Model

* MobileNetV2

### Data Processing

* NumPy

### Visualization

* Matplotlib

### Dataset

* Cats vs Dogs Dataset
* Dataset imported/downloaded using a URL

---

# 📦 Libraries Used

```python
import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
```

For MobileNetV2 preprocessing, the following can also be used:

```python
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
```

---

# ⚙️ Project Configuration

The project uses the following configuration:

```python
IMG_SIZE = 160
BATCH_SIZE = 32
EPOCHS = 10
```

### Configuration Explanation

| Parameter    | Value | Description                              |
| ------------ | ----: | ---------------------------------------- |
| `IMG_SIZE`   |   160 | Images are resized to 160 × 160 pixels   |
| `BATCH_SIZE` |    32 | Number of images processed in each batch |
| `EPOCHS`     |    10 | Number of complete training cycles       |

---

# 🔄 Image Preprocessing

Images in the dataset may have different sizes and dimensions.

Before feeding them into MobileNetV2, the images are resized to a consistent size:

```text
160 × 160 pixels
```

The images are then converted into tensors and preprocessed before being passed to the model.

### Preprocessing Workflow

```text
Original Image
      ↓
Resize Image
      ↓
Convert to Tensor
      ↓
Preprocess / Normalize
      ↓
Input to MobileNetV2
```

---

# 🔀 Data Augmentation

Data augmentation is used to create variations of existing training images.

It helps the model generalize better and reduces the risk of **overfitting**.

Example:

```python
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])
```

Common augmentation techniques include:

* Random horizontal flipping
* Random rotation
* Random zoom
* Random contrast

### Why Data Augmentation?

Without augmentation:

```text
Training Images
      ↓
Model Memorizes Training Data
      ↓
Poor Performance on New Images
      ↓
Overfitting
```

With augmentation:

```text
Training Images
      ↓
Random Transformations
      ↓
More Diverse Training Examples
      ↓
Better Generalization
```

---

# 🧠 MobileNetV2

This project uses **MobileNetV2** as the base model.

MobileNetV2 is a lightweight Convolutional Neural Network architecture designed for efficient image classification and Computer Vision applications.

It is particularly useful when computational resources are limited.

The model was pre-trained on the **ImageNet** dataset.

### Why MobileNetV2?

MobileNetV2 was selected because it:

* Is lightweight
* Requires fewer computational resources
* Provides good image classification performance
* Is suitable for Transfer Learning
* Trains faster than many larger CNN architectures
* Can be used in mobile and edge applications

---

# 🔄 Transfer Learning Process

The Transfer Learning process consists of the following steps:

```text
Dataset
    ↓
Image Preprocessing
    ↓
Data Augmentation
    ↓
Pre-trained MobileNetV2
    ↓
Freeze Base Model
    ↓
Add Custom Classification Head
    ↓
Compile Model
    ↓
Train Model
    ↓
Evaluate Model
    ↓
Predict Cat or Dog
```

---



# 🧪 Complete Project Workflow

```text
1. Get Cats vs Dogs Dataset URL
            ↓
2. Download Dataset
            ↓
3. Extract and Organize Dataset
            ↓
4. Load Images
            ↓
5. Create Training and Validation Sets
            ↓
6. Resize Images
            ↓
7. Preprocess Images
            ↓
8. Apply Data Augmentation
            ↓
9. Load MobileNetV2
            ↓
10. Load ImageNet Pre-trained Weights
            ↓
11. Remove Original Classification Head
            ↓
12. Freeze Base Model
            ↓
13. Add Custom Classification Layer
            ↓
14. Compile Model
            ↓
15. Train Model
            ↓
16. Evaluate Model
            ↓
17. Visualize Accuracy and Loss
            ↓
18. Predict New Images
```

---

# 🌟 Key Learnings

Through this project, I learned:

* What Transfer Learning is
* Why Transfer Learning is useful
* How to use a pre-trained CNN
* How to use MobileNetV2
* How to download and use a dataset from a URL
* How to prepare image datasets
* How to preprocess image data
* How to resize images
* How to apply Data Augmentation
* How to freeze pre-trained model layers
* How to add custom classification layers
* How to compile a Deep Learning model
* How to train an image classifier
* How to evaluate model performance
* How to visualize training and validation metrics
* How to perform predictions on new images

---

# 🚀 Future Improvements

The project can be improved in several ways.

### 1. Fine-Tuning

Some of the upper MobileNetV2 layers can be unfrozen after initial training and trained with a small learning rate.

This can help the model adapt more specifically to the Cats vs Dogs dataset.

### 2. More Data Augmentation

Additional techniques can be tested:

* Random contrast
* Random brightness
* Random translation
* Random rotation

### 3. Hyperparameter Tuning

Different values can be tested for:

* Learning rate
* Batch size
* Dropout
* Number of epochs

### 4. Model Comparison

Other pre-trained models can be compared with MobileNetV2:

* ResNet50
* EfficientNet
* VGG16
* InceptionV3

### 5. Deployment

The trained model can be deployed as:

* Streamlit Web App
* Flask API
* FastAPI Application
* TensorFlow Lite Mobile Application

---

# 🌍 Real-World Applications

The concepts learned in this project can be applied to:

* Animal classification
* Medical image classification
* Plant disease detection
* Object classification
* Product classification
* Quality inspection
* Wildlife monitoring
* Agricultural image analysis

---

# 🎓 Conclusion

This project demonstrates how **Transfer Learning** can be used to build an effective image classification system without training a large CNN completely from scratch.

Using **MobileNetV2**, a model pre-trained on ImageNet, the project reuses previously learned visual features and adapts them to the task of classifying cats and dogs.

The project provided practical experience with:

```text
Deep Learning
      +
CNNs
      +
Transfer Learning
      +
MobileNetV2
      +
Data Augmentation
      +
Image Classification
```

This project was an important step toward understanding how modern Deep Learning and Computer Vision models are developed and applied to real-world problems.

---


You can include:

* Dataset samples
* Model summary
* Training output
* Accuracy graph
* Loss graph
* Cat prediction
* Dog prediction

---

# 👨‍💻 Author

**Ashhad**
