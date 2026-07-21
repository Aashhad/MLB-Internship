import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# load dataset
iris = load_iris()
X = iris.data
y = iris.target
print(iris.feature_names)
print(iris.target_names)

# convert into pandas dataframe
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df["Target"] = iris.target

# explore the dataset
print(df.head())
print(df.info())
print(df.describe())
print(df.isnull().sum())
print(df["Target"].value_counts())
print(df.shape)

# feature scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Elbow Method
wcss = []
for k in range(1, 11):

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)


# Visualize Elbow Method
plt.figure(figsize=(8, 5))
plt.plot(
    range(1, 11),
    wcss,
    marker="o"
)
plt.xlabel("Number of Clusters (K)")
plt.ylabel("WCSS")
plt.title("Elbow Method")
plt.xticks(range(1, 11))
plt.show()

# Apply K-Means

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)
labels = kmeans.fit_predict(X_scaled)
df["Cluster"] = labels

# Compare Cluster with Actual Classes
print("\nActual Target vs K-Means Cluster:")
print(pd.crosstab(df["Target"],df["Cluster"]))

# Apply PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
print("\nOriginal Shape:", X_scaled.shape)
print("PCA Shape:", X_pca.shape)

# Check expalained variance
print("Explained Variance Ratio:",pca.explained_variance_ratio_)
print("Total Explained Variance:",pca.explained_variance_ratio_.sum())

fig, axes = plt.subplots(2,2,figsize=(14, 10))


# Original Iris Data
axes[0, 0].scatter(
    X[:, 0],
    X[:, 1],
    c=y,
    cmap="viridis",
    s=60
)
axes[0, 0].set_xlabel("Sepal Length")
axes[0, 0].set_ylabel("Sepal Width")
axes[0, 0].set_title("Original Iris Data")


# K-Means Clusters
axes[0, 1].scatter(
    X[:, 0],
    X[:, 1],
    c=labels,
    cmap="viridis",
    s=60
)
axes[0, 1].set_xlabel("Sepal Length")
axes[0, 1].set_ylabel("Sepal Width")
axes[0, 1].set_title("K-Means Clusters")


# PCA Visualization
axes[1, 0].scatter(
    X_pca[:, 0],
    X_pca[:, 1],
    c=y,
    cmap="viridis",
    s=60
)
axes[1, 0].set_xlabel("Principal Component 1")
axes[1, 0].set_ylabel("Principal Component 2")
axes[1, 0].set_title("PCA Visualization")


# K-Means Clusters with PCA
axes[1, 1].scatter(
    X_pca[:, 0],
    X_pca[:, 1],
    c=labels,
    cmap="viridis",
    s=60
)
axes[1, 1].set_xlabel("Principal Component 1")
axes[1, 1].set_ylabel("Principal Component 2")
axes[1, 1].set_title("K-Means Clusters with PCA")

fig.suptitle("Iris Flower Clustering and PCA Visualization",fontsize=16)
plt.savefig("DAY 9/iris_clustering_pca_comparison.png",dpi=300,bbox_inches="tight")
plt.tight_layout()
plt.show()