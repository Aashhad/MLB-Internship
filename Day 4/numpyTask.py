# NUMPY Tasks
import numpy as np


# Creat 1D & 2D array
arr1d = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90])
print("1D :", arr1d)

arr2d = np.array([[1, 2, 3], [4, 5, 6]])
print("2D:", arr2d)


# Arithmetic operations on arrays
print(arr1d + 5)
print(arr1d - 5)
print(arr1d * 5)
print(arr1d / 5)

# Max, min, mean, sum
print(np.max(arr2d))
print(np.min(arr2d))
print(np.mean(arr2d))
print(np.sum(arr2d))


arrReshape = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120])
newArr1D = arrReshape.reshape(3,4) # 3 rows, 4 columns
print(newArr1D)

newArr3D = arrReshape.reshape(2,3,2)  # 4 rows, 3 columns
print(newArr3D)


# Slicing & Indexing
print("first index:", arr1d[0]) 
print("last index", arr1d[-1])
print("Slice index 1 to 4:", arr1d[1:4])

