import json

# # Store student information in a JSON file.
students = [{
    "name": "Ashhad", 
    "roll": "101", 
    "age": 23, 
    "course": "AI"
            }]

with open("students.json", "w") as file:
    # use indent parameter make JSON more readable
    json.dump(students, file, indent =4)


# # Read data from a JSON file.
with open("students.json", "r") as file:
    students = json.load(file)

print(students)

# Update an existing student's information.

with open("students.json", "r") as file:
    data = json.load(file)

roll = int(input("Enter Roll Number: "))
newName = input("Enter New Name: ")

found = False

for student in data:
    if student["roll"] == roll:
        student["name"] = newName
        found = True
        break

if found:
    with open("students.json", "w") as file:
        json.dump(data, file, indent=4)
    print("Student updated successfully!")
else:
    print("Student not found!")

# Add a new student to the JSON file.

with open ("students.json", "r") as file:
    data = json.load(file)

roll = int(input("Enter Roll Number: "))
name = (input("Enter Name: "))
age = int(input("Enter Age: "))
city = (input("Enter City: "))

newStudents = {
    "roll": roll,
    "name": name,
    "age" : age,
    "city": city
}

data.append(newStudents)

with open("students.json", "w") as file:
    json.dump(data, file, indent=4)

print("Student Added")







