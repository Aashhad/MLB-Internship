import cv2
# import os
import numpy as np



# # read and image  
# image = cv2.imread("Day 14/sampleImages/car.jpg")
# cv2.imshow("Car Image",image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # Display dimensions
# height, width, channel = image.shape
# # display file size
# fileSize = os.path.getsize("Day 14/sampleImages/car.jpg")
# fileSizeKb = fileSize / 1024
# print("Image Width :", width, "pixels")
# print("Image Height:", height, "pixels")
# print("Channels    :", channel) 
# print(f"File Size   : {fileSize:.2f} KB")


# # Convert a color image to grayscale.
# colorConversion = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow("GrayScale",colorConversion)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Resize an image to different resolutions.
img = cv2.imread("Day 14/sampleImages/bike.jpg")
# resize = cv2.resize(img, (700,500))
# cv2.imshow("Resize Image", resize)
# # save the image 
# cv2.imwrite("Day 14/outputImages/Resize Image.jpg", resize)
# cv2.waitKey(0)
# cv2.destroyAllWindows

# # Crop different regions of an image.
# cropped = img[400:850, 500:750]
# cropped1 = img[350:1450, 1000:2000]
# # cropped2 = img[800:1250, 1300:1950]
# cv2.imshow("Cropped Image", cropped)
# cv2.imshow("Cropped Image1", cropped1)
# cv2.imwrite("Day 14/outputImages/Cropped Image.jpg", cropped)
# cv2.imwrite("Day 14/outputImages/Cropped Image1.jpg", cropped1)
# cv2.waitKey(0)
# cv2.destroyAllWindows



# Rotate the image by 90°, 180°, and 270°.
# h, w = img.shape[:2]
# center = (2000//2, 700//2)
# center1 = (1300//2, 1500//2)
# center2 = (1550//2, 1600//2)
# matrix = cv2.getRotationMatrix2D(center, 90, 1.0)
# matrix1 = cv2.getRotationMatrix2D(center1, 180, 1.0)
# matrix2 = cv2.getRotationMatrix2D(center2, 270, 1.0)
# rotated90 = cv2.warpAffine(img, matrix, (w,h))
# rotated180 = cv2.warpAffine(img, matrix1, (w,h))
# rotated270 = cv2.warpAffine(img, matrix2, (w,h))
# cv2.imshow('Rotated 90', rotated90)
# cv2.imshow('Rotated 180', rotated180)
# cv2.imshow('Rotated 270', rotated270)
# cv2.imwrite("Day 14/outputImages/Rotated 90.jpg", rotated90)
# cv2.imwrite("Day 14/outputImages/Rotated 180.jpg", rotated180)
# cv2.imwrite("Day 14/outputImages/Rotated 270.jpg", rotated270)
# cv2.waitKey(0)


# Flip the image horizontally and vertically
# for horizontal image
# flipped = cv2.flip(image, 1)
# for vertical image
# flipped1 = cv2.flip(image, 0)
# both horizontal & vertical
# flipped1 = cv2.flip(image, -1)
# cv2.imshow("Horizontal Image", flipped)
# cv2.imshow("Vertical Image", flipped1)
# cv2.imwrite("Day 14/outputImages/Horizontal Image.jpg", flipped)
# cv2.imwrite("Day 14/outputImages/Vertical Image.jpg", flipped1)
# cv2.waitKey(0)

image = cv2.imread("Day 14/sampleImages/black.jpg")
cv2.rectangle(image, (650, 250), (450, 500), (0, 255, 0), -1)

# Circle (center, radius)
cv2.circle(image, (1500, 450), 70, (255, 0, 0), -1)

# Line (start point, end point)
cv2.line(image, (50, 300), (400, 300), (0, 0, 255), 3)
# Polygon
points = np.array([
    [950, 400],
    [1050, 350],
    [1150, 420],
    [1100, 530],
    [980, 500]
], np.int32)
points = points.reshape((-1, 1, 2))
cv2.polylines(image, [points], True, (255, 255, 0), 3)


# Add custom text (your name and today's date) on the image.
text = cv2.putText(image, "My Name is Muhammad Ashhad today date is 30-July-2026",(300, 700), cv2.FONT_HERSHEY_COMPLEX, 2.0, (0, 255, 0), 4)

# Display
cv2.imshow("Shapes", image)
# Save
cv2.imwrite("Day 14/outputImages/shapes.jpg", img)
print("Image saved successfully in Day 14/outputImages/shapes.jpg")
cv2.waitKey(0)
cv2.destroyAllWindows()



