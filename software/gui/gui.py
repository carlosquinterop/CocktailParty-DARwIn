from dw_gui import *
from threading import Thread
import cv2
from PyQt5 import QtGui, QtCore

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

app = []
widget = []

def init_gui():
    global app, widget
    app = QApplication(sys.argv)
    widget = App(states, signals)
    app.exec_()

guiThread = Thread(target = init_gui, args = ())
guiThread.start()

while True:
    pass

#
# # guiThread = Thread(target = app.exec_, args = ())
# # guiThread.start()
#
# capture = cv2.VideoCapture(0)
# capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# capture.set(cv2.CAP_PROP_FPS, 10)
#
# def updateCamera():
#     while True:
#         ret, frame = capture.read()
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         frame = frame[115:600, 320:960]
#         frame = cv2.flip(frame,0)
#         frame = cv2.flip(frame,1)
#         img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
#         pix = QtGui.QPixmap.fromImage(img)
#         widget.graph.setPixmap(pix)
#         # cv2.waitKey(1)
#
# cameraThread = Thread(target = updateCamera, args = ())
# # cameraThread.start()
#
# sys.path.insert(0,'../oralInteraction')
# from Cliente import Cliente
#
# clients = [		Cliente("Bryan","café","no esta listo"), \
# 				Cliente("Lyna","vino","no esta listo"), \
# 				Cliente("Fabián","una gaseosa","no esta listo")]
#
# dictionary = {'age':21,'gender':"female", 'smile':0, 'beard':0.2, \
# 		'glasses':"glasses", 'bald' : 0.2, 'hairColor' : "brown", \
# 		'eyeMakeUp':True, 'lipMakeUp':True,'headWear':0.9, 'mustache':0.1}
# for i in range(len(clients)):
#  	clients[i].assignAttributes(dictionary)
#
# widget.update_clients(clients)
#
# while True:
#     pass
#
# # sys.exit(app.exec_())
