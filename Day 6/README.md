# 📅 Day 6 – Data Preprocessing & Linear Regression

## 📖 Overview

On Day 6 of my AI & ML Internship, I learned how to prepare data for Machine Learning and build my first predictive model using **Scikit-learn**.

The focus of this assignment was understanding the complete Machine Learning workflow, including:

- Data Preprocessing
- Feature Engineering
- Label Encoding
- Train-Test Splitting
- Feature Scaling
- Linear Regression
- Model Evaluation
- Student Score Prediction System

---

# 🎯 Learning Objectives

During this assignment, I learned:

## 📊 Data Preprocessing

- Understanding Features (X) and Target (y)
- Label Encoding for categorical data
- Train-Test Split
- Feature Scaling using StandardScaler
- Preventing Data Leakage
- Preparing data for Machine Learning

## 🤖 Machine Learning

- Introduction to Linear Regression
- Model Training
- Model Prediction
- Model Evaluation
- Understanding Regression Metrics

---

# 📂 Dataset

Dataset Used:

```
cleaned_student_performance.csv
```

This dataset was created during **Day 5** after performing data cleaning and feature engineering.

---

# 🧹 Data Preprocessing

The following preprocessing steps were performed:

- Loaded the cleaned student dataset.
- Encoded the **Performance** column using Label Encoding.
- Selected the following feature columns:

```
Math
Python
Statistics
```

Target Column:

```
Average_Score
```

- Split the dataset into:
  - **80% Training Data**
  - **20% Testing Data**
- Applied **StandardScaler** for feature scaling.
- Fitted the scaler only on the training data to avoid data leakage.

---

# 📚 What I Learned

### Features and Target

Features (X) are the input variables used by the model to make predictions, while the target (y) is the value the model learns to predict.

---

### Label Encoding

Machine Learning models require numerical input. Since the **Performance** column contains text values, it was converted into numeric values using Label Encoding.

---

### Feature Scaling

Feature scaling standardizes numerical values so that every feature contributes fairly during model training.

---

### Train-Test Split

The dataset was divided into training and testing sets.

This allows the model to learn from one portion of the data and be evaluated on completely unseen data.

---

### Data Leakage

I learned that data leakage can produce unrealistic model performance.

Since the **Performance** column is directly calculated from **Average_Score**, it was **not used** as an input feature because it would indirectly reveal the target value.

---

# 🤖 Linear Regression Model

A Linear Regression model was trained using:

### Input Features

- Math
- Python
- Statistics

### Target

- Average_Score

The **Machine_Learning** subject was intentionally excluded so that the model learns relationships instead of simply calculating the average directly.

---

# 📈 Model Evaluation

The following evaluation metrics were used:

### Mean Absolute Error (MAE)

Measures the average prediction error.

### Mean Squared Error (MSE)

Penalizes larger prediction errors by squaring them.

### R² Score

Shows how well the model explains the variation in the target values.

---

# 📊 Model Performance

The model achieved approximately:

| Metric | Value |
|---------|-------|
| MAE | 0.0000 |
| MSE | 0.0000 |
| R² Score | 1.0000 |

The model performed very well because the selected features have a strong relationship with the target variable.

However, since the dataset contains only **16 students**, these results should not be considered representative of real-world performance.

---

# 🚀 Mini Project

## Student Score Prediction System

The final project combines the complete Machine Learning workflow into one program.

It performs the following tasks:

- Loads the cleaned dataset
- Preprocesses the data
- Encodes categorical values
- Splits training and testing data
- Applies feature scaling
- Trains the Linear Regression model
- Predicts Average Scores
- Evaluates the model
- Displays Actual vs Predicted Scores
- Generates a scatter plot comparing predictions with actual values

---

# 📊 Generated Visualization

The project generates:

**Actual vs Predicted Average Score**

This scatter plot compares the model's predicted scores with the actual student scores.

A reference line is included to show how close the predictions are to perfect accuracy.

---

# 📁 Project Structure

```
Day 6/
│
├── Actual vs Predicted Average Score.png
├── cleaned_student_performance.csv
├── dataPreProcessing.py
├── linearRegressionModel.py
├── studentScorePredictionSystem.py
└── README.md
```

---

# 🛠 Technologies Used

- Python 3
- NumPy
- Pandas
- Scikit-learn
- Matplotlib

---

# ▶️ How to Run

## 1. Clone the Repository

```bash
git clone <repository-url>
```

## 2. Navigate to Day 6

```bash
cd "Day 6"
```

## 3. Install Dependencies

```bash
pip install numpy pandas matplotlib scikit-learn
```

## 4. Run the Scripts

### Data Preprocessing

```bash
python dataPreProcessing.py
```

### Linear Regression Model

```bash
python linearRegressionModel.py
```

### Student Score Prediction System

```bash
python studentScorePredictionSystem.py
```

--- 

# 📚 Key Learnings

Through this assignment, I learned how to:

- Prepare datasets for Machine Learning.
- Understand the importance of preprocessing.
- Encode categorical variables.
- Apply feature scaling correctly.
- Prevent data leakage.
- Train a Linear Regression model.
- Evaluate regression models using MAE, MSE, and R² Score.
- Compare actual and predicted values visually.
- Build a complete Machine Learning prediction pipeline.

---

# 🚀 Expected Outcome

After completing this assignment, I can:

- Prepare data for Machine Learning.
- Build regression models using Scikit-learn.
- Evaluate model performance.
- Understand the importance of proper preprocessing.
- Develop simple Machine Learning prediction systems.

---

# 👨‍💻 Author

**Muhammad Ashhad**

AI & Machine Learning Intern

---

## ✅ Project Status

**Completed Successfully ✔️**