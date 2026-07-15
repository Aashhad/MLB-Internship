# # Find the largest number in a list.
# numbers = [10, 30, 40, 90, 50, 60, 70, 80, 99]
# print("Largest Number:", max(numbers))


# # Find the second largest number.
# numbers = [45, 12, 78, 34, 89, 23, 67]

# largest = secondLargest = float("-inf")

# for num in numbers:
#     if num > largest:
#         secondLargest = largest
#         largest = num
#     elif num > secondLargest and num != largest:
#         secondLargest = num

# print("Second Largest Number:", secondLargest)


# # Remove duplicates values from a list.
# numbers = [10, 20, 30, 20, 40, 10, 50]
# uniqueNumbers = []

# for num in numbers:
#     if num not in uniqueNumbers:
#         uniqueNumbers.append(num)

# print(uniqueNumbers)

# # Reverse a List Without Using reverse()
# numbers = [10, 20, 30, 40, 50]
# reversedNumbers = []

# for i in range(len(numbers) - 1, -1, -1):
#     reversedNumbers.append(numbers[i])

# print(reversedNumbers)

# # Find common elements between two lists
# list1 = [1, 2, 3, 4, 5]
# list2 = [3, 4, 5, 6, 7]

# common = []

# for item in list1:
#     if item in list2:
#         common.append(item)

# print(common)

# TUPLES
# Count occurrences of an element in a tuple
# numbers = (10, 20, 30, 20, 40, 20)
# count = numbers.count(20)
# print(count)

# Convert a tuple into a list
# numbers = (1, 2, 3, 4)
# # Use list() to convert a tuple into a list.
# numberChanges = list(numbers)
# print(numberChanges)
# print(type(numberChanges))


# Sets
# Find unique values from a list
# numbers = [1, 2, 2, 3, 4, 4, 5, 5]
# uniqueNumbers = set(numbers)
# print(uniqueNumbers)

# Perform union and intersection operations.
# union operations
# set1 = {1, 2, 3, 4}
# set2 = {3, 4, 5, 6}
# # result = set1.union(set2)
# # result = set1 | set2 
# print(result)

# Intersection operations
# set1 = {1, 2, 3, 4}
# set2 = {3, 4, 5, 6}
# result = set1.intersection(set2)
# result = set1 & set2
# print(result)

# Dictionaries
# Create a student record dictionary
# student = {
#     "name": "Ashhad",
#     "age": 23,
#     "course": "Computer Science",
#     "marks": 85
# }
# print(student)

# Calculate average marks of students
# marks = {
#     "Ali": 80,
#     "Ahmed": 90,
#     "Sara": 85,
#     "Ayesha": 95
# }
# total = sum(marks.values())
# average = total / len(marks)
# print("Average Marks:", average)

# Count Frequency of Words in a Sentence
# sentence = "Ashhad doing internship in ML Bench, as a CV Engineer"

# words = sentence.split()

# countFrequency = {}

# for word in words:
#     if word in countFrequency:
#         countFrequency[word] += 1
#     else:
#         countFrequency[word] = 1
# print(countFrequency)


