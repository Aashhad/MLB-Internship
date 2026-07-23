# Day-11: Fashion MNIST Image Classification using Convolutional Neural Networks (CNN)

## 📌 Project Overview

This project demonstrates the implementation of a **Convolutional Neural Network (CNN)** using **TensorFlow/Keras** to classify clothing images from the **Fashion MNIST** dataset.

The project covers the complete deep learning workflow, including data preprocessing, CNN model development, training, evaluation, prediction, visualization, and performance analysis.

---

# 🎯 Objectives

- Understand the architecture of Convolutional Neural Networks (CNNs).
- Learn why CNNs perform better than Artificial Neural Networks (ANNs) for image classification.
- Build and train a CNN using TensorFlow/Keras.
- Classify clothing images from the Fashion MNIST dataset.
- Evaluate the model using accuracy, loss, and a confusion matrix.
- Visualize correctly and incorrectly classified images.

---

# 📚 Concepts Covered

## Convolutional Neural Networks (CNN)

- Convolution Layer
- Filters (Kernels)
- Feature Maps
- Max Pooling Layer
- Average Pooling (Concept)
- Flatten Layer
- Fully Connected (Dense) Layer

## Image Classification

- Image Classification Workflow
- Training & Validation Data
- Epochs
- Batch Size
- Overfitting
- Data Augmentation (Concept)
- Model Evaluation

---

# 🧠 Why CNNs are Better than ANNs for Images

Artificial Neural Networks (ANNs) convert images into one-dimensional vectors, causing the loss of important spatial information between pixels.

Convolutional Neural Networks (CNNs) preserve this spatial information by applying convolution operations that automatically learn meaningful visual features such as:

- Edges
- Shapes
- Textures
- Patterns
- Object Parts

Compared to ANNs, CNNs:

- Learn image features automatically
- Require fewer trainable parameters
- Reduce overfitting through pooling
- Achieve higher accuracy on image classification tasks

---

# 📂 Dataset

**Dataset:** Fashion MNIST

The Fashion MNIST dataset contains grayscale images of clothing items.

- Training Images: **60,000**
- Testing Images: **10,000**
- Image Size: **28 × 28**
- Number of Classes: **10**

### Classes

- T-shirt/Top
- Trouser
- Pullover
- Dress
- Coat
- Sandal
- Shirt
- Sneaker
- Bag
- Ankle Boot

---

# 🏗️ CNN Model Architecture

The implemented CNN architecture consists of:

```
Input Layer (28 × 28 × 1)

↓

Conv2D
32 Filters
3 × 3 Kernel
ReLU

↓

MaxPooling2D
2 × 2

↓

Conv2D
64 Filters
3 × 3 Kernel
ReLU

↓

MaxPooling2D
2 × 2

↓

Flatten

↓

Dense
128 Neurons
ReLU

↓

Output Layer
10 Neurons
Softmax
```

---

# ⚙️ Project Workflow

```
Load Fashion MNIST Dataset
            │
            ▼
Display Sample Images
            │
            ▼
Normalize Images
            │
            ▼
Reshape Images
            │
            ▼
Build CNN Model
            │
            ▼
Compile Model
            │
            ▼
Train Model
            │
            ▼
Evaluate Model
            │
            ▼
Generate Predictions
            │
            ▼
Confusion Matrix
            │
            ▼
Correct & Incorrect Predictions
```

---

# 🛠️ Technologies Used

- Python
- TensorFlow
- Keras
- NumPy
- Matplotlib
- Scikit-learn

---

# 📁 Project Structure

```
Day-11/
│
├── generatedImages/
│   ├── training_graph.png
│   ├── confusion_matrix.png
│   ├── sample_predictions.png
│   ├── correct_predictions.png
│   └── incorrect_predictions.png
│
├── CNN.py
├── fashionMNISTimageClassifier.py
├── requirements.txt
└── README.md
```

---

# 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/MLB-Internship.git
```

### 2. Navigate to the Project Folder

```bash
cd MLB-Internship/Day-11
```

### 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 4. Run the CNN Classifier

```bash
python fashionMNISTimageClassifier.py
```

---

# 📊 Model Evaluation

The CNN model was evaluated using:

- Training Accuracy
- Validation Accuracy
- Test Accuracy
- Test Loss
- Sample Predictions
- Confusion Matrix

The project also visualizes:

- 10 Correctly Classified Images
- 10 Incorrectly Classified Images

---

# 📈 Training Graphs

The training process includes:

- Training Accuracy
- Validation Accuracy
- Training Loss
- Validation Loss

Both graphs are displayed together in a single figure to compare model performance during training.

---

# 🖼️ Sample Predictions

The model predicts clothing categories for test images and displays:

- Actual Label
- Predicted Label

This provides a visual comparison of the model's predictions.

---

# 📉 Confusion Matrix

A confusion matrix is generated to evaluate the model's classification performance across all 10 Fashion MNIST classes.

It helps identify which classes are correctly classified and which classes are commonly misclassified.

---

# 📸 Output Images

The **generatedImages** folder contains:

- Sample Images
- Training & Validation Graphs
- Confusion Matrix
- Correct Predictions
- Incorrect Predictions

---

# 📊 Results

**Final Training Accuracy**

> Add your training accuracy here after running the model.

Example:

```
Training Accuracy: 96.20%
```

**Final Test Accuracy**

> Add your test accuracy here after running the model.

Example:

```
Test Accuracy: 92.80%
```

**Test Loss**

> Add your loss value here.

Example:

```
Loss: 0.23
```

---

# ⚠️ Challenges Faced

During this project, I encountered several challenges:

- Understanding the CNN architecture.
- Reshaping image data for CNN input.
- Displaying predicted and actual labels together.
- Creating and interpreting the confusion matrix.
- Identifying correctly and incorrectly classified images.

### Solutions

- Studied TensorFlow/Keras CNN documentation.
- Practiced image preprocessing techniques.
- Used Matplotlib for visualization.
- Used Scikit-learn's Confusion Matrix for model evaluation.
- Tested the model multiple times to understand prediction behavior.

---

# 🎥 Screen Recording

A short screen recording demonstrates:

- Dataset loading
- Image preprocessing
- CNN model architecture
- Model training
- Evaluation metrics
- Training graphs
- Confusion matrix
- Prediction results

---

# 🎓 Learning Outcomes

After completing this project, I learned how to:

- Build Convolutional Neural Networks using TensorFlow/Keras.
- Process and classify image datasets.
- Extract image features using convolution layers.
- Reduce image dimensions using pooling layers.
- Evaluate CNN models using accuracy, loss, and confusion matrices.
- Visualize prediction results.
- Understand why CNNs are widely used in modern Computer Vision applications.

---

# ✅ Conclusion

This project provided practical experience in developing a Convolutional Neural Network for image classification using the Fashion MNIST dataset. It demonstrated the complete deep learning pipeline, including preprocessing, model building, training, evaluation, prediction, and performance visualization. CNNs proved to be highly effective for image classification by automatically learning meaningful visual features while preserving spatial information.

---

## 👨‍💻 Author

**Ashhad**

