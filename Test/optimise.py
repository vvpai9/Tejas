import cv2
import numpy as np
import os

# Initialize webcam
cap = cv2.VideoCapture(0)

# Variable to control frame skipping
#skip_frames = 5  # Skip every 5 frames, adjust as needed

while True:
    # Skip frames
    #for _ in range(skip_frames):
     #   cap.grab()
    
    # Capture frame
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for orange color in HSV
    lower_orange = np.array([0, 0, 200])
    upper_orange = np.array([180, 50, 255])

    # Threshold the HSV frame to create a mask for orange colors
    orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # Find contours in the orange mask
    contours, _ = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables to store information about the largest contour
    largest_contour = None
    largest_contour_area = 0

    # Find the largest contour
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > largest_contour_area:
            largest_contour = contour
            largest_contour_area = area

    # Draw a circle at the centroid of the largest contour
    if largest_contour is not None and len(largest_contour) >= 5:
        # Calculate centroid of the largest contour
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            print("Xcoordinate",cx)
            # print("Ycoordinate",cy)
            f=open("xa.txt","a")
            f.write(str(cx))
            f.write("\n")
            f=open("yb.txt","a")
            f.write(str(cy))
            f.write("\n")
            # Draw a circle at the centroid
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    # Display the resulting frame
    cv2.imshow('Webcam', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()



