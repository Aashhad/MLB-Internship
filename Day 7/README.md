# 📅 Day 7 – Classification & Model Evaluation

## 📖 Overview

On Day 7 of my AI & ML Internship, I learned about **Classification** problems and how to evaluate Machine Learning models using different performance metrics.

The focus of this assignment was understanding the difference between **Regression** and **Classification**, training classification models using **Scikit-learn**, evaluating their performance, and building an **Iris Flower Classification System**.

---

# 🎯 Learning Objectives

During this assignment, I learned:

## 📊 Model Evaluation

- Training vs Testing Performance
- Overfitting and Underfitting
- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

## 🤖 Classification Algorithms

- What is Classification?
- Regression vs Classification
- Logistic Regression
- Decision Trees
- Real-world Classification Applications

---

# 📂 Dataset

Dataset Used:

```
Iris Dataset (Scikit-learn Built-in Dataset)
```

The Iris dataset contains measurements of iris flowers and is commonly used for learning classification algorithms.

### Features

- Sepal Length
- Sepal Width
- Petal Length
- Petal Width

### Target Classes

- Setosa
- Versicolor
- Virginica

---

# 🌸 What is Classification?

Classification is a Machine Learning task where the goal is to predict a **category or class** rather than a continuous value.

Examples include:

- Email Spam Detection
- Disease Prediction
- Face Recognition
- Iris Flower Classification
- Fraud Detection

---

# 🔄 Regression vs Classification

| Regression | Classification |
|------------|----------------|
| Predicts numerical values | Predicts categories or classes |
| Output is continuous | Output is discrete |
| Example: House Price Prediction | Example: Iris Species Prediction |

---

# 🧹 Data Preparation

The following preprocessing steps were performed:

- Loaded the Iris dataset from Scikit-learn.
- Explored dataset features and target classes.
- Split the dataset into **80% Training** and **20% Testing** data.
- Prepared the data for classification model training.

---

# 🤖 Logistic Regression Model

A Logistic Regression model was trained using the Iris dataset.

### Workflow

- Load dataset
- Train model
- Predict flower species
- Evaluate model
- Display sample predictions
- Generate Confusion Matrix

---

# 🌳 Decision Tree Model

As a bonus task, a Decision Tree Classifier was also trained.

The performance of the Decision Tree model was compared with the Logistic Regression model using the same evaluation metrics.

---

# 📈 Evaluation Metrics

The following metrics were used to evaluate both models:

### ✅ Accuracy

Measures the percentage of correct predictions.

---

### 🎯 Precision

Measures how many predicted positive values were actually correct.

---

### 🔍 Recall

Measures how many actual positive values were correctly identified.

---

### ⚖️ F1-Score

The harmonic mean of Precision and Recall.

---

### 📊 Confusion Matrix

Shows the number of:

- Correct Predictions
- Incorrect Predictions
- True Positives
- True Negatives
- False Positives
- False Negatives

It provides a detailed view of the model's performance.

---

# 📊 Model Performance & Observations

- Logistic Regression achieved excellent classification accuracy on the Iris dataset.
- Decision Tree also performed well and produced comparable results.
- The Confusion Matrix showed that most flower species were classified correctly.
- Since the Iris dataset is small and well-structured, both models performed with very high accuracy.

---

# 🌸 Mini Project

## Iris Flower Classification System

The mini project performs the following tasks:

- Loads the Iris dataset
- Explores the dataset
- Splits the data into training and testing sets
- Trains a Logistic Regression model
- Predicts flower species
- Evaluates the model
- Displays Accuracy, Precision, Recall, and F1-Score
- Generates a Confusion Matrix
- Prints Actual vs Predicted values
- Trains a Decision Tree model for comparison

---

# 📁 Project Structure

```
Day 7/
│
├── cleaned_student_performance.csv
├── confusion_matrix.png
├── irisFlowerClassificationSystem.py
├── modelClass.py
├── modelEva.py
├── README.md
└── requirements.txt
```

---

# 🛠 Technologies Used

- Python 3
- NumPy
- Pandas
- Matplotlib
- Scikit-learn

---


# 📚 Key Learnings

Through this assignment, I learned how to:

- Understand classification problems.
- Differentiate between Regression and Classification.
- Train Logistic Regression and Decision Tree models.
- Evaluate models using Accuracy, Precision, Recall, F1-Score, and Confusion Matrix.
- Interpret model performance correctly.
- Compare different classification algorithms.
- Build a complete Machine Learning classification project using Scikit-learn.

---

# 🚀 Expected Outcome

After completing this assignment, I can:

- Solve classification problems using Machine Learning.
- Train and evaluate classification models.
- Explain common evaluation metrics.
- Compare different classification algorithms.
- Build simple end-to-end classification systems.

---

# 👨‍💻 Author

**Muhammad Ashhad**

