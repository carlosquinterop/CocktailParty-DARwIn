import cv2
import numpy as np

def detect_door(frame, show):
    maskDoor = cv2.inRange(frame, np.array([110,40,40]), np.array([130,255,255])) #AZUL
    rateDoorPixels = cv2.countNonZero(maskDoor)/(frame.shape[0]*frame.shape[1])
    if show:
        cv2.imshow('maskDoor', maskDoor)
    return rateDoorPixels > 0.3

def detect_client(frame, show):
    #maskClient = cv2.inRange(frame, np.array([40,60,60]), np.array([50,255,255])) #VERDE
    maskClient = cv2.inRange(frame, np.array([40,60,60]), np.array([60,255,255])) #VERDE
    rateClientPixels = cv2.countNonZero(maskClient)/(frame.shape[0]*frame.shape[1])
    if show:
        cv2.imshow('maskClient', maskClient)
    # print('rateClientPixels' + str(rateClientPixels))
    return rateClientPixels > 0.1 #0.04

def detect_center(frame, show):
    maskCenter = cv2.inRange(frame, np.array([140,30,30]), np.array([170,255,255])) #ROSADO
    rateCenterPixels = cv2.countNonZero(maskCenter)/(frame.shape[0]*frame.shape[1])
    if show:
        cv2.imshow('maskCenter', maskCenter)
    return rateCenterPixels > 0.04
