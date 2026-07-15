import numpy as np
import pandas as pd

df = pd.read_csv("Day 6/cleaned_student_performance.csv")
print(df)

independentVar = df[['Name', 'Roll_No' ,'Python' ,'Machine_Learning' ,'Data_Science']].values
print(independentVar)

dependentVar = df[['Performance']].values
print(dependentVar)


# Fill missing values
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(missing_values= np.nan, strategy='mean')
impute = imputer.fit(independentVar[:, 1:4])
imputer.transform(independentVar[:, 1:4])
independent= imputer.transform(independentVar[:, 1:4])
print(independent)

# Handling categorical data
# in which you can give data in form of 0 - 9 (12, 45, 678)
from sklearn.preprocessing import LabelEncoder
labelEncoder = LabelEncoder()
catData = labelEncoder.fit_transform(independentVar[:, 0])
print(catData)

# you can change str to float 
from sklearn.preprocessing import LabelEncoder
labelEncoder = LabelEncoder()
df["Name"] = labelEncoder.fit_transform(df["Name"])

# if you can give data in the form of 0 and 1
from sklearn.preprocessing import OneHotEncoder
onehotencoder = OneHotEncoder()
dummyEncoder = onehotencoder.fit_transform(df["Name"].values.reshape(-1, 1)).toarray()
print(dummyEncoder)

# if you have a column in dataset which yes or no for this column you can use labelencoder
from sklearn.preprocessing import LabelEncoder
labelencoder_dependentVar = LabelEncoder()
catData = labelencoder_dependentVar.fit_transform(dependentVar)
print(catData)

# Train Test Split
independentVar = df[['Name', 'Roll_No' ,'Python' ,'Machine_Learning' ,'Data_Science']].values
dependentVar = df[['Performance']].values
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(independentVar, dependentVar,test_size = 0.2, random_state = 0)
print(x_train, x_test, y_train, y_test)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
X = df[['Roll_No', 'Python', 'Machine_Learning', 'Data_Science']].values
scale_x = StandardScaler()
x_train = scale_x.fit_transform(x_train)
x_test = scale_x.transform(x_test)
print(x_train)
print(x_test)

