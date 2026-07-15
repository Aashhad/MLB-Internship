import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# df = pd.read_csv("Day 5/cleaned_student_performance.csv")


# Bar chart showing the average marks of each student.
# plt.figure(figsize=(10, 6))
# plt.bar(df["Roll_No"], df["Average_Score"])
# plt.title("Average Marks of Each Student")
# plt.xlabel("Students")
# plt.ylabel("Average Score")
# plt.show()

# Histogram showing the distribution of Average Scores.
# plt.figure(figsize=(8,5))
# plt.hist(df["Average_Score"], bins=8)
# plt.title("Distribution of Average Scores")
# plt.xlabel("Average Score")
# plt.ylabel("Number of Students")
# plt.show()

# Scatter plot comparing Python and Machine Learning marks.
# plt.figure(figsize=(8,6))
# plt.scatter(df["Python"], df["Machine_Learning"])
# plt.title("Python & Machine Learning")
# plt.xlabel("Python")
# plt.ylabel("Machine Learning")
# plt.show()

# performance_counts = df["Performance"].value_counts()
# plt.figure(figsize=(7,7))
# plt.pie(
#     performance_counts,
#     labels=performance_counts.index,
#     autopct="%1.1f%%",
#     startangle=90
# )

# plt.title("Performance Category Distribution")
# plt.show()

# plt.figure(figsize = (10, 6))
# plt.boxplot([
#     df["Python"],
#     df["Machine_Learning"],
#     df["Data_Science"]
# ])
# plt.title("Marks Distribution Across Subjects")
# plt.xlabel("Subjects")
# plt.ylabel("Marks")
# plt.show()


# subjects = [
#     "Python",
#     "Data_Science",
#     "Machine_Learning"
# ]
# plt.figure(figsize=(10, 6))
# plt.boxplot([df[sub] for sub in subjects])
# # add subjects name to x-axis 
# plt.xticks(range(1, len(subjects) + 1), subjects)
# plt.title("Spread of Marks in All Subjects")
# plt.xlabel("Subjects")
# plt.ylabel("Marks")
# plt.show()
