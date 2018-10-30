import cv2
import numpy as np
import time
import sys
import darwin_tcp.darwin as dw
import color_detection.color_detection as cd
from PyQt5 import QtGui, QtCore
from threading import Thread

sys.path.insert(0,'./oralInteraction')
sys.path.insert(0,'./recognition')
sys.path.insert(0,'./gui')

import oralInterface as oi
import recognition as rg
import dw_gui as gui

### DEFINES ###
# General
INIT_TIME = 7.0
# Capture
CAMERA_INDEX = 2
# Color Detection
SHOW_COLOR_DETECTIONS = False

# states = {  'reset':0, 'at_door':1, 'look_around1':2, 'door2center':3, \
#             'look_around2':4, 'turn_left1':5, 'dw_stop1':6, 'center2client':7, \
#             'ask4request':8, 'wait4person':9, 'ask4presentation':10, \
#             'requestDrink':11,'requestNewPerson':12, 'waitChangePerson':13,\
#             'turn_right1':14, 'dw_stop2':15, 'client2center':16, 'center2bar':17,
#             'wait4barman':18, 'listingRequest':19, 'dummy':20}

states = {  'reset':0, 'at_door':0, 'look_around1':0, 'door2center':0, \
            'look_around2':0, 'turn_left1':0, 'dw_stop1':0, 'center2client':0, \
            'ask4request':0, 'wait4person':0, 'ask4presentation':0, \
            'requestDrink':0,'requestNewPerson':0, 'waitChangePerson':0,\
            'turn_right1':0, 'dw_stop2':0, 'client2center':0, 'center2bar':0,
            'wait4barman':0, 'listingRequest':0, 'turn_left2':0, 'dw_stop3':0, \
            'bar2center':0, 'center2client2':0, 'requestClients':0, 'wait4person2':0, \
            'recognition':0, 'informOrderState':0, 'waitChangePerson2':0, \
            'turn_right2':0, 'dw_stop4':0, 'client2bar2':0, 'wait4barman2':0, \
            'informNewChoice':0, 'turn_left3':0, 'dw_stop5':0, 'bar2client2':0, \
            'ask4client2':0, 'wait4person3':0, 'informReadyChoice':0, 'END':0, 'dummy':0}

for i, key in enumerate(list(states.keys())):
    states[key]=i

signals = { 'time_delay':0, 'door':False, 'dwFinished':False, 'onTarget':False, \
            'client_on_camera':False, 'dwLookFinished':False, 'speaking':False, \
            'person_on_camera':False, 'center_on_camera':False, 'newPerson':False}

signals2 = { 'time_delay':0, 'door':False, 'dwFinished':False, 'onTarget':False, \
            'client_on_camera':False, 'dwLookFinished':False, 'speaking':False, \
            'person_on_camera':False, 'center_on_camera':False, 'newPerson':False}

outputs = { 'yolo_enable': False }

state = states['reset']
prevState = -1

dw.signals = signals
oi.signals = signals

app = []
widget = []

# def init_gui():
#     global app, widget
#     app = gui.QApplication(sys.argv)
#     widget = gui.App(states, signals)
#     # app.exec_()
#
# guiThread = Thread(target = init_gui, args = ())
# guiThread.start()

dw.init(20087)

# dw.gui_led_func = widget.updateDarwinPhoto
# oi.OralInteraction.setGuiChatFunction(widget.add_chat_item)

import person_detection as pd

capture = cv2.VideoCapture(CAMERA_INDEX)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
capture.set(cv2.CAP_PROP_FPS, 10)

rg.capture = capture
oi.capture = capture

clientCounter = 0

signals['time_delay'] = time.time()
while True:
    ret, frame = capture.read()
    if not ret:
        break
    frame = frame[115:600, 320:960]
    frame = cv2.flip(frame,0)
    frame = cv2.flip(frame,1)
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    ### SIGNALS GENERATION ###
    signals['door'] = cd.detect_door(frame_hsv, SHOW_COLOR_DETECTIONS)
    signals['client_on_camera'] = cd.detect_client(frame_hsv, SHOW_COLOR_DETECTIONS)
    signals['center_on_camera'] = cd.detect_center(frame_hsv, SHOW_COLOR_DETECTIONS)
    signals['dwLookFinished'] = dw.look_around_done()
    oi.checkThreads()
    if outputs['yolo_enable']:
        signals['person_on_camera'] = pd.detect_person(frame)
    else:
        signals['person_on_camera'] = False

    ### FSM ###
    # widget.state = state
    if prevState != state:
        print('--- STATE = ' + list(states.keys())[state] + '---')
    prevState = state
    # print("signals['client_on_camera'] = ", signals['client_on_camera'])

    # if state==states['reset']:
    #     dw.stop_action(dw.actions['STAND']) #SIT_DOWN
    #     dw.set_head_angle(0, 90); #AJUSTAR
    #     state = states['at_door']
    # if state==states['at_door']:
    #     state = states['at_door']

    if state==states['reset']:
        if (time.time()-signals['time_delay']) < INIT_TIME:
            state = states['reset']
        else:
            ##ORIGINAL
            dw.set_led_head(dw.led_colors['BLUE'])
            dw.stop_action(dw.actions['STAND']) #SIT_DOWN
            dw.set_head_angle(0, 90); #AJUSTAR
            state = states['at_door']

    elif state==states['at_door']:
        if signals['door']:
            state = states['at_door']
        else:
            ### 16 ###
            # dw.set_led_head(dw.led_colors['GREEN'])
            # dw.set_action(dw.actions['SPEAK44'])
            # oi.launchGreet()
            # state = states['ask4request']
            ## ORIGINAL
            ### 4 ###
            signals['dwLookFinished'] = False
            dw.look_around('RIGTH')
            state = states['look_around1']

    elif state==states['look_around1']:
        if not signals['dwLookFinished']:
            state = states['look_around1']
        else:
            ### 6 ###
            signals['onTarget'] = False
            dw.goto(dw.ball_colors['PINK'])
            state = states['door2center']

    elif state==states['door2center']:
        if not signals['onTarget']:
            state = states['door2center']
        else:
            ### 8 ###
            signals['dwLookFinished'] = False
            dw.look_around('LEFT')
            state = states['look_around2']

    elif state==states['look_around2']:
        if not signals['dwLookFinished']:
            state = states['look_around2']
        else:
            ### 10 ###
            dw.turn_left()
            state = states['turn_left1']

    elif state==states['turn_left1']:
        if not signals['client_on_camera']:
            state = states['turn_left1']
        else:
            ### 12 ###
            signals['dwFinished'] = False
            dw.stop_walking(dw.actions['STAND'])
            state = states['dw_stop1']

    elif state==states['dw_stop1']:
        if not signals['dwFinished']:
            state = states['dw_stop1']
        else:
            ### 14 ###
            signals['onTarget'] = False
            dw.goto(dw.ball_colors['GREEN'])
            state = states['center2client']
            #state = states['dummy']

    elif state==states['center2client']:
        if not signals['onTarget']:
            state = states['center2client']
        else:
            ### 16 ###
            dw.set_led_head(dw.led_colors['GREEN'])
            dw.set_action(dw.actions['SPEAK44'])
            oi.launchGreet()
            state = states['ask4request']

    elif state==states['ask4request']:
        if signals['speaking']:
            state = states['ask4request']
        else:
            ### 18 ###
            dw.set_led_head(dw.led_colors['BLUE'])
            dw.stop_action(dw.actions['STAND']) #SIT_DOWN
            dw.set_head_angle(0, 110); #AJUSTAR
            pd.clear_buffer()
            outputs['yolo_enable'] = True
            signals['person_on_camera'] = False
            state = states['wait4person']

    elif state==states['wait4person']:
        if not signals['person_on_camera']:
            state = states['wait4person']
        else:
            ### 20 ###
            # outputs['yolo_enable'] = False
            # dw.set_head_angle(0, 0)
            # dw.turn_right()
            # state = states['turn_right1']
            # ORIGINAL
            dw.set_led_head(dw.led_colors['GREEN'])
            oi.launchAskPresentation()
            rg.launch_add_person()
            state = states['ask4presentation']

    elif state==states['ask4presentation']:
        if signals['speaking']:
            state = states['ask4presentation']
        else:
            oi.launchRequestDrink()
            state = states['requestDrink']

    elif state==states['requestDrink']:
        if signals['speaking']:
            state = states['requestDrink']
        else:
            oi.launchRequestNewPerson()
            while rg.check_thread():
                pass
            rg.people_ids[rg.azure_id] = oi.clients[-1].darNombre()
            oi.clients[-1].assignAttributes(rg.C.get_person_attribute(str(rg.azure_id)))
            rg.azure_id += 1
            # widget.update_clients(oi.clients)
            state = states['requestNewPerson']

    elif state==states['requestNewPerson']:
        if signals['speaking']:
            state = states['requestNewPerson']
        else:
            dw.set_led_head(dw.led_colors['BLUE'])
            if signals['newPerson']:
                pd.fill_buffer()
                state = states['waitChangePerson']
            else:
                ##34
                # dw.set_led_head(dw.led_colors['GREEN'])
                # outputs['yolo_enable'] = True
                # print()
                # print()
                # print('-----------------------------')
                # print('-----------------------------')
                # print(rg.C.persons.azureService.get_all_names())
                # print('-----------------------------')
                # print('-----------------------------')
                # print()
                # print()
                # clientCounter = len(oi.clients)
                # state = states['wait4barman']
                ## 28
                # ORIGINAL
                clientCounter = len(oi.clients)
                outputs['yolo_enable'] = False
                dw.set_head_angle(0, 0)
                dw.turn_right()
                state = states['turn_right1']

    elif state==states['waitChangePerson']:
        if signals['person_on_camera']:
            state = states['waitChangePerson']
        else:
            ##
            time.sleep(4.0)
            pd.clear_buffer()
            state = states['wait4person']

    elif state==states['turn_right1']:
        if not signals['center_on_camera']:
            state = states['turn_right1']
        else:
            ### 12 ###
            signals['dwFinished'] = False
            dw.stop_walking(dw.actions['STAND'])
            state = states['dw_stop2']

    elif state==states['dw_stop2']:
        if not signals['dwFinished']:
            state = states['dw_stop2']
        else:
            ### 14 ###
            signals['onTarget'] = False
            dw.goto(dw.ball_colors['BLUE'])
            dw.set_head_angle(0, 80) #AJUSTAR
            state = states['center2bar']

    elif state==states['client2center']:
        if not signals['onTarget']:
            state = states['client2center']
        else:
            ### 16 ###
            signals['onTarget'] = False
            dw.goto(dw.ball_colors['BLUE'])
            state = states['center2bar']

    elif state==states['center2bar']:
        if not signals['onTarget']:
            state = states['center2bar']
        else:
            ### 16 ###
            dw.set_led_head(dw.led_colors['GREEN'])
            outputs['yolo_enable'] = True
            # dw.set_action(dw.actions['SPEAK44'])
            state = states['wait4barman']

    elif state==states['wait4barman']:
        if not signals['person_on_camera']:
            state = states['wait4barman']
        else:
            ### 32 ###
            # dw.turn_left()
            # outputs['yolo_enable'] = False
            # state = states['turn_left2']
            # ORIGINAL
            dw.set_led_head(dw.led_colors['GREEN'])
            dw.stop_action(dw.actions['SIT_DOWN'])
            dw.set_head_angle(0, 10)
            oi.launchListingRequest()
            state = states['listingRequest']

    elif state==states['listingRequest']:
        if signals['speaking']:
            state = states['listingRequest']
        else:
            ##44
            # oi.launchRequestClients()
            # state = states['requestClients']
            ## ORIGINAL
            ##38
            dw.turn_left()
            state = states['turn_left2']

    elif state==states['turn_left2']:
        if not signals['center_on_camera']:
            state = states['turn_left2']
        else:
            ### 35 ###
            signals['dwFinished'] = False
            dw.stop_walking(dw.actions['STAND'])
            state = states['dw_stop3']

    elif state==states['dw_stop3']:
        if not signals['dwFinished']:
            state = states['dw_stop3']
        else:
            ### 36 ###
            signals['onTarget'] = False
            dw.goto(dw.ball_colors['GREEN'])
            state = states['center2client2']

    elif state==states['bar2center']:
        if not signals['onTarget']:
            state = states['bar2center']
        else:
            ### 38 ###
            signals['onTarget'] = False
            dw.goto(dw.ball_colors['GREEN'])
            state = states['center2client2']

    elif state==states['center2client2']:
        if not signals['onTarget']:
            state = states['center2client2']
        else:
            ### 40 ###
            dw.set_action(dw.actions['SPEAK44'])
            oi.launchRequestClients()
            state = states['requestClients']

    elif state==states['requestClients']:
        if signals['speaking']:
            state = states['requestClients']
        else:
            ### 46 ###
            #input('Press ENTER ...')
            dw.set_led_head(dw.led_colors['BLUE'])
            dw.stop_action(dw.actions['STAND']) #SIT_DOWN
            dw.set_head_angle(0, 110); #AJUSTAR
            pd.clear_buffer()
            outputs['yolo_enable'] = True
            signals['person_on_camera'] = False
            state = states['wait4person2']

    elif state==states['wait4person2']:
        if not signals['person_on_camera']:
            state = states['wait4person2']
        else:
            ### 48 ###
            # ORIGINAL
            dw.set_led_head(dw.led_colors['GREEN'])
            rg.launch_identify_person()
            state = states['recognition']

    elif state==states['recognition']:
        if rg.check_thread():
            state = states['recognition']
        else:
            if rg.Recognized_id == 'desconocido':
                dw.set_led_head(dw.led_colors['GREEN'])
                rg.launch_identify_person()
                state = states['recognition']
            else:
                rg.clients = oi.clients
                oi.Recognized_name = rg.people_ids[int(rg.Recognized_id)]
                oi.launch_informOrderState()
                state = states['informOrderState']

    elif state==states['informOrderState']:
        if signals['speaking']:
            state = states['informOrderState']
        else:
            #input('Press ENTER ...')
            clientCounter -= 1
            if clientCounter > 0:
                pd.fill_buffer()
                oi.OralInteraction.say_something('¿Podría pasar el siguiente cliente?')
                dw.set_led_head(dw.led_colors['BLUE'])
                state = states['waitChangePerson2']
            else:
                ### 66 ###
                # pd.clear_buffer()
                # dw.set_led_head(dw.led_colors['GREEN'])
                # outputs['yolo_enable'] = True
                # signals['person_on_camera'] = False
                # state = states['wait4barman2']
                ### 52 ###
                # ORIGINAL
                outputs['yolo_enable'] = False
                dw.set_head_angle(0, 0)
                dw.turn_right()
                # widget.update_clients(oi.clients)
                # dw.goto(dw.ball_colors['BLUE'])
                state = states['turn_right2']

    elif state==states['waitChangePerson2']:
        if signals['person_on_camera']:
            state = states['waitChangePerson2']
        else:
            time.sleep(4.0)
            pd.clear_buffer()
            state = states['wait4person2']

    elif state==states['turn_right2']:
        if not signals['center_on_camera']:
            state = states['turn_right2']
        else:
            ### 54 ###
            signals['dwFinished'] = False
            dw.stop_walking(dw.actions['STAND'])
            state = states['dw_stop4']

    elif state==states['dw_stop4']:
        if not signals['dwFinished']:
            state = states['dw_stop4']
        else:
            ### 58 ###
            signals['onTarget'] = False
            dw.set_head_angle(0, 80) #AJUSTAR
            dw.goto(dw.ball_colors['BLUE'])
            state = states['client2bar2']

    elif state==states['client2bar2']:
        if not signals['onTarget']:
            state = states['client2bar2']
        else:
            ### 60 ###
            dw.set_led_head(dw.led_colors['BLUE'])
            outputs['yolo_enable'] = True
            # dw.set_action(dw.actions['SPEAK44'])
            state = states['wait4barman2']

    elif state==states['wait4barman2']:
        if not signals['person_on_camera']:
            state = states['wait4barman2']
        else:
            ### 62 ###
            dw.set_led_head(dw.led_colors['GREEN'])
            dw.stop_action(dw.actions['SIT_DOWN'])
            dw.set_head_angle(0, 10)
            oi.launch_informNewChoice()
            state = states['informNewChoice']

    elif state==states['informNewChoice']:
        if signals['speaking']:
            state = states['informNewChoice']
        else:
            ### 70 ###
            #input('Press ENTER ...')
            # oi.launch_askForMissingClient()
            # state = states['ask4client2']
            # ORIGINAL
            ### 64 ###
            dw.turn_left()
            state = states['turn_left3']

    elif state==states['turn_left3']:
        if not signals['center_on_camera']:
            state = states['turn_left3']
        else:
            ### 66 ###
            signals['dwFinished'] = False
            dw.stop_walking(dw.actions['STAND'])
            state = states['dw_stop5']

    elif state==states['dw_stop5']:
        if not signals['dwFinished']:
            state = states['dw_stop5']
        else:
            ### 68 ###
            signals['onTarget'] = False
            dw.goto(dw.ball_colors['GREEN'])
            state = states['bar2client2']

    elif state==states['bar2client2']:
        if not signals['onTarget']:
            state = states['bar2client2']
        else:
            ### 70 ###
            dw.set_led_head(dw.led_colors['GREEN'])
            dw.set_action(dw.actions['SPEAK44'])
            oi.launch_askForMissingClient()
            state = states['ask4client2']

    elif state==states['ask4client2']:
        if signals['speaking']:
            state = states['ask4client2']
        else:
            ### 72 ###
            #input('Press ENTER ...')
            dw.set_led_head(dw.led_colors['BLUE'])
            dw.stop_action(dw.actions['STAND'])
            dw.set_head_angle(0, 110); #AJUSTAR
            pd.clear_buffer()
            outputs['yolo_enable'] = True
            signals['person_on_camera'] = False
            state = states['wait4person3']

    elif state==states['wait4person3']:
        if not signals['person_on_camera']:
            state = states['wait4person3']
        else:
            ### 72 ###
            oi.launch_informReadyChoice()
            state = states['informReadyChoice']

    elif state==states['informReadyChoice']:
        if signals['speaking']:
            state = states['informReadyChoice']
        else:
            ### 74 ###
            #input('Press ENTER ...')
            state = states['END']

    elif state==states['END']:
        state = states['END']

    elif state==states['dummy']:
        state = states['dummy']

    # if states['door2center']==state or states['center2client']==state or \
    #     states['center2bar']==state or states['center2client']==state or \
    #     states['client2bar2']==state or states['bar2client2']==state:
    #     black = np.zeros(frame.shape)
    #     img = QtGui.QImage(black, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
    #     pix = QtGui.QPixmap.fromImage(img)
    #     widget.graph.setPixmap(pix)
    # else:
    #     frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #     img = QtGui.QImage(frame2, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
    #     pix = QtGui.QPixmap.fromImage(img)
    #     pix = pix.scaled(593,450)
    #     widget.graph.setPixmap(pix)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

dw.close()

capture.release()
cv2.destroyAllWindows()
