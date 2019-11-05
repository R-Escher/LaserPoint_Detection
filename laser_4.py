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



cap = cv2.VideoCapture('laser4.3gp')

while(cap.isOpened()):
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # splits frame in 3 color channels
    r,g,b = cv2.split(hsv)

    # creates color range
    maskMin = np.array(200)
    maskMax = np.array(255)

    # applies color range mask
    maskRed = cv2.inRange(r, maskMin, maskMax)
    resultRed = cv2.bitwise_and(r, r, mask = maskRed)

    maskGreen = cv2.inRange(g, maskMin, maskMax)
    resultGreen = cv2.bitwise_and(g, g, mask = maskGreen)

    maskBlue = cv2.inRange(b, maskMin, maskMax)
    resultBlue = cv2.bitwise_and(b, b, mask = maskBlue)

    result = np.ndarray([])
    #cv2.absdiff(resultRed, resultBlue, result)

    '''result = np.subtract(resultRed, resultGreen)
    result2 = np.subtract(resultBlue, resultRed)
    result = np.subtract(result, result2)'''

    _, resultRed = cv2.threshold(resultRed,224,255,cv2.THRESH_BINARY)
    _, resultGreen = cv2.threshold(resultGreen,215,255,cv2.THRESH_BINARY)
    _, resultBlue = cv2.threshold(resultBlue,225,255,cv2.THRESH_BINARY)

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