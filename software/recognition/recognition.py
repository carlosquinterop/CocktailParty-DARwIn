import characterization as face_detection
from threading import Thread
import time

C = face_detection.Characterization()
C.delete_all_person()
azure_id = 1000
azure_res = -1
azure_thread = []
people_ids = {}
azureThread = []
capture = []
Recognized_id = []

def add_person():
    global C, azure_id, capture, azure_res
    print("--- Añadir nueva persona--- ")
    time.sleep(2)
    add_suc = False
    while not add_suc:
        try:
            res = C.add_person(str(azure_id), capture)
            if(len(C.get_person_attribute(str(azure_id)))!=0):
                add_suc = True
        except:
            print('error adding person')

def launch_add_person():
    global azureThread
    azureThread = Thread(target = add_person, args = ())
    azureThread.start()

def identify_person():
    global C, capture, Recognized_id
    print("--- Identify Person--- ")
    Recognized_id = C.identify_person(capture)


def launch_identify_person():
    global azureThread
    azureThread = Thread(target = identify_person, args = ())
    azureThread.start()

def check_thread():
    global azureThread
    try:
        return azureThread.isAlive()
    except:
        return False
