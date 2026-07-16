from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

iris = load_iris()
X = iris.data
y = iris.target

print("Features:", iris.feature_names)
print("Targets:", iris.target_names)
print("Shape of Dataset:", X.shape)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = LogisticRegression()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(f"Accuracy:", accuracy_score(y_test, y_pred))
print(f"Precision:",precision_score(y_test, y_pred, average="macro"))
print(f"Recall:", recall_score(y_test, y_pred, average="macro"))
print(f"F1:", f1_score(y_test, y_pred, average="macro"))
