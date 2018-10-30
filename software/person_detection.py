import cv2
from darkflow.net.build import TFNet
import numpy as np

### DEFINES ###
MIN_WIDTH_PERSON = 0.35
SIZE_BUFFER_PERSON = 20
YOLO_TH_PERSON = 0.8

yolo_person_buffer = SIZE_BUFFER_PERSON*[False]
yolo_person_bcounter = 0

options = {
    'model': 'cfg/yolov2_22.cfg',
    'load': 'bin/yolov2_22.weights',
    'threshold': 0.40,
    'gpu': .5
}

'''
options = {
    'model': 'cfg/yolov3.cfg',
    'load': 'bin/yolov3.weights',
    'threshold': 0.45,
    'gpu': .5
}
'''

tfnet = TFNet(options)
colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]

yolo_person_buffer = SIZE_BUFFER_PERSON*[False]
yolo_person_bcounter = 0

def clear_buffer():
    global yolo_person_buffer
    yolo_person_buffer = SIZE_BUFFER_PERSON*[False]

def fill_buffer():
    global yolo_person_buffer
    yolo_person_buffer = SIZE_BUFFER_PERSON*[True]

def person_push(data):
    global yolo_person_buffer, yolo_person_bcounter
    yolo_person_buffer[yolo_person_bcounter] = data
    yolo_person_bcounter += 1
    if yolo_person_bcounter == SIZE_BUFFER_PERSON:
        yolo_person_bcounter = 0
    return 1.0*yolo_person_buffer.count(True)/SIZE_BUFFER_PERSON

def detect_person(frame):
    global tfnet, color
    results = tfnet.return_predict(frame)
    rateMax = 0.0
    person = []
    for obj in results:
        if obj['label']=='person' and (obj['bottomright']['x'] - obj['topleft']['x'])>(MIN_WIDTH_PERSON*frame.shape[1]):
            rate = 0.0
            # Confidence
            rate += 0.25*obj['confidence']
            # Center
            rate += 0.25*(1.0-abs(0.5*(frame.shape[1]-obj['topleft']['x']-obj['bottomright']['x']))/(frame.shape[1]/2.0))
            # Area
            rate += 0.50*(obj['bottomright']['x'] - obj['topleft']['x'])*(obj['bottomright']['y'] - obj['topleft']['y']) / (frame.shape[1]*frame.shape[0])
            if rate>rateMax:
                person = obj
                rateMax = rate
    rate = person_push(person!=[])
    if rate > YOLO_TH_PERSON and person!=[]:
        tl = (person['topleft']['x'], person['topleft']['y'])
        br = (person['bottomright']['x'], person['bottomright']['y'])
        label = 'person'
        confidence = person['confidence']
        text = '{}: {:.0f}%'.format(label, confidence * 100)
        frame = cv2.rectangle(frame, tl, br, [255, 0, 0], 5)
        frame = cv2.putText(
                frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        return True
    else:
        return False
