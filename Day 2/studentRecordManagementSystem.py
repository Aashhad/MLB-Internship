# Student Record Management System

students = []

def findStudent(roll):
    for student in students:
        if student["roll"] == roll:
            return student
    return None

# Add Student
def addStudent():
    print("\nAdd Student")

    name = input("Enter Name: ")
    roll = input("Enter Roll Number: ")

    # Check duplicate roll number
    if findStudent(roll):
        print("Roll Number already exists!\n")
        return

    age = input("Enter Age: ")
    course = input("Enter Course: ")

    student = {
        "name": name,
        "roll": roll,
        "age": age,
        "course": course
    }

    students.append(student)
    print("Student added successfully!\n")

#  View Students 
def viewStudents():
    if len(students) == 0:
        print("")
        return

    print("\n Student Records ")

    for student in students:
        print(f"Name   : {student['name']}")
        print(f"Roll   : {student['roll']}")
        print(f"Age    : {student['age']}")
        print(f"Course : {student['course']}")
        print("")

# Search Student 
def searchStudent():
    roll = input("Enter Roll Number to Search: ")

    student = findStudent(roll)

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
def updateStudent():
    roll = input("Enter Roll Number to Update: ")

    student = findStudent(roll)

    if student:
        print("\nCurrent Information")
        print(f"Name   : {student['name']}")
        print(f"Age    : {student['age']}")
        print(f"Course : {student['course']}")

        print("")

        name = input("New Name: ")
        age = input("New Age: ")
        course = input("New Course: ")

        if name != "":
            student["name"] = name

        if age != "":
            student["age"] = age

        if course != "":
            student["course"] = course

        print("Student updated successfully!\n")

    else:
        print("Student not found.\n")

#  Delete Student
def deleteStudent():
    roll = input("Enter Roll Number to Delete: ")

    student = findStudent(roll)

    if student:
        students.remove(student)
        print("Student deleted successfully!\n")
    else:
        print("Student not found.\n")


while True:

    print("\nStudent Record Management System ")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        addStudent()

    elif choice == "2":
        viewStudents()

    elif choice == "3":
        searchStudent()

    elif choice == "4":
        updateStudent()

    elif choice == "5":
        deleteStudent()

    elif choice == "6":
        print("\nThank you for using Student Record Management System!")
        break

    else:
        print("\nInvalid Choice! Please enter a number between 1 and 6.\n")