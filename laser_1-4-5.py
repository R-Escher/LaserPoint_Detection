'''
THIS CODE WORKS WITH VIDEOS:

laser.mp4
laser2.mp4 +-
laser4.3gp
laser5.3gp

'''


import numpy as np
import cv2
from time import sleep

def centroid(channel, frame):
    M = cv2.moments(channel)

    if (M["m00"] != 0):
        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    
        coord = '(' + str(cX) + ' | ' + str(cY) + ')'
        # put text on image
        cv2.putText(frame, "laser", (cX - 50, cY - 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
        cv2.putText(frame, coord, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        cv2.circle(frame, (cX, cY), 30, (255, 255, 255) , thickness=2, lineType=8, shift=0)
    else:
        cv2.putText(frame, "NOT DETECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)   

    return frame


################# CHOOSE VIDEOS ######################
cap = cv2.VideoCapture('laser2.mp4')
######################################################

while(cap.isOpened()):
    ret, frame = cap.read()

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # splits frame in 3 color channels
    r,g,b = cv2.split(rgb)

    _, resultRed = cv2.threshold(r,224,255,cv2.THRESH_BINARY)
    _, resultGreen = cv2.threshold(g,215,255,cv2.THRESH_BINARY)
    _, resultBlue = cv2.threshold(b,225,255,cv2.THRESH_BINARY)

    result = cv2.bitwise_xor(resultRed, resultGreen)

    result = cv2.bitwise_and(result, resultRed)

    #result = cv2.bitwise_xor(result, resultGreen)


    # applies color range mask
    '''maskRed = cv2.inRange(r, minRed, maxRed)
    resultRed = cv2.bitwise_and(r, r, mask = maskRed)'''

    # creates kernel, then erode and then dilates
    kernel = np.ones((1,1), np.uint8)
    result = cv2.erode(result, kernel, iterations = 2)
    result = cv2.dilate(result, np.ones((4,4), np.uint8), iterations = 2)
    #result = cv2.erode(result, np.ones((2,2), np.uint8), iterations = 1)
    

    result = centroid(result, frame)

    ############# SHOWS SCREEN FRAME #####################################################

    #resized2 =  cv2.resize(resultRed, (800, 400), interpolation = cv2.INTER_AREA)
    cv2.imshow('h',cv2.resize(result, (800, 400), interpolation = cv2.INTER_AREA))
    #cv2.imshow('s',cv2.resize(resultGreen, (800, 400), interpolation = cv2.INTER_AREA))
    #cv2.imshow('v',cv2.resize(resultBlue, (800, 400), interpolation = cv2.INTER_AREA))
    #cv2.imshow('lala',resized2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('Q'):
        break

    ######################################################################################
    
    

cap.release()
cv2.destroyAllWindows()