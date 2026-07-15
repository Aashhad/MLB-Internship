import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Day 5/cleaned_student_performance.csv")

# How many students are in the dataset?
print(len(df))

# What is the average score for each subject?
subjects = ["Python", "Machine_Learning", "Data_Science"]
subjectAverage = df[subjects].mean()

print("Average Score for Each Subject")
print(subjectAverage)

# Who are the Top 5 performing students?
top5 = df.sort_values(by="Average_Score", ascending=False).head(5)

print("Top 5 Performing Students")
print(top5[["Roll_No", "Name", "Average_Score", "Performance"]])

# Which students need improvement?
need_improvement = df[df["Performance"] == "Needs Improvement"]

print("Students Needing Improvement")
print(need_improvement[["Roll_No", "Name", "Average_Score"]])

# Which subject has the highest class average?
highestAverage = subjectAverage.max()
print(f"Average Marks: {highestAverage:.2f}")

# Visualize your findings using appropriate charts.
plt.figure(figsize=(8,5))
plt.bar(subjectAverage.index, subjectAverage.values)
plt.title("Average Marks by Subject")
plt.xlabel("Subjects")
plt.ylabel("Average Marks")
plt.xticks(rotation=15)
plt.savefig("Day 5/generatedCharts/Students Average", dpi=300)
plt.show()


plt.figure(figsize=(8,5))
plt.bar(top5["Roll_No"], top5["Average_Score"])
plt.title("Top 5 Performing Students")
plt.xlabel("Students")
plt.ylabel("Average Score")
plt.savefig("Day 5/generatedCharts/Top 5 student", dpi=300)
plt.show()


performance_counts = df["Performance"].value_counts()

plt.figure(figsize=(7,7))
plt.pie(
    performance_counts,
    labels=performance_counts.index,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Performance Category Distribution")
plt.savefig("Day 5/generatedCharts/Student Performance", dpi=300)
plt.show()


plt.figure(figsize=(8,5))
sns.histplot(df["Average_Score"], bins=8)
plt.title("Distribution of Average Scores")
plt.xlabel("Average Score")
plt.ylabel("Number of Students")
plt.savefig("Day 5/generatedCharts/Distribution of Average Scores", dpi=300)
plt.show()


plt.figure(figsize=(10, 6))
sns.boxplot(data=df[subjects])
# add subjects name to x-axis 
plt.xticks(range(1, len(subjects) + 1), subjects)
plt.title("Spread of Marks in All Subjects")
plt.xlabel("Subjects")
plt.ylabel("Marks")
plt.savefig("Day 5/generatedCharts/Spread of Marks in All Subjects", dpi=300)
plt.show()