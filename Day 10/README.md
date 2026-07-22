# Day 10: Introduction to Deep Learning & Artificial Neural Network

## 📌 Overview

Day 10 marks the beginning of **Phase 2: Deep Learning** in my Machine Learning and AI internship.

In this project, I explored the fundamentals of **Deep Learning, Artificial Neural Networks (ANNs), Perceptrons, Neural Network Layers, and Activation Functions** using **TensorFlow/Keras**.

As a mini project, I built my first **Artificial Neural Network (ANN)** using the **Fashion MNIST dataset** to classify images of clothing items into 10 different categories.

---

## 🧠 Topics Covered

- Introduction to Deep Learning
- Machine Learning vs Deep Learning
- Applications of Deep Learning
- Artificial Neural Networks (ANN)
- Input Layer
- Hidden Layer
- Output Layer
- Perceptron
- Weights and Bias
- Activation Functions
  - ReLU
  - Sigmoid
  - Tanh
  - Softmax

---

## 💻 Coding Practice

Using **TensorFlow/Keras**, I practiced:

- Installing and verifying TensorFlow
- Importing TensorFlow and Keras
- Building a simple neural network
- Understanding Input, Hidden, and Output Layers
- Viewing the model summary
- Experimenting with different activation functions
- Comparing ReLU, Sigmoid, and Tanh activation functions

---

## 👕 Mini Project: Fashion MNIST Classification

For the main project, I used the **Fashion MNIST dataset** provided by TensorFlow/Keras.

The project includes:

- Loading the Fashion MNIST dataset
- Exploring dataset shapes and labels
- Visualizing sample images
- Normalizing pixel values
- Building an Artificial Neural Network
- Training the ANN model
- Evaluating the model on test data
- Checking training and validation accuracy
- Making predictions on test images
- Comparing actual and predicted labels
- Visualizing model predictions

---

## 🔄 Project Workflow

```text
Fashion MNIST Dataset
        ↓
Data Exploration
        ↓
Data Preprocessing
        ↓
Build ANN Model
        ↓
Train Model
        ↓
Evaluate Model
        ↓
Make Predictions
        ↓
Visualize Results
```

---

## 🏗️ ANN Model Architecture

The Fashion MNIST ANN follows this architecture:

```text
Input Image (28 × 28)
        ↓
Flatten
        ↓
Dense Layer (128 Neurons + ReLU)
        ↓
Dense Layer (64 Neurons + ReLU)
        ↓
Output Layer (10 Neurons + Softmax)
```

### Model Configuration

- **Input:** 28 × 28 grayscale image
- **Flatten Layer:** Converts image into a 1D array
- **Hidden Layer 1:** 128 neurons with ReLU
- **Hidden Layer 2:** 64 neurons with ReLU
- **Output Layer:** 10 neurons with Softmax
- **Optimizer:** Adam
- **Loss Function:** Sparse Categorical Crossentropy
- **Evaluation Metric:** Accuracy

---

## 📊 Dataset

The Fashion MNIST dataset contains:

| Property | Details |
|---|---|
| Training Images | 60,000 |
| Testing Images | 10,000 |
| Image Size | 28 × 28 pixels |
| Image Type | Grayscale |
| Number of Classes | 10 |

### Classes

```text
0 → T-shirt/top
1 → Trouser
2 → Pullover
3 → Dress
4 → Coat
5 → Sandal
6 → Shirt
7 → Sneaker
8 → Bag
9 → Ankle boot
```

---

## 📈 Model Results

The model was evaluated using:

- Training Accuracy
- Validation Accuracy
- Testing Accuracy

### Accuracy Results

```text
Final Training Accuracy: [Add Your Result]
Final Validation Accuracy: [Add Your Result]
Final Testing Accuracy: [Add Your Result]
```

The project also includes a **Training vs Validation Accuracy** graph to visualize the model's performance during training.

---

## 🔮 Predictions

After training the ANN, predictions were made on unseen test images.

The predicted labels were compared with the actual labels to check how accurately the model classified Fashion MNIST images.

Example:

```text
Actual:    Sneaker
Predicted: Sneaker
```

The project also contains sample prediction visualizations showing the images along with their actual and predicted labels.

---

## 🖼️ Project Visualizations

The following visualizations are included in this project:

- Sample prediction images
- Top 10 predicted images
- Training vs Validation Accuracy graph
- Actual vs Predicted labels

---

## 📁 Project Structure

```text
Day 10/
│
├── firstArtificialNeuralNetwork.py
├── NNlayers&Activation.py
├── predicted sample.png
├── README.md
├── requirements.txt
├── Top 10 predicted images.png
└── Training vs Validation Accuracy.png
```

### File Description

| File | Description |
|---|---|
| `firstArtificialNeuralNetwork.py` | Main Fashion MNIST ANN mini project |
| `NNlayers&Activation.py` | Practice with neural network layers and activation functions |
| `predicted sample.png` | Sample prediction visualization |
| `Top 10 predicted images.png` | Visualization of selected predictions |
| `Training vs Validation Accuracy.png` | Training and validation accuracy graph |
| `requirements.txt` | Required Python libraries |
| `README.md` | Project documentation |

---

## 🛠️ Technologies Used

- Python
- TensorFlow
- Keras
- NumPy
- Matplotlib
- Fashion MNIST Dataset

---

---

## 🎯 Key Learning Outcomes

Through this project, I learned how to:

- Understand the fundamentals of Deep Learning
- Understand the structure of Artificial Neural Networks
- Understand Input, Hidden, and Output Layers
- Understand Perceptrons, Weights, and Bias
- Work with TensorFlow and Keras
- Build and train an ANN model
- Preprocess image data
- Normalize pixel values
- Evaluate neural network performance
- Analyze training and validation accuracy
- Make predictions using a trained ANN
- Compare actual and predicted results
- Visualize model predictions

---

## 🚀 Future Learning

This project provides a foundation for learning more advanced Deep Learning topics, including:

- Forward Propagation
- Backpropagation
- Loss Functions
- Gradient Descent
- Overfitting and Regularization
- Dropout
- Convolutional Neural Networks (CNNs)
- Computer Vision
- Image Classification
- Transfer Learning
- Object Detection

---

## 👨‍💻 Author

**Ashhad**
