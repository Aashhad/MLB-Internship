# 📅 Day 5 – Data Cleaning & Data Visualization using Pandas, Matplotlib, and Seaborn

## 📖 Overview

On Day 5 of my AI & ML Internship, I learned how to clean, prepare, analyze, and visualize datasets using **Pandas**, **NumPy**, **Matplotlib**, and **Seaborn**.

The main objective was to understand the importance of data preprocessing before building Machine Learning models. I performed data cleaning, created different visualizations, and built a Student Performance Dashboard to analyze students' academic performance.

---

# 🎯 Learning Objectives

During this assignment, I learned:

## 🧹 Data Cleaning with Pandas

- Handling missing values
- Removing duplicate records
- Renaming columns
- Creating new columns
- Sorting and filtering data
- Saving cleaned datasets

## 📊 Data Visualization

- Importance of Data Visualization
- Introduction to Matplotlib
- Introduction to Seaborn
- Line Chart
- Bar Chart
- Histogram
- Scatter Plot
- Pie Chart
- Box Plot

---

# 📂 Dataset

Dataset Used:

- `students_dataset.csv`

After cleaning the data, the processed dataset was saved as:

- `cleaned_student_performance.csv`

---

# 🧹 Data Cleaning Tasks Performed

The following preprocessing steps were completed:

- Checked for missing values.
- Removed duplicate records.
- Renamed columns for better readability.
- Created a new column **Average_Score**.
- Created a new column **Performance** based on average score.

### Performance Criteria

| Average Score | Performance |
|--------------|-------------|
| ≥ 90 | Excellent |
| 80–89 | Good |
| 70–79 | Average |
| Below 70 | Needs Improvement |

Finally, the cleaned dataset was saved as:

```
cleaned_student_performance.csv
```

---

# 📈 Data Visualizations Created

The following visualizations were created using Matplotlib:

- 📊 Bar Chart – Average marks of each student
- 📉 Histogram – Distribution of Average Scores
- 📍 Scatter Plot – Python vs Machine Learning marks
- 🥧 Pie Chart – Student Performance Categories
- 📦 Box Plot – Distribution of marks across all subjects

All generated charts are stored inside the **generatedCharts** folder.

---

# 📊 Student Performance Dashboard

The dashboard answers the following questions:

- Total number of students
- Average score for each subject
- Top 5 performing students
- Students who need improvement
- Subject with the highest class average

The results are displayed in a simple and easy-to-understand format along with visualizations.

---

# 💡 Key Insights

After analyzing the dataset, I found that:

1. Most students belong to the **Good** and **Excellent** performance categories.
2. The dashboard easily identifies the Top 5 students and those who need improvement.
3. Data visualization makes it easier to understand score distributions, subject performance, and overall class trends.

---

# 📁 Project Structure

```
Day 5/
│
├── generatedCharts/
│
├── cleanData.py
├── dataCleaningPractice.py
├── dataVisualizationPractice.py
├── VisualizeData.py
├── studentPerformanceDashboard.py
│
├── students_dataset.csv
├── students.csv
├── cleaned_student_performance.csv
│
└── README.md
```

---

# 🛠 Technologies Used

- Python 3
- NumPy
- Pandas
- Matplotlib
- Seaborn

---

# ▶️ How to Run

### 1. Clone the Repository

```bash
git clone <repository-url>
```

### 2. Navigate to Day 5

```bash
cd "Day 5"
```

### 3. Install Required Libraries

```bash
pip install pandas numpy matplotlib seaborn
```

### 4. Run the Scripts

```bash
python cleanData.py

python dataCleaningPractice.py

python dataVisualizationPractice.py

python VisualizeData.py

python studentPerformanceDashboard.py
```

---

# 🎥 Project Demonstration

A short screen recording demonstrating the project and explaining the implementation is included with the submission.

---

# 📚 What I Learned

Through this project, I learned how to:

- Clean real-world datasets using Pandas.
- Handle missing values and duplicate records.
- Create calculated columns using DataFrames.
- Sort and filter data efficiently.
- Build meaningful visualizations using Matplotlib.
- Use Seaborn for enhanced data visualization.
- Extract insights from datasets through analysis.
- Present findings in a professional and easy-to-understand manner.

---

# 🚀 Expected Outcome

By completing this assignment, I can now:

- Prepare datasets for Machine Learning.
- Perform data cleaning using Pandas.
- Visualize data effectively using Matplotlib and Seaborn.
- Analyze datasets and generate meaningful insights.
- Build simple analytical dashboards using Python.

---

## ✅ Project Status

**Completed Successfully ✔️**

👨‍💻 Author
Muhammad Ashhad

Day 4