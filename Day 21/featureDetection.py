import cv2
import numpy as np
import time


# LOAD IMAGES

image1 = cv2.imread("Day 21/images/inputImages/building (1).jpg")
image2 = cv2.imread("Day 21/images/inputImages/building (2).jpg")


# Check if images loaded successfully
if image1 is None:
    print("Error: book (1).jpg not found!")
    exit()
if image2 is None:
    print("Error: book (2).jpg not found!")
    exit()

print("Images loaded successfully!")


# HARRIS CORNER DETECTION
print("\n================ HARRIS CORNER DETECTION ================")

# Convert image to grayscale
gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)

# Harris requires float32 input
gray_float = np.float32(gray1)

# Start timer
harris_start = time.time()

# Harris Corner Detection
harris = cv2.cornerHarris(
    gray_float,
    blockSize=2,
    ksize=3,
    k=0.04
)


# Dilate the result so corners are easier to see
harris = cv2.dilate(harris, None)

# Threshold
threshold = 0.01 * harris.max()

# Create output image
harris_result = image1.copy()

# Find coordinates of detected corners
corner_coordinates = np.argwhere(harris > threshold)

# Mark corners in red
harris_result[harris > threshold] = [0, 0, 255]

# Calculate time
harris_time = time.time() - harris_start

# Number of detected corner pixels
harris_corners = len(corner_coordinates)

print("Harris corners detected:", harris_corners)
print("Harris processing time:", round(harris_time, 5), "seconds")


# CREATE ORB DETECTOR
print("\n================ ORB KEYPOINT DETECTION ================")

orb = cv2.ORB_create(
    nfeatures=1000,
    scaleFactor=1.2,
    nlevels=8,
    edgeThreshold=31,
    firstLevel=0,
    WTA_K=2,
    scoreType=cv2.ORB_HARRIS_SCORE,
    patchSize=31,
    fastThreshold=20
)


# DETECT ORB KEYPOINTS IN IMAGE 1

orb_start = time.time()

keypoints1, descriptors1 = orb.detectAndCompute(
    gray1,
    None
)
orb_time = time.time() - orb_start
print("ORB keypoints detected:", len(keypoints1))

# Check descriptors
if descriptors1 is None:
    print("Error: No ORB descriptors found in image 1.")
    exit()

print("ORB descriptor shape:", descriptors1.shape)
print("ORB processing time:", round(orb_time, 5), "seconds")


# VISUALIZE ORB KEYPOINTS

# it may give a very large circle 
# orb_keypoints_image = cv2.drawKeypoints(
#     image1,
#     keypoints1,
#     None,
#     color=(0, 255, 0),
#     flags=cv2.DrawMatchesFlags_DRAW_RICH_KEYPOINTS
# )

# i give small circle in output that why we use this
orb_keypoints_image = image1.copy()

for kp in keypoints1:

    x = int(kp.pt[0])
    y = int(kp.pt[1])

    # Small keypoint circle
    cv2.circle(
        orb_keypoints_image,
        (x, y),
        3,
        (0, 255, 0),
        1
    )

    # Orientation line
    angle = np.deg2rad(kp.angle)

    length = 8

    end_x = int(x + length * np.cos(angle))
    end_y = int(y + length * np.sin(angle))

    cv2.line(
        orb_keypoints_image,
        (x, y),
        (end_x, end_y),
        (0, 255, 0),
        1
    )


# DETECT ORB KEYPOINTS IN IMAGE 2

gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
keypoints2, descriptors2 = orb.detectAndCompute(gray2, None)
print("ORB keypoints in image 2:", len(keypoints2))


# Check descriptors
if descriptors2 is None:
    print("Error: No ORB descriptors found in image 2.")
    exit()

print("Image 2 descriptor shape:", descriptors2.shape)


# BRUTE FORCE MATCHER
print("\n================ FEATURE MATCHING ================")
# ORB descriptors are binary.
# Therefore, use Hamming distance.

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Start matching timer
match_start = time.time()
matches = bf.match(descriptors1, descriptors2)

# Calculate matching time
match_time = time.time() - match_start

# Sort matches by distance
matches = sorted(matches, key=lambda match: match.distance)
print("Total matches:", len(matches))
print("Matching time:", round(match_time, 5),"seconds")

# FILTER GOOD MATCHES

# Calculate average distance
if len(matches) > 0:

    distances = [
        match.distance
        for match in matches
    ]

    average_distance = np.mean(distances)

    print(
        "Average match distance:",
        round(average_distance, 2)
    )


# Take best 50 matches
good_matches = matches[:50]
print("Good matches displayed:", len(good_matches))

# DRAW FEATURE MATCHES
matched_image = cv2.drawMatches(
    image1,
    keypoints1,
    image2,
    keypoints2,
    good_matches,
    None,
    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
)


# PERFORMANCE COMPARISON

print("\n================ PERFORMANCE COMPARISON ================")
print(f"Harris Corner Detection : " f"{harris_corners} corners | " f"{harris_time:.5f} seconds")
print(f"ORB Keypoint Detection   : " f"{len(keypoints1)} keypoints | " f"{orb_time:.5f} seconds")
print(f"ORB Feature Matching     : " f"{len(matches)} matches | " f"{match_time:.5f} seconds")


# SAVE RESULTS
output_folder = "Day 21/images/outputImages"
import os
# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Save original image
cv2.imwrite(f"{output_folder}/original.jpg", image1)
# Save Harris result
cv2.imwrite(f"{output_folder}/harris_corners.jpg", harris_result)
# Save ORB keypoints
cv2.imwrite(f"{output_folder}/orb_keypoints.jpg", orb_keypoints_image)
# Save feature matches
cv2.imwrite(f"{output_folder}/orb_matches.jpg",matched_image)
print("Results saved successfully!")
print(f"Original image     : {output_folder}/original.jpg")
print(f"Harris corners     : {output_folder}/harris_corners.jpg")
print(f"ORB keypoints      : {output_folder}/orb_keypoints.jpg")
print(f"ORB matches        : {output_folder}/orb_matches.jpg")
