# Day-8: Model Evaluation and Hyperparameter Tuning

## What I worked on

Today's objective was to learn how to evaluate a Machine Learning classification model and improve its performance using Hyperparameter Tuning. I used the **Breast Cancer Wisconsin Diagnostic Dataset** from Scikit-learn to build a Logistic Regression model, evaluate it using different performance metrics, tune it using GridSearchCV, and compare the baseline model with the tuned model.

---

## Dataset Exploration (`exploreDataset.py`)

- Loaded the Breast Cancer Wisconsin Diagnostic Dataset from `sklearn.datasets`.
- Converted the dataset into a Pandas DataFrame.
- Explored the dataset using:
  - `head()`
  - `info()`
  - `describe()`
- Checked the target class distribution using `value_counts()`.
- Observed that the dataset contains two target classes:
  - **0 = Malignant**
  - **1 = Benign**

---

## Baseline Model (`baselineModel.py`)

- Split the dataset into 80% training data and 20% testing data.
- Applied **StandardScaler** to scale the features.
- Trained a Logistic Regression model using the default parameters.
- Evaluated the model using:
  - Accuracy
  - Precision
  - Recall
  - F1-Score
  - Confusion Matrix

### Baseline Results

- **Accuracy:** `0.9737`
- **F1-Score:** `0.9790`

---

## Hyperparameter Tuning (`hyperParmeterTuning.py`)

Used **GridSearchCV** to automatically search for the best Logistic Regression hyperparameters.

### Parameters Tested

- **C:** 0.25, 0.50, 0.75, 1.0
- **Solver:** lbfgs, liblinear
- **Max Iterations:** 100, 500, 1000

GridSearchCV evaluated every parameter combination using **5-Fold Cross Validation** and selected the best-performing model.

### Best Parameters Found

```python
{
    'C': 0.25,
    'max_iter': 100,
    'solver': 'liblinear'
}
```

### Best Cross Validation Accuracy

```
0.9780
```

---

## Tuned Model

After applying the best hyperparameters, the tuned Logistic Regression model was evaluated on the testing dataset.

### Tuned Results

- **Accuracy:** `0.9912`
- **F1-Score:** `0.9930`

---

# Baseline vs Tuned Model Comparison

| Metric | Baseline Model | Tuned Model |
|----------|:-------------:|:-----------:|
| Accuracy | **0.9737** | **0.9912** |
| F1-Score | **0.9790** | **0.9930** |

### Observation

The tuned model performed better than the baseline model.

- Accuracy improved from **97.37%** to **99.12%**.
- F1-Score improved from **97.90%** to **99.30%**.
- GridSearchCV selected better hyperparameters, resulting in improved model performance.

---

## What I Learned

During this task, I learned:

- Difference between Training and Testing performance.
- Underfitting and Overfitting concepts.
- Importance of Cross Validation.
- Choosing the correct evaluation metrics.
- Accuracy alone is not enough to evaluate a classification model.
- Precision, Recall, and F1-Score provide a better understanding of model performance.
- Hyperparameter tuning helps improve model accuracy.
- GridSearchCV automatically searches for the best hyperparameters using Cross Validation.

---

## Challenges Faced

While implementing Hyperparameter Tuning, I faced several issues:

- I initially used `best_params_` instead of `best_estimator_` for prediction.
- I made syntax mistakes while defining the parameter grid.
- I encountered errors due to incorrect solver names.
- After understanding how GridSearchCV works, I successfully tuned the model and compared it with the baseline model.

---

# Project File Structure

```
Day 8/
│
├── baselineModel.py
├── breastCancerPredictionSystem.py
├── confusion_matrix_comparison.png
├── exploreDataset.py
├── hyperParmeterTuning.py
├── README.md
└── requirements.txt
```

### File Description

- **baselineModel.py** → Trains and evaluates the baseline Logistic Regression model.
- **breastCancerPredictionSystem.py** → Complete Breast Cancer Prediction System pipeline.
- **confusion_matrix_comparison.png** → Side-by-side comparison of baseline and tuned confusion matrices.
- **exploreDataset.py** → Loads and explores the dataset.
- **hyperParmeterTuning.py** → Performs GridSearchCV and compares baseline vs tuned model.
- **README.md** → Project documentation.
- **requirements.txt** → List of required Python libraries.

---

## Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- Seaborn
- Scikit-learn

---

## Conclusion

This project helped me understand the complete Machine Learning workflow for a classification problem. I learned how to evaluate a Logistic Regression model using different metrics, improve its performance with GridSearchCV, and compare the baseline and tuned models. Hyperparameter tuning increased the model's Accuracy from **97.37%** to **99.12%**, demonstrating the importance of selecting the right model parameters.

---

# 👨‍💻 Author

**Muhammad Ashhad**