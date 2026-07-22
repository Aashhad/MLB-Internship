Day 10: Introduction to Deep Learning & Artificial Neural Network
📌 Overview

Day 10 marks the beginning of Phase 2: Deep Learning in my Machine Learning and AI internship.

In this project, I explored the fundamentals of Deep Learning, Artificial Neural Networks (ANNs), Perceptrons, Neural Network Layers, and Activation Functions using TensorFlow/Keras.

As a mini project, I built my first Artificial Neural Network (ANN) using the Fashion MNIST dataset to classify images of clothing items into 10 different categories.

🧠 Topics Covered
Introduction to Deep Learning
Machine Learning vs Deep Learning
Applications of Deep Learning
Artificial Neural Networks (ANN)
Input Layer
Hidden Layer
Output Layer
Perceptron
Weights and Bias
Activation Functions
ReLU
Sigmoid
Tanh
Softmax
💻 TensorFlow/Keras Practice

In the coding practice, I:

Installed and verified TensorFlow.
Imported TensorFlow and Keras.
Built a simple neural network.
Explored Input, Hidden, and Output Layers.
Viewed the model summary.
Experimented with different activation functions.
Compared ReLU, Sigmoid, and Tanh activation functions.
👕 Mini Project: Fashion MNIST Classification

For the main project, I used the Fashion MNIST dataset provided by TensorFlow/Keras.

The project includes:

Loading the Fashion MNIST dataset.
Exploring dataset shapes and labels.
Visualizing sample images.
Normalizing pixel values.
Building an Artificial Neural Network.
Training the ANN model.
Evaluating the model on test data.
Checking training and validation accuracy.
Making predictions on test images.
Comparing actual and predicted labels.
Visualizing model predictions.
Project Workflow
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
🏗️ ANN Model Architecture

The Fashion MNIST ANN follows this basic architecture:

Input Image (28 × 28)
        ↓
Flatten
        ↓
Dense Layer (128 Neurons + ReLU)
        ↓
Dense Layer (64 Neurons + ReLU)
        ↓
Output Layer (10 Neurons + Softmax)

The model uses:

ReLU activation in hidden layers.
Softmax activation in the output layer for 10-class classification.
Adam optimizer.
Sparse Categorical Crossentropy loss function.
Accuracy as the evaluation metric.
📊 Model Results

The project evaluates the model using:

Training Accuracy
Validation Accuracy
Testing Accuracy

The project also includes a graph showing the Training vs Validation Accuracy during model training.

Final Training Accuracy: Add your final accuracy here
Final Validation Accuracy: Add your final accuracy here
Final Testing Accuracy: Add your final accuracy here

🖼️ Visualizations

The project contains visual outputs for:

Sample Fashion MNIST images.
Predicted sample images.
Top 10 predicted images.
Training and validation accuracy graph.
Actual vs predicted labels.
📁 Project Structure
Day 10/
│
├── firstArtificialNeuralNetwork.py
├── NNlayers&Activation.py
├── predicted sample.png
├── README.md
├── requirements.txt
├── Top 10 predicted images.png
└── Training vs Validation Accuracy.png
File Description
File	Description
firstArtificialNeuralNetwork.py	Main Fashion MNIST ANN mini project
NNlayers&Activation.py	Practice with neural network layers and activation functions
predicted sample.png	Sample prediction visualization
Top 10 predicted images.png	Visualization of selected predictions
Training vs Validation Accuracy.png	Training and validation accuracy graph
requirements.txt	Required Python libraries
README.md	Project documentation
🛠️ Technologies Used
Python
TensorFlow
Keras
NumPy
Matplotlib
Fashion MNIST
🎯 Key Learning Outcomes

Through this project, I learned how to:

Understand the fundamentals of Deep Learning.
Understand the basic structure of Artificial Neural Networks.
Understand Perceptrons and activation functions.
Work with TensorFlow and Keras.
Build and train an ANN model.
Preprocess image data.
Evaluate neural network performance.
Analyze training and validation accuracy.
Make predictions using a trained ANN.
Compare actual and predicted results.
Visualize neural network predictions.

This project is my first step into Deep Learning, providing a foundation for future learning in Convolutional Neural Networks (CNNs), Computer Vision, and advanced Deep Learning models.

👨‍💻 Author

Ashhad

MLB Internship — Day 10

Phase 2: Deep Learning