#! usr/bin/env python3
import cv2
import numpy as np

def nothing(x):
    pass

def find_contour(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #need to check if contours is empty before we do anything with them
    if contours:
        #only consider the biggest contour, this is helps filter out the noise  
        biggestCont = max(contours, key=cv2.contourArea)
        #Draw the outline of the contours
        cv2.drawContours(frame, biggestCont, -1, (0,255,0), 3)
        
        #One important thing we can find about this contour is its centroid, this can be
        #very good as for example we can tell the car to steer to the point between the
        #two lines centroids
        #first thing we do is find the moments of the centroid, moments is something to
        #do with spacial distribution
        #The centroid is calculated using Cx = M10/M00 and Cy = M01/M00
        M = cv2.moments(biggestCont)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        
        #draw a circle at the centroid to show where it is
        #to draw a circle use cv2.circle(image, (x, y), radius, colour, thickness)
        cv2.circle(frame, (cX, cY), 10, (0, 0, 255), -1)       

        # return a tuple of the x and y coordinates of the centeroid of contour
        return (cX, cY)

def draw_center(blue_center, yellow_center):
    # TODO: Account for if blue center is empty or if yellow center is empty


    # TODO: Draw a circle at the center of the blue center and yellow center
    #to draw a circle use cv2.circle(image, (x, y), radius, colour, thickness)
        


    # TODO: Draw a line to the center of the lines
    #to draw a line use cv2.line(image, (x1, y1), (x2, y2), colour, thickness)



#First thing we will do is load in a video to test on by creating a video capture
#object, make sure the video you want to use is in the same location as this code
#and change the name of the video file to its name, you can also use a camera if
#you want by changing the name to the number corresponding to the camera
cap = cv2.VideoCapture("TrackTest1.avi")

#First lets check the video object could open the video, this is helpful to do as
#weird error messages will be produced if it is not opened properly
if (cap.isOpened()== False): 
    print("Error opening video stream or file")

width = cap.get(3)
height = cap.get(4)
#fps = cap.get(5)

# arrays for the hsv values of the colours
# TODO: Edit last week's program to take a video as input
# then use it to find these values
BLUE_MIN = np.array([0, 0, 0])
BLUE_MAX = np.array([140, 0, 0])

YELLOW_MIN = np.array([0, 0, 0])
YELLOW_MAX = np.array([0, 0, 0])


while(1):
    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only blue colors
    mask_yellow = cv2.inRange(hsv, YELLOW_MIN, YELLOW_MAX)
    mask_blue = cv2.inRange(hsv, BLUE_MIN, BLUE_MAX)

    # Combine both masks using the bitwise_or function
    mask = cv2.bitwise_or(mask_yellow, mask_blue) 

    # Apply color to the mask
    color_filter = cv2.bitwise_and(frame, frame, mask=mask)

    #Apply any filtering you would like to use

    #Find the center of the largest section of blue
    blue_center = find_contour(mask_blue)
    #Find the center of the largest section of yellow
    yellow_center = find_contour(mask_yellow)
    #Find the center point of this
    draw_center(blue_center, yellow_center)

    # TODO: display the windows with their respective mask

    # TODO: END the loop when the q key is pressed


# TODO: Release resources

