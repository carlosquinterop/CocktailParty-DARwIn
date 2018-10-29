import cv2
import numpy as np
import time
import sys

CAMERA_INDEX = 0

capture = cv2.VideoCapture(CAMERA_INDEX)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
capture.set(cv2.CAP_PROP_FPS, 10)

doorMin = np.array([110,70,40]) #AZUL
doorMax = np.array([130,255,255])

clientMin = np.array([40,60,60]) #VERDE
clientMax = np.array([60,255,255])

centerMin = np.array([140,30,30]) #ROSADO
centerMax = np.array([170,255,255])

while True:
    ret, frame = capture.read()
    if not ret:
        break
    frame = frame[115:600, 320:960]
    frame = cv2.flip(frame,0)
    frame = cv2.flip(frame,1)
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    maskDoor = cv2.inRange(frame_hsv, doorMin, doorMax)
    rateDoorPixels = cv2.countNonZero(maskDoor)/(frame.shape[0]*frame.shape[1])
    cv2.imshow('maskDoor', maskDoor)

    maskClient = cv2.inRange(frame_hsv, clientMin, clientMax)
    rateClientPixels = cv2.countNonZero(maskClient)/(frame.shape[0]*frame.shape[1])
    cv2.imshow('maskClient', maskClient)

    maskCenter = cv2.inRange(frame_hsv, centerMin, centerMax)
    rateCenterPixels = cv2.countNonZero(maskCenter)/(frame.shape[0]*frame.shape[1])
    cv2.imshow('maskCenter', maskCenter)

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
