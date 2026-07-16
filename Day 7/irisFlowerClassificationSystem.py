# First import libraries
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix


# load the dataset
iris = load_iris()
X = iris.data
y = iris.target
print("Feature Names:")
print(iris.feature_names)
print("Target Names:")
print(iris.target_names)
print("Dataset Shape:")
print(X.shape)

# Explore the dataset
df = pd.DataFrame(X, columns=iris.feature_names)
df["Species"] = y
print("Missing Values:")
print(df.isnull().sum())
print("Class Distribution:")
print(df["Species"].value_counts())

# train test split 
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

# scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# model selection
model = LogisticRegression()
model1 = DecisionTreeClassifier()
model.fit(X_train, y_train)
model1.fit(X_train, y_train)

# predictions
y_pred = model.predict(X_test)
y_pred1 = model1.predict(X_test)

# model evaluation metrics comparison of Logistic Regression & Decision Tree
print("Accuracy Using Logistic Regression :", accuracy_score(y_test, y_pred))
print("Accuracy Using Decision Tree :", accuracy_score(y_test, y_pred1))
print("Precision Using Logistic Regression :", precision_score(y_test, y_pred, average="macro"))
print("Precision Using Decision Tree:", precision_score(y_test, y_pred1, average="macro"))
print("Recall Using Logistic Regression:", recall_score(y_test, y_pred, average="macro"))
print("Recall Using Decision Tree:", recall_score(y_test, y_pred1, average="macro"))
print("F1 Score Using Logistic Regression:", f1_score(y_test, y_pred, average="macro"))
print("F1 Score Using Decision Tree:", f1_score(y_test, y_pred1, average="macro"))

# confusion matrix
conMatrix = confusion_matrix(y_test, y_pred)
conMatrixx = confusion_matrix(y_test, y_pred1)
print("\nConfusion Matrix:\n")
print(conMatrix)

# Sample predictions with the actual values
print("\nSample Predictions\n")

# using or operator
for actual, predicted in zip(y_test[:10], y_pred[:10]):
    print(
        f"Actual: {iris.target_names[actual]} | "
        f"Predicted: {iris.target_names[predicted]} "
    )



fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Logistic Regression Confusion Matrix
ConfusionMatrixDisplay(
    confusion_matrix=conMatrix,
    display_labels=iris.target_names
).plot(cmap="Blues", ax=axes[0], colorbar=False)

axes[0].set_title("Logistic Regression")
axes[0].set_xlabel("Predicted Label")
axes[0].set_ylabel("True Label")

# Decision Tree Confusion Matrix
ConfusionMatrixDisplay(
    confusion_matrix=conMatrixx,
    display_labels=iris.target_names
).plot(cmap="Greens", ax=axes[1], colorbar=False)

axes[1].set_title("Decision Tree")
axes[1].set_xlabel("Predicted Label")
axes[1].set_ylabel("True Label")

plt.suptitle("Confusion Matrix Comparison", fontsize=14)
plt.tight_layout()

plt.savefig("Day 7/confusion_matrix.png", dpi=300)
plt.show()