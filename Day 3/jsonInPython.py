# What JSON is and why it's commonly used
# Easy for humans to read and write.
# Easy for machines to parse.
# Used in Web APIs.
# Stores configuration/settings.
# Used to save application data.
# Supported by almost every programming language.

# Reading JSON files
# use with statement to reading JSOn file
# first you can import a json file
# import json

# # then we use with with statement
# with open("students.json", "r") as file:
# # then load a json file
#     data = json.load(file)

# print(data)
# print(data["name"])
# print(data["course"])

# # Writing Data to JSON Files

# import json
# # write any thing you want in JSON format
# student = {
#     "name": "Muhammad",
#     "age": 21,
#     "course": "AI"
# }

# # you used "w" mode for write a data
# with open("student.json", "w") as file:
#     json.dump(student, file)


# # Converting Python dictionaries to JSON

# import json

# student = {
#     "name": "Zainab",
#     "age": 20,
#     "city": "Lahore"
# }

# # use json.dumps() function convert python dictionaries in to json
# jsonData = json.dumps(student)

# print(jsonData)
# print(type(jsonData))



# # Loading JSON Data into Python Objects

# import json

# jsonString = '{"name":"Sara","age":23,"city":"Karachi"}'

# # use json.load (read from a file) use json.loads (read from a string)
# data = json.loads(jsonString)

# print(data)
# print(type(data))
# print(data["city"])


# # using json.load function
# import json

# with open("student.json", "r") as file:
#     data = json.load(file)

# print(data)
# print(type(data))
# print(data["course"])


