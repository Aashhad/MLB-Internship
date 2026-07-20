import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


breastCancer = load_breast_cancer()
X = breastCancer.data
y = breastCancer.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)


baselineAcc = accuracy_score(y_test, y_pred)
baselinef1 = f1_score(y_test, y_pred)


print(f"Baseline Accuracy: {baselineAcc:.4f}")
print(f"Baseline F1-Score: {baselinef1:.4f}")
 

# GridSearchCV
params_grid = {
    "C": [0.25, 0.50, 0.75, 1.0],
    "solver": ["lbfgs", "newton-cg","liblinear"],
    'max_iter': [100, 500, 1000]
}

gridSearch = GridSearchCV(
    LogisticRegression(max_iter=1000),
    param_grid = params_grid,
    cv = 5,
    scoring="accuracy",
    n_jobs= -1
)

gridSearch.fit(X_train, y_train)

print("Best Parameters:", gridSearch.best_params_)
print("Best Cross Validation Accuracy:", gridSearch.best_score_)

tunedModel = gridSearch.best_estimator_
tunedPred = tunedModel.predict(X_test)

tunedAcc = accuracy_score(y_test, tunedPred)
tunedF1 = f1_score(y_test, tunedPred)

print(f"Tuned Accuracy: {tunedAcc:.4f}")
print(f"Tuned F1-Score: {tunedF1:.4f}")

# Comparison Both Models
print("Compare Baseline & Tuned Model")
print(f"Baseline Accuracy : {baselineAcc:.4f}")
print(f"Tuned Accuracy    : {tunedAcc:.4f}")

print(f"Baseline F1-Score : {baselinef1:.4f}")
print(f"Tuned F1-Score    : {tunedF1:.4f}")

if tunedAcc > baselineAcc and tunedF1 > baselinef1:
    print("\n✅ Tuned model is better than both Accuracy & F1-Score.")
elif tunedAcc == baselineAcc and tunedF1 == baselinef1:
    print("\n✅ Both models perform equally.")
else:
    print("\n✅ Baseline model performs better in one or more metrics.")