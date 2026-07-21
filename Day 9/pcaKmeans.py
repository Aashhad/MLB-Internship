import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Load Iris dataset
iris = load_iris()
X = iris.data
y = iris.target


# Scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# apply pca
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# variance
print("Explained Variance Ratio:",pca.explained_variance_ratio_)
print("Total Explained Variance:",pca.explained_variance_ratio_.sum())

# print before and after PCA
print("Before PCA:", X_scaled.shape)
print("After PCA:", X_pca.shape)

# before pca
plt.scatter(
    X[:, 0],
    X[:, 1],
    c=y
)

plt.xlabel("Sepal Length")
plt.ylabel("Sepal Width")
plt.title("Iris Dataset Before PCA")
plt.show()

# after PCA
plt.scatter(
    X_pca[:, 0],
    X_pca[:, 1],
    c=y
)

plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("Iris Dataset After PCA")
plt.savefig("Day 9/pca.png",dpi=300,bbox_inches="tight")
plt.show()