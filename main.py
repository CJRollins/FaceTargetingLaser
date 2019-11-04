import cv2
import numpy as np
import serial

cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
ser = serial.Serial('com4', 9600)
videoCamera = cv2.VideoCapture(0)
t0 = 0 # Data Timer
valueX = 0
valueY = 0

while True:
    ret, img = videoCamera.read()
    faces = cascade.detectMultiScale(img, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2) # Creates Rectangle around face detected
        # Final Face calculation
        if(t0>15):
            # Calculate the X & Y coordinates of where the laser should target
            valueX = ((180 - x / (videoCamera.get(cv2.CAP_PROP_FRAME_WIDTH)/180)) + w/2)
            valueY = ((y / (videoCamera.get(cv2.CAP_PROP_FRAME_HEIGHT)/180)) + h/2)

            faceLocation = "X" + str(valueX) + "Y" + str(valueY)
            ser.write(faceLocation)
            t0 = 0 # Reset data timer
    
    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    t0 += 1
    if k == 27:
        break

videoCamera.release()
cv2.destroyAllWindows()
