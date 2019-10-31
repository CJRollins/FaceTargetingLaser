import cv2
import numpy as np
import serial

cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
ser = serial.Serial('com4', 9600)
videoCamera = cv2.VideoCapture(0)
t0 = 0
valueX = 0
valueY = 0

maxCap = 120
minCap = 75

multiplicative = videoCamera.get(cv2.CAP_PROP_FRAME_HEIGHT)/maxCap
while True:
    ret, img = videoCamera.read()
    faces = cascade.detectMultiScale(img, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)

        # Calculate X
        if((maxCap-(x/multiplicative)) > maxCap): valueX = maxCap
        elif((maxCap-(x/multiplicative)) < minCap): valueX = minCap
        else: valueX = (maxCap-(x/multiplicative))

        # Calculate Y
        if((y/multiplicative) > maxCap): valueY = maxCap
        elif(((y/multiplicative)) < minCap): valueY = minCap
        else: valueY = (y/multiplicative)

        # Final Face calculation
        faceLocation = "X" + str(valueX) + "Y90"
        ser.write(faceLocation)
        print(faceLocation)
        t0 = 0
    
    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    t0 += 1
    if k == 27:
        break

videoCamera.release()
cv2.destroyAllWindows()

# str(180-(x/multiplicative)