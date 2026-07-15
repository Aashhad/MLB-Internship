# Student Grading System

name = input("Enter student name: ")
student_class = input("Enter class: ")

subjects = {}
num_subjects = int(input("How many subjects? "))

for i in range(num_subjects):
    subject_name = input(f"Enter subject {i+1} name: ")
    marks = float(input(f"Enter marks for {subject_name}: "))
    subjects[subject_name] = marks

total = sum(subjects.values())
average = total / num_subjects

if average >= 90:
    grade = "A"
elif average >= 75:
    grade = "B"
elif average >= 50:
    grade = "C"
else:
    grade = "F"

print("\n--- Student Report ---")
print(f"Name: {name}")
print(f"Class: {student_class}")
print("Subjects and Marks:")
for subject, mark in subjects.items():
    print(f"  {subject}: {mark}")
print(f"Average: {average:.2f}")
print(f"Grade: {grade}")