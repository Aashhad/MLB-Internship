# Student Record Management System (Persistent Version)

import json

# Load students from JSON file
try:
    with open("students.json", "r") as file:
        students = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    students = []


# Save students to JSON file
def save_students():
    with open("students.json", "w") as file:
        json.dump(students, file, indent=4)


def find_student(roll):
    for student in students:
        if student["roll"] == roll:
            return student
    return None


# Add Student
def add_student():
    print("\n----- Add Student -----")

    name = input("Enter Name: ")
    roll = input("Enter Roll Number: ")

    if find_student(roll):
        print("Roll Number already exists!\n")
        return

    try:
        age = int(input("Enter Age: "))
    except ValueError:
        print("Age must be a number.\n")
        return

    course = input("Enter Course: ")

    student = {
        "name": name,
        "roll": roll,
        "age": age,
        "course": course
    }

    students.append(student)
    save_students()

    print("Student added successfully!\n")


# View Students
def view_students():
    if len(students) == 0:
        print("No students found.\n")
        return

    print("\n========== Student Records ==========")

    for student in students:
        print(f"Name   : {student['name']}")
        print(f"Roll   : {student['roll']}")
        print(f"Age    : {student['age']}")
        print(f"Course : {student['course']}")
        print("-------------------------------------")


# Search Student
def search_student():
    roll = input("Enter Roll Number to Search: ")

    student = find_student(roll)

    if student:
        print("\nStudent Found")
        print(f"Name   : {student['name']}")
        print(f"Roll   : {student['roll']}")
        print(f"Age    : {student['age']}")
        print(f"Course : {student['course']}")
        print()
    else:
        print("Student not found.\n")


# Update Student
def update_student():
    roll = input("Enter Roll Number to Update: ")

    student = find_student(roll)

    if student:
        print("\nCurrent Information")
        print(f"Name   : {student['name']}")
        print(f"Age    : {student['age']}")
        print(f"Course : {student['course']}")

        print("\nLeave blank if you don't want to change.")

        name = input("New Name: ")
        age = input("New Age: ")
        course = input("New Course: ")

        if name != "":
            student["name"] = name

        if age != "":
            student["age"] = age

        if course != "":
            student["course"] = course

        save_students()

        print("Student updated successfully!\n")

    else:
        print("Student not found.\n")


# Delete Student
def delete_student():
    roll = input("Enter Roll Number to Delete: ")

    student = find_student(roll)

    if student:
        students.remove(student)
        save_students()
        print("Student deleted successfully!\n")
    else:
        print("Student not found.\n")


# Main Menu
while True:

    print("\n========== Student Record Management System ==========")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Please enter a number between 1 and 6.\n")
        continue

    if choice == 1:
        add_student()

    elif choice == 2:
        view_students()

    elif choice == 3:
        search_student()

    elif choice == 4:
        update_student()

    elif choice == 5:
        delete_student()

    elif choice == 6:
        print("\nThank you for using Student Record Management System!")
        break

    else:
        print("Invalid Choice! Please enter a number between 1 and 6.\n")