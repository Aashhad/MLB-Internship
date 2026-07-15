#Lists

# departments = ["Human Resources","Finance","Marketing","Information Technology","Operations"]
# print(departments[0]) # indexing
# print(departments[:3]) # slicing
# departments.remove("Operations") # remove
# print(departments)
# departments.append("Sales") # append mean add anything in the last of array
# print(departments)
# departments.insert(2,"Legal") # insert mean add anything in the specific index of array
# print(departments)

# LIST methods
# cities = ["Lahore","Karachi","Islamabad","Multan","Faisalabad"]
# villages = ["Mandi Burewala", "Mandi Bahauddin"]
# chak = ["Chak 55", "Chak 7", "Chak 1L"]

# # Access an item
# print(cities[2])   # Valid index

# # Add an item
# cities.append("RYK")
# print(cities)

# # Remove all items
# cities.clear()
# print(cities)

# # Copy the list
# cities = ["Lahore","Karachi","Islamabad","Multan","Faisalabad"]
# cities_copy = cities.copy()
# print(cities_copy)

# # Count occurrences
# print(cities.count("Lahore"))

# # Extend with another list
# cities.extend(villages)
# print(cities)


# # Insert an item
# cities.insert(2, "Bahawalpur")
# print(cities)

# # Remove item at index 1
# cities.pop(1)
# print(cities)

# # Remove a specific item
# cities.remove("Multan")
# print(cities)   

# # Reverse the list
# cities.reverse()            
# print(cities)

# # Sort the list
# cities.sort()
# print(cities)

# List Comprehension

# fruits = ["apple", "banana", "cherry", "kiwi", "mango", "Peach", "grape", "orange"]
# newFruits = []

# for x in fruits:
#     if "e" in x:
#         newFruits.append(x)

# print(newFruits)

# fruits = ["apple", "banana", "cherry", "kiwi", "mango", "Peach", "grape", "orange"]
# # newFruits = [x for x in fruits if x != "apple"]
# newFruits = [x if x != "apple" else "orange" for x in fruits]
# print(newFruits)


# TUPLES

# numbers = (1, 2, 3, 4, 5)
# print(numbers[0]) # indexing
# print(numbers[:3]) # slicing

# number = (1,) you must use comma after number to make a tuple
# print(type(number))

# months = ("January","February","March","April","May","June","July","August","December")
# print(months)

# Tuples Operations
# months = tuple("January")
# monthsNumber = (1,2,3,4,5,6,7,8,12) 
# months1 = months + monthsNumber concatenation
# print(months[0:]) slicing
# print(months1)

# LIST vs TUPLE
# main thing list is mutable and tuple is immutable
#  list is slower than tuple because list is mutable and tuple is immutable
# list is changed and tuple is fixed
#  list (shopping cart, student names)
# tuple (month names, days of week, colors)

# for example

# list example
# employees = ["Ali","Ahmed","Ayesha","Zainab"]
# employees.append("Hassan") # list is mutable
# employees.remove("Ahmed") # list is mutable
# employees[3] = "Hina" # list is mutable
# print(employees)

# tuple example
# days = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
# print(days)

# Sets
# fruits = {"Apple", "Banana", "Mango"}
# print(fruits)

# # Set Operations
# fruits = {"Apple", "Banana"}
# fruits.add("Orange")
# print(fruits)
# fruits.update(["Mango", "Grapes"])
# print(fruits)
# fruits.remove("Banana")
# print(fruits)

# # remove duplicates
# numbers = {10, 20, 30, 20, 10, 40, 50}
# duplicateNumbers = set(numbers)
# print(duplicateNumbers)

# # combine all unique numbers
# A = {1, 2, 3}
# B = {3, 4, 5}
# print(A.union(B))
# print(A | B)

# return common numbers
# A = {1, 2, 3}
# B = {3, 4, 5}
# print(A.intersection(B))
# print(A & B)

# Returns elements present in the first set but not in the second.
# A = {1, 2, 3}
# B = {3, 4, 5}
# print(A.difference(B))
# print(A - B)

# Dictionaries
# student = {
#     "name": "Ashhad",
#     "age": 22,
#     "course": "Python"
# }
# print(student)
# print(student["name"])
# print(student["age"])
# # using get()
# print(student.get("course"))
# # update value
# student["course"] = "Data Science"
# print(student)
# # find keys of Dictionary
# print(student.keys())
# # find values of Dictionary
# print(student.values())
# # find items of Dictionary
# print(student.items())
# remove item from Dictionary
# student = {
#     "name": "Ashhad",
#     "age": 22,
#     "course": "Python"
# }
# student.pop("course")
# print(student)
# # Removes the last inserted key-value pair
# student.popitem()
# print(student)
# # clear the dictionary
# student.clear()
# print(student)

# # Nested Dictionary
# students = {
#     "student1": {
#         "name": "Ashhad",
#         "age": 21
#     },
#     "student2": {
#         "name": "Muhammad",
#         "age": 22
#     }
# }
# print(students)

# print(students["student1"]["name"])
# print(students["student2"]["age"])