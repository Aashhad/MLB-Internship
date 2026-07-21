import pandas as pd 
from sklearn.datasets import load_iris


iris=load_iris()

print(iris.keys())
print(iris.feature_names)

X=iris.data
df=pd.DataFrame(iris.data,columns=iris.feature_names)

print(df)
# shape of dataset
print(df.shape)
# last five rows from bottom/end
print(df.tail())
# information of dataset 
print(df.info())
# if can describe mean,count,std,min
print(df.describe())
# first five rows from top
print(df.head())
