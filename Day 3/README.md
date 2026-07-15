📌 Overview

Today I learned File Handling and JSON in Python. I practiced reading, writing, appending, and storing data permanently using text files and JSON files. I also upgraded my Student Record Management System by adding persistent storage using JSON and implemented exception handling to make the application more reliable.

🔗 How File Handling and JSON Work Together

File Handling allows Python programs to create, read, write, and update files, while JSON provides a structured format for storing data.

In this project:

File Handling was used to open, read, and write files.
The json module was used to convert Python lists and dictionaries into JSON format and convert JSON back into Python objects.
Together, they enabled the Student Record Management System to save and retrieve student records permanently.
⚡ Challenges Faced

During this project, I faced several challenges:

Understanding how to store student records permanently using JSON.
Designing the logic to automatically load data when the program starts and save changes after every operation.
My initial implementation became lengthy and difficult to manage.
I found myself repeating the same code in multiple functions.
Managing File Handling and JSON together was confusing at first.
I took guidance from ChatGPT to better understand the concepts and improve the program structure.
Based on that guidance, I created two reusable functions:
load_students()
save_students()
This made my code cleaner, easier to maintain, more efficient, and closer to professional coding practices.

These challenges improved my understanding of:

File Handling
JSON
Exception Handling
Code Reusability
Writing clean and maintainable Python code
📚 Topics Covered
File Handling
Opening and closing files
Reading text files
Writing text files
Appending data
Using the with statement
File modes (r, w, a)
JSON
Introduction to JSON
Reading JSON files
Writing JSON files
Converting Python objects to JSON
Loading JSON into Python objects
💻 Coding Practice
File Handling
Created a text file
Wrote data into a file
Read file contents
Appended data
Counted the number of lines in a file
JSON
Stored student information in a JSON file
Read data from a JSON file
Updated existing student records
Added new student records
🚀 Student Record Management System (Persistent Version)
Features
Load student records automatically from students.json
Save records permanently
Add students
View all students
Search students
Update student information
Delete students
Exception handling for invalid inputs
Reusable load_students() and save_students() functions
🛠️ Technologies Used
Python 3
File Handling
JSON
Exception Handling
Functions
Lists
Dictionaries
📂 Project Structure
Day 3/
│── file.txt
│── fileHandling.py
│── fileHandlingTask.py
│── fileTask.txt
│── jsonInPython.py
│── jsonTask.py
│── students.json
│── updatedRecordManagementSystem.py
│── writeFile.txt
│── README.md
│── requirements.txt
📖 Description of Files
File	Description
fileHandling.py	Practice programs for reading, writing, and appending files
fileHandlingTask.py	File Handling practice tasks
jsonInPython.py	Practice programs demonstrating JSON operations
jsonTask.py	JSON practice tasks
students.json	Stores student records permanently
updatedRecordManagementSystem.py	Student Record Management System with JSON persistence and exception handling
file.txt	Sample text file for reading practice
fileTask.txt	Text file used in file handling tasks
writeFile.txt	Output file created during writing practice
README.md	Project documentation
requirements.txt	Project dependencies
🎯 Learning Outcomes

After completing Day 3, I learned how to:

Work with text files in Python
Read, write, and append data
Use file modes (r, w, a)
Store data permanently using JSON
Read and update JSON files
Convert Python objects into JSON format
Load JSON data into Python objects
Handle exceptions using try and except
Build a persistent Student Record Management System
Write cleaner and reusable Python code

⚠️ Challenges
Understanding how JSON integrates with File Handling
Learning persistent data storage using JSON
Managing file-related exceptions
Resolving Git and GitHub issues while pushing project updates and working with branches
📌 Plan for Next Working Day (Monday)
Complete the assigned internship tasks
Continue improving Python programming and problem-solving skills
Practice File Handling and JSON with more exercises
Strengthen Git and GitHub knowledge for better version control and project management


👨‍💻 Author
Muhammad Ashhad

Day 3