# Day 3: File Handling & JSON in Python

## 📌 Overview

Today I learned **File Handling and JSON in Python**. I practiced reading, writing, appending, and storing data permanently using text files and JSON files.

I also upgraded my **Student Record Management System** by adding persistent storage using JSON and implemented **exception handling** to make the application more reliable.

---

## 🔗 How File Handling and JSON Work Together

**File Handling** allows Python programs to create, read, write, and update files, while **JSON** provides a structured format for storing data.

In this project:

* File Handling was used to open, read, and write files.
* The `json` module was used to convert Python lists and dictionaries into JSON format.
* JSON data was converted back into Python objects when reading the file.
* Together, File Handling and JSON enabled the Student Record Management System to save and retrieve student records permanently.

---

## 📚 Topics Covered

### File Handling

* Opening and closing files
* Reading text files
* Writing text files
* Appending data
* Using the `with` statement
* File modes:

  * `r` — Read
  * `w` — Write
  * `a` — Append

### JSON

* Introduction to JSON
* Reading JSON files
* Writing JSON files
* Converting Python objects into JSON
* Loading JSON data into Python objects
* Updating JSON data

### Exception Handling

* Using `try` and `except`
* Handling invalid inputs
* Handling file-related errors
* Making the application more reliable

---

## 💻 Coding Practice

### File Handling

During the practice, I:

* Created a text file.
* Wrote data into a file.
* Read file contents.
* Appended new data.
* Counted the number of lines in a file.
* Practiced different file modes.

### JSON

I also practiced:

* Storing student information in a JSON file.
* Reading data from a JSON file.
* Updating existing student records.
* Adding new student records.
* Saving updated data permanently.

---

# 🚀 Student Record Management System

I upgraded the Student Record Management System to support **persistent JSON storage**.

### Features

* Load student records automatically from `students.json`.
* Save records permanently.
* Add students.
* View all students.
* Search students.
* Update student information.
* Delete students.
* Handle invalid inputs using exception handling.
* Reusable `load_students()` function.
* Reusable `save_students()` function.

### 🔄 Application Workflow

```text
Start Program
      ↓
Load students.json
      ↓
Display Menu
      ↓
Add / View / Search / Update / Delete
      ↓
Save Changes to students.json
      ↓
Continue Program
```

---

## 🧩 Code Reusability

During development, my initial implementation became lengthy because similar file-handling code was repeated in multiple functions.

To improve the structure, I created two reusable functions:

```python
load_students()
save_students()
```

### `load_students()`

Responsible for:

* Opening `students.json`
* Reading stored data
* Converting JSON data into Python objects
* Returning student records

### `save_students()`

Responsible for:

* Receiving updated student records
* Converting Python objects into JSON
* Writing the updated data back to `students.json`

This made the application:

* Cleaner
* Easier to maintain
* More reusable
* More organized
* Closer to professional coding practices

---

## 🛠️ Technologies Used

* Python 3
* File Handling
* JSON
* Exception Handling
* Functions
* Lists
* Dictionaries

---

## 📂 Project Structure

```text
Day 3/
│
├── file.txt
├── fileHandling.py
├── fileHandlingTask.py
├── fileTask.txt
├── jsonInPython.py
├── jsonTask.py
├── students.json
├── updatedRecordManagementSystem.py
├── writeFile.txt
├── README.md
└── requirements.txt
```

---

## 📖 Description of Files

| File                               | Description                                                                   |
| ---------------------------------- | ----------------------------------------------------------------------------- |
| `fileHandling.py`                  | Practice programs for reading, writing, and appending files                   |
| `fileHandlingTask.py`              | File Handling practice tasks                                                  |
| `jsonInPython.py`                  | Practice programs demonstrating JSON operations                               |
| `jsonTask.py`                      | JSON practice tasks                                                           |
| `students.json`                    | Stores student records permanently                                            |
| `updatedRecordManagementSystem.py` | Student Record Management System with JSON persistence and exception handling |
| `file.txt`                         | Sample text file for reading practice                                         |
| `fileTask.txt`                     | Text file used in File Handling tasks                                         |
| `writeFile.txt`                    | Output file created during writing practice                                   |
| `README.md`                        | Project documentation                                                         |
| `requirements.txt`                 | Project dependencies                                                          |

---

## 🎯 Learning Outcomes

After completing Day 3, I learned how to:

* Work with text files in Python.
* Read, write, and append data.
* Use file modes such as `r`, `w`, and `a`.
* Use the `with` statement for file operations.
* Store data permanently using JSON.
* Read and update JSON files.
* Convert Python objects into JSON format.
* Load JSON data into Python objects.
* Handle exceptions using `try` and `except`.
* Build a persistent Student Record Management System.
* Create reusable functions.
* Write cleaner and maintainable Python code.

---

## ⚠️ Challenges Faced

During this project, I faced several challenges:

* Understanding how to store student records permanently using JSON.
* Understanding how JSON works together with File Handling.
* Designing the logic to automatically load data when the program starts.
* Saving changes after every operation.
* Managing file-related exceptions.
* Avoiding repeated code across multiple functions.
* Resolving Git and GitHub issues while pushing project updates and working with branches.

Initially, managing File Handling and JSON together was confusing. I took guidance from **ChatGPT** to better understand the concepts and improve my program structure.

This helped me understand the importance of **code reusability, clean code, and maintainable program structure**.

---

## 📌 Plan for Next Working Day

* Complete the assigned internship tasks.
* Continue improving Python programming and problem-solving skills.
* Practice File Handling and JSON with more exercises.
* Strengthen Git and GitHub knowledge.
* Improve version control and project management skills.

---

## 👨‍💻 Author

**Muhammad Ashhad**

**MLB Internship — Day 3**
