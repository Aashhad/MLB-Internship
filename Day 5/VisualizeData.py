# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# df = pd.read_csv("Day 5/students_dataset.csv")

# plt.figure(figsize = (10, 6))
# plt.bar(df["Roll_No"], df["Total_Marks"])
# plt.title("Student Record")
# plt.xlabel("Roll No of Students")
# plt.ylabel("Total Marks of Students")
# plt.show()

# plt.figure(figsize = (10, 6))
# plt.plot([
#     df["Math"],
#     df["Science"],
#     df["English"]
# ])
# plt.title("Student Record")
# plt.xlabel("Roll No of Students")
# plt.ylabel("Total Marks of Students")
# plt.show()

# plt.figure(figsize=(10, 6))
# plt.hist(df["Total_Marks"], bins=10)
# plt.title("Distribution of Total Marks")
# plt.xlabel("Total Marks")
# plt.ylabel("Number of Students")
# plt.show()

# plt.figure(figsize = (10, 6))
# plt.scatter(df["Roll_No"], df["Total_Marks"])
# plt.title("Student Record")
# plt.xlabel("Roll No of Students")
# plt.ylabel("Total Marks of Students")
# plt.show()

# plt.figure(figsize = (10, 6))
# plt.boxplot([df["Roll_No"], df["Total_Marks"]])
# plt.title("Student Record")
# plt.xlabel("Roll No of Students")
# plt.ylabel("Total Marks of Students")
# plt.show()

# SEABORN CHARTS using sns

# plt.figure(figsize = (10, 6))
# sns.boxplot(data=df[["Math", "Science", "English"]])
# plt.title("Student Record")
# plt.xlabel("Roll No of Students")
# plt.ylabel("Total Marks of Students")
# plt.show()

# plt.figure(figsize = (10, 6))
# plt.scatter(df["Roll_No"], df["Total_Marks"])
# plt.title("Student Record")
# plt.xlabel("Roll No of Students")
# plt.ylabel("Total Marks of Students")
# plt.show()

# plt.figure(figsize=(10, 6))
# sns.histplot(df["Total_Marks"], bins=10)
# plt.title("Distribution of Total Marks")
# plt.xlabel("Total Marks")
# plt.ylabel("Number of Students")
# plt.show()


# plt.figure(figsize = (10, ))
# sns.barplot(x=df["Roll_No"], y=df["Total_Marks"])
# plt.title("Student Record")
# plt.xlabel("Roll No of Students")
# plt.ylabel("Total Marks of Students")
# plt.show()