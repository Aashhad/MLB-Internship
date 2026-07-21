import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


# load the dataset
iris = load_iris()
X = iris.data
y = iris.target

# explore the dataset using pandas
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df["Target"] = iris.target

print(df.head())
print(df.shape)
print(df.info())
print(df.describe())
print(df.isnull().sum())
print(df["Target"].value_counts())

# feature scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# elbow methon

wcss = []

for k in range(1, 11):
    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

# elbow graph
plt.figure(figsize=(8, 5))

plt.plot(range(1, 11), wcss, marker="o" )
plt.xlabel("Number of Clusters (K)")
plt.ylabel("WCSS")
plt.title("Elbow Method")
plt.xticks(range(1, 11))
plt.show()


# apply k-mean

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)
labels = kmeans.fit_predict(X_scaled)
df["Cluster"] = labels
print(df)

# compare K-means & actual classes
print(pd.crosstab(df["Target"], df["Cluster"]))

# Apply PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
print("Before PCA:", X_scaled.shape)
print("After PCA:", X_pca.shape)

# Check expalained variance
print("Explained Variance Ratio:",pca.explained_variance_ratio_)
print("Total Explained Variance:",pca.explained_variance_ratio_.sum())

# visualize PCA
plt.figure(figsize=(8, 6))

plt.scatter(
    X_pca[:, 0],   
    X_pca[:, 1],
    c=y,
    cmap="viridis",
    s=60
)

plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("Iris Dataset - PCA Visualization")
plt.show()


# compare PCA with K-means
plt.figure(figsize=(8, 6))
plt.scatter(
    X_pca[:, 0],
    X_pca[:, 1],
    c=labels,
    cmap="viridis",
    s=60
)
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("K-Means Clusters Visualized Using PCA")
plt.show()
