import numpy as np
import cv2
from time import sleep

cap = cv2.VideoCapture('laser.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()

    # converts frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

    ret,thresh1 = cv2.threshold(gray,250,255,cv2.THRESH_BINARY)

    # calculate moments of binary image
    M = cv2.moments(thresh1)

    # calculate x,y coordinate of center
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    
    coord = '(' + str(cX) + ' | ' + str(cY) + ')'
    # put text on image
    cv2.putText(thresh1, "laser", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.putText(thresh1, coord, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
    #cv2.putText(thresh1, str(cY), (100, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow('frame',thresh1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    

cap.release()
cv2.destroyAllWindows()