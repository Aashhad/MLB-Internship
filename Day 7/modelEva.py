import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score , confusion_matrix , precision_score, recall_score, f1_score

df = pd.read_csv("Day 7/cleaned_student_performance.csv")

df = df.dropna()

# Features and Target
X = df[["Python", "Machine_Learning", "Data_Science"]]
y = df["Performance"]

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Feature Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Models
model = LogisticRegression()
model1 = DecisionTreeClassifier(random_state=42)

# Train
model.fit(X_train, y_train)
model1.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_pred1 = model1.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
accuracy1 = accuracy_score(y_test, y_pred1)
print("Logistic Regression Accuracy:", accuracy)
print("Decision Tree Accuracy:", accuracy1)

# Precision
precision = precision_score(y_test, y_pred, average="macro", zero_division=0)
precisions = precision_score(y_test, y_pred1, average="macro", zero_division=0)
print('Logistic Regression  of Precision:', precision)
print('Decision Tree of Precision:', precisions)

# Recall
recall = recall_score(y_test, y_pred, average="macro")
recall1 = recall_score(y_test, y_pred1, average="macro")
print("Logistic Regression  of Recall:", recall)
print("Decision Tree of Recall:", recall1)


# F1
f1 = f1_score(y_test, y_pred, average="macro")
f11 = f1_score(y_test, y_pred1, average="macro")
print("Logistic Regression  of F1-Score:", f1 )
print("Decision Tree of F1-Score:", f11 )

# Confusion Matrix
conFmatrix = confusion_matrix(y_test, y_pred)
conFmatrix1 = confusion_matrix(y_test, y_pred)
print("Logistic Regression Confusion Matrix:") 
print(conFmatrix)
print("Decision Tree Confusion Matrix:")
print(conFmatrix1)

