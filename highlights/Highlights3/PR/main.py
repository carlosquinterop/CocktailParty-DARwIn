#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import time
import threading
import characterization as face_detection
from edit_files import Group


C = face_detection.Characterization()
cap = cv2.VideoCapture(0)
person_id = 209 #incrementar en maquina de estado

class thread_recognition(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print("Añadir nueva persona")
        add_suc = False
        while not add_suc:
            try:
                res = C.add_person(str(person_id), cap)                
                if(len(C.get_person_attribute(str(person_id)))!=0):
                    add_suc = True                                                
            except:
                print('error adding person')
            

        


#en maquina de estado
print("\nAnadir persona")
thread1 = thread_recognition(1, "face recognition")
thread1.start()
thread1.join()


# print("\nObtener atributos por person_id")
# print(C.get_person_attribute(str(person_id)))

# print("\nIdentificar persona")
# ant = time.time()
# print(C.identify_person(cap))
# print("Tiempo: " + str(time.time()-ant))

print ("Exiting Main Thread")