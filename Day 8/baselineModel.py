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
baselineRecall = recall_score(y_test, y_pred)
baselinePre = precision_score(y_test, y_pred)
baselineF1 = f1_score(y_test, y_pred)

print(f"Baseline Accuracy: {baselineAcc:.4f}")
print(f"Baseline Recall: {baselineRecall:.4f}")
print(f"Baseline Precision: {baselinePre:.4f}")
print(f"Baseline F1-Score: {baselineF1:.4f}")