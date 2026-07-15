# import pandas as pd

# Objective of Pandas
# Series & DataFrame
# a = pd.Series([1, 2, 3])
# b = pd.Series([1, 2, 3])
# print(a)

# c = pd.DataFrame({
#     "Age:":[20, 25, 26],
#     "Salary:":[30000, 40000, 60000]           
#                })

# print(c)

# z = pd.DataFrame({"Column1" : a, "Column2" : b})
# print(z)

# Reading CSV files
# df = pd.read_csv("Day 4/students_dataset.csv")
# print(df)
# info of dataset
# print(df.info())
# print first 5 rows of dataset
# print(df.head(5))
# print last five rows of dataset
# print(df.tail(5))

# Exporting datasets
# df = df.to_csv("Day 4/students_dataset.csv", index=False)
# print(df)

# if you can select only one column you can use only one square bracket
# print(df["Name"])
# # if you can select more than one column you can use two square brackets 
# print(df[["Name", "RollNo"]])

# if you selected a row 
# print(df.loc[0])
# print(df.loc[[10, 12, 13]])


# filtering data
# df = pd.read_csv("Day 4/students_dataset.csv")

# print(df["Rank"])
# print(df[df["Rank"] >= 5])
# you can filter one or more column you can use and operator
# print(df[(df["Rank"] > 10) & (df["Total"] > 200)])

# you filter the row with this method
# row = df.loc[0]
# you can filter row index 1 to 6
# row = df.loc[1:6]
# you can filter row index 1 to 6 and column filter Name and Math in b/w all column are appear in output
# row = df.loc[1:6, "Name":"Computer Studies"]
# print(row)


# Basis Statistics
# it can describe all statistics functions
# pd = df.describe()
# it can describe first five row are shown if you cannot write any thing
# pd = df.head()
# it can describe info of dataset
# pd = df.info()
# print(pd)



# Handling Missing Values
# it is use to find missing values if any row have null value this one block can show True in this method
# miss = df.isna()
# it is use to find missing values if any row have null value this one block can show False in this method
# miss = df.notna()
# you can find missing value in specific row
# miss = df[df["Physics"].isna()]

# how to fill missing value
# you can fill value from this method
# miss = df.fillna(0)

# you fill at a specific column
# miss = df["Name"].fillna(0)
# miss = df[["Name", "RollNo"]].fillna(0)

# you can fill value with mean of column you replace missing value in RollNo with the mean of Rank column
# miss = df["RollNo"].fillna(df["Rank"].mean())
# you can fill value with mean of column you replace missing value in RollNo with the max value of Mathematics column
# miss = df["RollNo"].fillna(df["Mathematics"].max())

# you can drop missing values from this method
# miss = df.dropna()

# forward fill
# miss = df.ffill()

# backward fill
# miss = df.bfill()
# print(miss)








