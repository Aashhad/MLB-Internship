import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score,precision_score,recall_score,f1_score,confusion_matrix,ConfusionMatrixDisplay)

# Load Dataset
breastCancer = load_breast_cancer()
X = breastCancer.data
y = breastCancer.target

# Explore Dateset
df = pd.DataFrame(X, columns=breastCancer.feature_names)
df["target"] = y
print(df.head())
df.info()
print(df.describe())
print(df["target"].value_counts())

# Train test Split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

# Feature Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)


# Hyperparameter Tuning
params = {
    "C":[0.25,0.5,0.75,1],
    "solver":["lbfgs","newton-cg"],
    "max_iter":[100,500,1000]
}

grid = GridSearchCV(
    LogisticRegression(),
    param_grid=params,
    cv=5,
    scoring="accuracy",
    n_jobs=-1
)

grid.fit(X_train,y_train)
print(grid.best_params_)

bestModel = grid.best_estimator_
tunedPred =  bestModel.predict(X_test)

# Create confusion matrices
baselineConfMatrix = confusion_matrix(y_test, y_pred)
tunedConfMatrix = confusion_matrix(y_test, tunedPred)

# Create figure with two plots
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Baseline Model
sns.heatmap(
    baselineConfMatrix,
    annot=True,
    fmt="d",
    cmap="magma",
    xticklabels=breastCancer.target_names,
    yticklabels=breastCancer.target_names,
    ax=axes[0]
)

axes[0].set_title("Baseline Logistic Regression")
axes[0].set_xlabel("Predicted Label")
axes[0].set_ylabel("True Label")

# Tuned Model
sns.heatmap(
    tunedConfMatrix,
    annot=True,
    fmt="d",
    cmap="BuPu",
    xticklabels=breastCancer.target_names,
    yticklabels=breastCancer.target_names,
    ax=axes[1]
)

axes[1].set_title("Tuned Logistic Regression")
axes[1].set_xlabel("Predicted Label")
axes[1].set_ylabel("True Label")

# Adjust layout
plt.tight_layout()

# Save figure
plt.savefig("Day 8/confusion_matrix_comparison.png", dpi=300)

# Display figure
plt.show()

print("Succesfully saved as 'Day 8/confusion_matrix_comparison.png'")