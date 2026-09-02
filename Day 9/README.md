# Day-9: K-Means Clustering & Principal Component Analysis (PCA)

## Objective

The objective of this project is to understand Unsupervised Learning by applying K-Means Clustering and Principal Component Analysis (PCA) on the Iris dataset. The project focuses on grouping similar data points, selecting the optimal number of clusters using the Elbow Method, and visualizing high-dimensional data in two dimensions.

---

## Topics Covered

- Unsupervised Learning
- Clustering
- K-Means Clustering
- Choosing the Value of K
- Elbow Method
- WCSS (Within-Cluster Sum of Squares)
- Cluster Visualization
- Cluster Centroid Visualization
- Principal Component Analysis (PCA)
- Dimensionality Reduction
- Data Visualization
- 3D Cluster Visualization
- Real-World Applications of Clustering

---

## Dataset

**Dataset:** Iris Dataset (Built into Scikit-learn)

### Features

- Sepal Length
- Sepal Width
- Petal Length
- Petal Width

### Target Classes

- Setosa
- Versicolor
- Virginica

---

## Project Workflow

1. Load the Iris dataset using Scikit-learn.
2. Convert the dataset into a Pandas DataFrame.
3. Explore the dataset using Pandas.
4. Standardize the features using `StandardScaler`.
5. Apply the Elbow Method to determine the optimal number of clusters.
6. Apply K-Means Clustering.
7. Visualize the K-Means clusters.
8. Visualize cluster centroids.
9. Apply PCA to reduce the dataset from four dimensions to two principal components.
10. Visualize the PCA-transformed data.
11. Compare the clustering results with PCA visualization.
12. Create 2D and 3D cluster visualizations.

---

## What is Clustering?

Clustering is an Unsupervised Machine Learning technique that groups similar data points together without using labeled data. Data points within the same cluster are more similar to each other than to data points in other clusters.

---

## What is PCA?

Principal Component Analysis (PCA) is a dimensionality reduction technique that transforms high-dimensional data into a smaller number of principal components while preserving important information.

In this project, PCA reduced the Iris dataset from **4 features to 2 principal components**, making the data easier to visualize.

---

## How was the Best Value of K Determined?

The **Elbow Method** was used to determine the optimal number of clusters.

The **WCSS (Within-Cluster Sum of Squares)** was calculated for different values of K. The Elbow graph showed a clear bend at **K = 3**.

Therefore, **K = 3** was selected for the K-Means clustering model.

---

## Observations

- Three clusters were formed using K-Means.
- The clusters represented the Iris flower species reasonably well.
- Setosa was more clearly separated from the other species.
- Versicolor and Virginica showed some overlap because their features are similar.
- PCA reduced the dataset from four features to two principal components.
- PCA made the clustering structure easier to visualize.
- Cluster centroids helped identify the center of each cluster.
- 3D visualization provided another way to understand the cluster distribution.

---

## Insights Gained

- K-Means can group similar data points without using target labels.
- Feature scaling is important for distance-based algorithms such as K-Means.
- The Elbow Method helps select an appropriate value of K.
- PCA simplifies high-dimensional data for visualization.
- Combining K-Means and PCA makes cluster patterns easier to understand.
- Cluster visualization can help identify similarities and differences within the dataset.

---

## Project Structure

```text
Day 9/
│
├── 3D K-Means Clustering with Centeroids.png
├── dataExplore.py
├── elbow_method.png
├── iris_clustering_pca_comparison.png
├── irisFlowerClustering&Visualization.py
├── K-Means Clustering with Centeroids.png
├── kMeans.py
├── kMeansClustering&PCA.py
├── pca.png
├── pcaKmeans.py
├── README.md
└── requirements.txt
```

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn

---

## Conclusion

This project demonstrated how K-Means Clustering can group similar data points and how PCA can reduce dimensionality for effective visualization. The Elbow Method identified **K = 3** as the optimal number of clusters. PCA reduced the four-dimensional Iris dataset to two dimensions, making the clustering results easier to visualize and interpret.

# 👨‍💻 Author

**Muhammad Ashhad**
