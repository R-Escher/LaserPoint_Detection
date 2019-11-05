import numpy as np
import cv2
from time import sleep

cap = cv2.VideoCapture('laser2.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()

    # splits frame in 3 color channels
    b,g,r = cv2.split(frame)

    # creates color range
    minRed = np.array(254)
    maxRed = np.array(255)

    # applies color range mask
    maskRed = cv2.inRange(r, minRed, maxRed)
    resultRed = cv2.bitwise_and(r, r, mask = maskRed)

    # creates kernel, then erode and then dilates
    kernel = np.ones((3, 3), np.uint8)
    resultRed = cv2.erode(resultRed, kernel, iterations = 1)
    resultRed = cv2.dilate(resultRed, kernel, iterations = 2) 


    ############# PUTS COORDS OF LASER POINT ON SCREEN FRAME #############################
    
    # calculate moments of binary image
    M = cv2.moments(resultRed)

    if (M["m00"] != 0):
        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    
        coord = '(' + str(cX) + ' | ' + str(cY) + ')'
        # put text on image
        cv2.putText(frame, "laser", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, coord, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
    else:
        cv2.putText(frame, "NOT DETECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
    ######################################################################################

    ############# SHOWS SCREEN FRAME #####################################################

    resized =  cv2.resize(frame, (800, 400), interpolation = cv2.INTER_AREA)
    resized2 =  cv2.resize(resultRed, (800, 400), interpolation = cv2.INTER_AREA)
    cv2.imshow('frame',resized)
    cv2.imshow('lala',resized2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    ######################################################################################
    
    

cap.release()
cv2.destroyAllWindows()