# Data types

# age = 23
# print(type(age))

# gpa = 3.5
# print(type(gpa))

# active = True
# print(type(active))


# role = "Computer Vision Engineer"
# print(type(role))

# variables that store data
# x = 10
# y = 20
# print(x + y)




# Data structures (list, tuple, dictionary, set)

# LIST it is mutable
# list = [1, 2, 3, 4]
# list.append(5)
# print(list)
# list.pop(2)
# print(list)   
# list.remove(4)
# print(list)   
# list.insert(2, 10)
# print(list)    

# TUPLE it is immutable
# tuple = (1,2,3,4,5)
# print(tuple)
# print(tuple[4])

# SET it is mutable and unordered
# set = {1,2,3,4,5}
# set.add(6) 
# print(set)
# set.remove(3)
# print(set)
# set.discard(10) # does not throw an error if the element is not found   
# print(set)
# set.clear() # removes all elements from the set
# print(set)
# set.update([7,8,9]) # adds multiple elements to the set
# print(set)


# DICTIONARY it is mutable and unordered
# dictionary = {"name": "Ashhad", "age": 23, "city": "RYK"}
# print(dictionary)
# dictionary["age"] = 24 # update value
# print(dictionary)
# dictionary["country"] = "Pakistan" # add new key-value pair
# print(dictionary)
# dictionary.pop("city") # remove key-value pair
# print(dictionary)

# FUNCTIONS
# def greet(name):
#     return f"Hello, {name}!"

# name = "Ashhad"
# print(greet(name))

# def add(a, b):
#     return a+b

# result = add(5, 3)
# print(result)

# def multiply(a, b):
#     return a*b

# result = multiply(5, 3)
# print(result)

# Conditional statements

city = "RYK"

if city == "RYK":
    print("You are in Rahim Yar Khan")
elif city == "LHR":
    print("You are in Lahore")

print(city) 



