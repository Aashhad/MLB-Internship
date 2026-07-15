import numpy as np
import pandas as pd

df = pd.read_csv("Day 4/students_dataset.csv")
print(df)

# Display dataset information.
print("DataSet Information:", df.info())

# Calculate average marks for each subject.
subjects = df[["Mathematics", "Science" , "English" ,"Social Studies"]].mean()
print("Average marks of Each Subject:", subjects)


# Identify the top 5 performing students.
toppers = df.nlargest(5, "Total Marks")
print(toppers)


# Find students scoring below the average.
average= df['Total Marks'].mean()  # Average Total Marks
print("Average Total Marks:", average)
print("Students scoring below the average Total_Marks:")
belowAverageStudents = df[df['Total Marks'] < average]
print(belowAverageStudents)


# Display the total number of students.
print("Total Number of Students:", len(df))

# Save the cleaned or analyzed dataset as a new CSV file

df.to_csv("AnalyzedDataset.csv", index=False)

print("NumPy Version:", np.__version__)
print("Pandas Version:", pd.__version__)
