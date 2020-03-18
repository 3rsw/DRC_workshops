# DRC Workshop 2 - Sample Code

# Import Relevant Libraries
import cv2
import numpy as np
import time

# Request Footage from Camera / Footage
cap = cv2.VideoCapture(0)

while(True):

    # Capture a Single Frame from the Camera
    _, frame = cap.read()

    # === Blurring the Image ===

    # Applying a Gaussian Blur - Efficient and Clean Blur
    blur_gaussian = cv2.GaussianBlur(frame, (5,5), 0)
    # Applying a Bilateral Filter - Good for Retaining Edges
    blur_bilateral = cv2.bilateralFilter(frame, 9, 75, 75)

    cv2.imshow('Original Frame', frame)
    cv2.imshow('Gaussian Blur', blur_gaussian)
    cv2.imshow('Bilateral Filter', blur_bilateral)

    # === Filtering Colours ===

    # Converting the Image to the HSV Colourspace
    hsv = cv2.cvtColor(blur_bilateral, cv2.COLOR_BGR2HSV)

    # Filtering a Colour
    mask = cv2.inRange(hsv, np.array([15, 50, 60]), np.array([25, 160, 130]))

    # === Morphological Operations ===

    # Kernel for the Range of Morphological Operations
    kernel = np.ones((5,5), np.uint8)
    # Erodes borders of masks and noise
    erosion = cv2.erode(mask, kernel, iterations = 3)
    # Dilates borders of masks
    dilation = cv2.dilate(mask, kernel, iterations = 3)
    # Opening = Erosion -> Dilation
    # Good for removing noise from the background.
    open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # Closing = Dilation -> Erosion
    # Good for removing noise from the foreground.
    close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    cv2.imshow('Original Mask', mask)
    cv2.imshow('Erosion Only', erosion)
    cv2.imshow('Dilation Only', dilation)
    cv2.imshow('Opening', open)
    cv2.imshow('Closing', close)

    # === Contour Detection ===

    # Detecting Contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Drawing the Outlines of the Contours
    contourFrame = frame
    cv2.drawContours(contourFrame, contours, -1, (0,0,255), 3)

    # === Canny Edges and Hough Line Transform ===
    # Using the Canny Edge Detection
    edges = cv2.Canny(frame, 100, 200)
    # Using Hough Line Transform to Detect and Draw Lines
    houghFrame = frame
    minLineLength = 10
    maxLineGap = 20
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
    for x1,y1,x2,y2 in lines[0]:
        cv2.line(houghFrame,(x1,y1),(x2,y2),(0,255,0),2)
        
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Detected Canny Edges', edges)
    cv2.imshow('Hough Line Transform', houghFrame)


    # If the key 'q' is pressed, exit the program.
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# End Video Capture and Close all Opened Windows
cap.release()
cv2.destroyAllWindows()
