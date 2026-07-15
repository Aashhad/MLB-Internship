import numpy as np
import pandas as pd


df = pd.read_csv("Day 5/students_dataset.csv")

# Check for missing values.
print("Missing Values:")
print(df.isnull().sum())

# Remove duplicate records (if any)
df = df.drop_duplicates()

# Rename one or more columns.
df = df.rename(columns={
    "Math": "Python",
    "Science": "Machine_Learning",
    "English":"Data_Science"
})

# Create a new column named Average_Score by calculating the average marks across all subjects.
df["Average_Score"] = df[
    ["Python", "Data_Science", "Machine_Learning"]
].mean(axis=1)

# Create another column named Performance
def performance(score):
    if score >= 90:
        return "Excellent"
    elif score >= 80:
        return "Good"
    elif score >= 70:
        return "Average"
    else:
        return "Needs Improvement"

df["Performance"] = df["Average_Score"].apply(performance)

# Save the cleaned dataset 
df.to_csv("cleaned_student_performance.csv", index=False)

print("\nData cleaned successfully!")
print(df.head())