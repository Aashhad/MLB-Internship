import numpy as np
import pandas as pd

# cleanData = pd.read_csv("Day 5/students.csv")
# use to check missing values
# print(cleanData.isna())
# how many missing values and in which column use this function
# print(cleanData.isnull().sum())
# remove row which have missing value
# print(cleanData.dropna())

# fill missing value with .fillna method
# missingValue = cleanData["Total Marks"].fillna("200")
# fill missing value with backward fill 
# missingValue = cleanData["Total Marks"].bfill()
# fill missing value with forward fill 
# missingValue = cleanData["Total Marks"].ffill()
# print(missingValue)
# fill with the column mean
# missingValue = cleanData["Total Marks"].fillna(cleanData["Total Marks"].mean())
# print(missingValue)

# to rename a column
# renameCol = cleanData.rename(columns={"Math": "Mathematics"})
# you rename more than one
# renameCol = cleanData.rename(columns={"Math": "Mathematics", "Science": "Computer Science"})
# print(renameCol)
# view updated columns
# print(cleanData.columns)

# Changing Data types

# check data types
# print(cleanData.dtypes)
# change data type
# changeDtype = cleanData["Science"].astype(str) 
# changeDtype = cleanData["Science"].astype(float) 
# changeDtype = cleanData["Roll No"].astype(str)
# print(changeDtype)
# print(changeDtype.dtype)

# creating new column

# create percentage column
# cleanData["Percentage"] = cleanData["Total Marks"] / 3
# print(cleanData["Percentage"])
# cleanData["Python"] = cleanData["Science"]
# print(cleanData["Python"])

# sorting & filtering
# sortValue = cleanData.sort_values(by=["Math", "English", "Science"])
# sort in descending order
# sortValue = cleanData.sort_values(by="Math", ascending=False)
# print(sortValue)

# filtering
# filterVal = cleanData[cleanData["Math"] > 90]
# print(filterVal)
# above average it can filter
# filterVal = cleanData["Math"].mean()
# aboveAvg = cleanData[cleanData["Math"] > filterVal]
# print(aboveAvg)

# multiple value can filter using AND operator
# mulVal = cleanData[
#     (cleanData["Math"] > 80) & 
#     (cleanData["Science"] > 80)
# ]
# print(mulVal)

# multiple value filter using OR operator 
# mulVal = cleanData[
#     (cleanData["Math"] > 90) | 
#     (cleanData["Science"] > 90)
# ]
# print(mulVal)

