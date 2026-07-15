# # you open a file using the open() function
# file = open("file.txt")
# # you can read the contents of the file using the read() method
# data = file.read()
# print(data)
# # you must close the file after you are done with it using the close() method
# file.close()

# # first you can write any thing you want in strings
# intro = "Hey Ashhad you do amazing work keep it up."
# # Then open a file, "w" is used for write in file
# file = open("writeFile.txt", "w")
# # then .write() is use for write you can see make a new file.
# file.write(intro)
# # then close a file
# file.close()

# # append data to files
# intro = "More power to you."
# # Then open a file, "a" is used for append in file
# file = open("writeFile.txt", "a")
# # then .write() is use for write you can see make a new file & append you can add any thing in it. if you can run many time it can append many times
# file.write(intro)
# # then close a file
# file.close()

# # Delete a file
# # To delete a file, you must import the OS module, and run its os.remove() function
# import os 
# # run its os.remove() function
# os.remove("writefile.txt")


# # Delete a folder
# import os
# os.rmdir("myfolder")


# # Using the with statment
# with open("file.txt") as file:
#      print(file.read())
# # if you use with statement you can use close function it can automatically close a file 


# File modes
# r is used for reading a file
# w is used for writing a file
# a is used for append a file
# + is used of updating
# rb is used for reading binary mode
# rt is used for reading binary text




 


