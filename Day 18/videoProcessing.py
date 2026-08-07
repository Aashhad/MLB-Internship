import cv2 
import os

# video path 
video = "Day 18/inputVideos/f1.mp4"

# open video
cap =cv2.VideoCapture(video)

# Check if video opened successfully
if not cap.isOpened():
    print("Error opening video file")
    exit()

# video properties
fps = cap.get(cv2.CAP_PROP_FPS)
frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
totalFrame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print("Video Properties:")
print(f"FPS: {fps}")
print(f"FRAME WIDTH : {frameWidth}")
print(f"FRAME HEIGHT : {frameHeight}")  
print(f"TOTAL FRAME : {totalFrame}")

# create output folder
os.makedirs("Day 18/outputVideos", exist_ok=True)

#  video writer
videoName = os.path.splitext(os.path.basename(video))[0]
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# output video path
outputPath = f"Day 18/outputVideos/{videoName}_output.mp4"

out = cv2.VideoWriter(
    outputPath, # output video path
    fourcc, # output video path
    fps,  # frame per seconds
    (frameWidth, frameHeight) # output video path
)

print(f"\nProcessing Video...\n")
print(f"Output will be saved as: {outputPath}")


# read video frame by frame 
while True:
    ret, frame = cap.read()

    if not ret:
        break

    # convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # apply canny edge detection
    edges = cv2.Canny(blur, 50, 150)
    # display original video
    cv2.imshow("Original Video", frame)
    # display grayscale video
    cv2.imshow("Grayscale Video", gray)
    # display blurred video
    cv2.imshow("Blurred Video", blur)
    # display edges video
    cv2.imshow("Edges Video", edges)
    # save processed frame to output video
    out.write(cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)) 
       # Press Q to Exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# release video capture and writer
cap.release()
out.release()
cv2.destroyAllWindows()
print("Processed video saved successfully!")
