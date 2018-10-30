import cv2
from darkflow.net.build import TFNet
import numpy as np
import time

options = {
    'model': 'cfg/yolov2_22.cfg',
    'load': 'bin/yolov2_22.weights',
    'threshold': 0.70,
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

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
capture.set(cv2.CAP_PROP_FPS, 10)

while True:
    stime = time.time()
    ret, frame = capture.read()
    frame = frame[115:600, 320:960]
    frame = cv2.flip(frame,0)
    frame = cv2.flip(frame,1)

    if ret:
        results = tfnet.return_predict(frame)
        rateMax = 0.0
        person = []
        for obj in results:
            if obj['label']=='person':
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
        if person!=[]:
            print(person)
            tl = (person['topleft']['x'], person['topleft']['y'])
            br = (person['bottomright']['x'], person['bottomright']['y'])
            label = 'person'
            confidence = person['confidence']
            text = '{}: {:.0f}%'.format(label, confidence * 100)
            frame = cv2.rectangle(frame, tl, br, [255, 0, 0], 5)
            frame = cv2.putText(
            frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        else:
            print('no person')



    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

conn.send(bytearray([10, 0, 0, 0, 0, 0, 0, 0]))
conn.close()

capture.release()
cv2.destroyAllWindows()
