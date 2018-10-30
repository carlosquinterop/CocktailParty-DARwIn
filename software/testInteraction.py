import cv2
import numpy as np
import time
import sys

sys.path.insert(0,'./oralInteraction')
sys.path.insert(0,'./recognition')

CAMERA_INDEX = 0

import oralInterface as oi
import recognition as rg

signals = { 'time_delay':0, 'door':False, 'dwFinished':False, 'onTarget':False, \
            'client_on_camera':False, 'dwLookFinished':False, 'speaking':False, \
            'person_on_camera':False, 'center_on_camera':False, 'newPerson':False}

capture = cv2.VideoCapture(CAMERA_INDEX)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
capture.set(cv2.CAP_PROP_FPS, 10)

rg.capture = capture
oi.signals = signals

while(True):
    input('Waiting for client:')

    oi.launchAskPresentation()
    rg.launch_add_person()
    while(signals['speaking']):
        pass

    oi.launchRequestDrink()
    while(signals['speaking']):
        pass

    oi.launchRequestNewPerson()
    while rg.check_thread():
        pass
    rg.people_ids[rg.azure_id] = oi.clients[-1].darNombre()
    oi.clients[-1].assignAttributes(rg.C.get_person_attribute(str(rg.azure_id)))
    rg.azure_id += 1

    while(signals['speaking']):
        pass

    if not signals['newPerson']:
        break

input('Waiting for current clients stands up:')
