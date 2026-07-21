import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# Load dataset
iris = load_iris()
X = iris.data
y = iris.target


# Standardize data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# Original Data Visualization
plt.scatter(X[:, 0], X[:, 1])
plt.xlabel(iris.feature_names[0])
plt.ylabel(iris.feature_names[1])
plt.title("Iris Dataset Scatter Plot")
plt.show()


# Elbow Method
wcss = []
for i in range(1, 11):
    km = KMeans(n_clusters=i,random_state=42,n_init=10)
    km.fit(X_scaled)
    wcss.append(km.inertia_)
print(wcss)


# Elbow Graph
plt.plot(range(1, 11), wcss, marker="o")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("WCSS")
plt.title("Elbow Method")
plt.savefig("Day 9/elbow method.png",dpi=300,bbox_inches="tight")
plt.show()



# K-Means Clustering based on elbow method 
km = KMeans(n_clusters=3,random_state=42,n_init=10)
label = km.fit_predict(X_scaled)
print(label)



# K-Means Clustering Graph
plt.scatter(X_scaled[label == 0, 0],X_scaled[label == 0, 1],color="blue",label="Cluster 0")
plt.scatter(X_scaled[label == 1, 0],X_scaled[label == 1, 1],color="red",label="Cluster 1")
plt.scatter(X_scaled[label == 2, 0],X_scaled[label == 2, 1],color="green",label="Cluster 2")


# Plot centroids
plt.scatter(
    km.cluster_centers_[:, 0],
    km.cluster_centers_[:, 1],
    color="black",
    marker="X",
    s=200,
    label="Centroids"
)

plt.xlabel("Standardized Feature 1")
plt.ylabel("Standardized Feature 2")
plt.title("K-Means Clustering on Iris Dataset")
plt.legend()
plt.savefig("Day 9/K-Means Custering with Centeroids.png",dpi=300,bbox_inches="tight")
plt.show()



from mpl_toolkits.mplot3d import Axes3D
# Create 3D figure
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection="3d")

# Cluster 0
ax.scatter(
    X_scaled[label == 0, 0],
    X_scaled[label == 0, 1],
    X_scaled[label == 0, 2],
    label="Cluster 0"
)

# Cluster 1
ax.scatter(
    X_scaled[label == 1, 0],
    X_scaled[label == 1, 1],
    X_scaled[label == 1, 2],
    label="Cluster 1"
)

# Cluster 2
ax.scatter(
    X_scaled[label == 2, 0],
    X_scaled[label == 2, 1],
    X_scaled[label == 2, 2],
    label="Cluster 2"
)

# Plot centroids
ax.scatter(
    km.cluster_centers_[:, 0],
    km.cluster_centers_[:, 1],
    km.cluster_centers_[:, 2],
    marker="X",
    s=200,
    label="Centroids"
)

# Labels
ax.set_xlabel(iris.feature_names[0])
ax.set_ylabel(iris.feature_names[1])
ax.set_zlabel(iris.feature_names[2])
ax.set_title("3D K-Means Clustering - Iris Dataset")
ax.legend()
plt.savefig("Day 9/3D K-Means Custering with Centeroids.png",dpi=300,bbox_inches="tight")
plt.show()

