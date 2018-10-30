import numpy as np
import socket
import fcntl, os
import select
import time
from threading import Thread

HOST = ''
PORT = 0
s = []
conn = []

TIME_LOOK_AROUND = 4.0
STEP_LOOK_AROUND = 0.05

look_positions = []

signals = []
recThread = []

COMMANDLENGTH = 8
TURN_VEL = 30

recFlag = False

ball_colors = {  'BLUE': {'colorL':240, 'colorH':0, 'hsvTol':20, 'minSat':27, 'minVal':27}, \
            'YELLOW': {'colorL':60, 'colorH':0, 'hsvTol':10, 'minSat':15, 'minVal':45}, \
            'PINK': {'colorL':54, 'colorH':1, 'hsvTol':30, 'minSat':23, 'minVal':23}, \
            'RED': {'colorL':0, 'colorH':0, 'hsvTol':15, 'minSat':15, 'minVal':45}, \
            'GREEN': {'colorL':100, 'colorH':0, 'hsvTol':20, 'minSat':23, 'minVal':23},}

# ball_colors = {  'BLUE': {'colorL':240, 'colorH':0, 'hsvTol':10, 'minSat':30, 'minVal':45}, \
#             'YELLOW': {'colorL':60, 'colorH':0, 'hsvTol':10, 'minSat':15, 'minVal':45}, \
#             'PINK': {'colorL':54, 'colorH':1, 'hsvTol':30, 'minSat':30, 'minVal':30}, \
#             'RED': {'colorL':0, 'colorH':0, 'hsvTol':15, 'minSat':15, 'minVal':45}, \
#             'GREEN': {'colorL':100, 'colorH':0, 'hsvTol':20, 'minSat':60, 'minVal':60},}

actions = { 'STAND':1, 'TO_WALK':9, 'SIT_DOWN':15, 'SPEAK06':6, \
            'SPEAK41':41, 'SPEAK42':42, 'SPEAK43':43, 'SPEAK44':44, 'SPEAK45':45}

led_colors = {'RED':[255,0,0], 'GREEN':[0,255,0],'BLUE':[0,0,255]}

gui_led_func = []

def recPacket():
    global conn, recFlag
    while(recFlag):
        com = conn.recv(COMMANDLENGTH)
        if(com == b"0OT_____"):
            signals['onTarget'] = True
        if(com == b"3FINISH_"):
            signals['dwFinished'] = True

def init(_port):
    global PORT, s, conn, recThread, recFlag
    PORT = _port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Waiting for connection...')
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)
    recFlag = True
    recThread = Thread(target = recPacket, args = ())
    recThread.start()
    print('Connected by', addr)

def close():
    global recFlag
    recFlag = False
    conn.send(bytearray([10, 0, 0, 0, 0, 0, 0, 0]))
    conn.close()

def goto(color):
    conn.send(  bytearray([0, color['colorL'], color['colorH'], color['hsvTol'], \
                color['minSat'], color['minVal'], 0, 0]))

def turn_left():
    global TURN_VEL
    conn.send(bytearray([2, 0, 100+TURN_VEL, 0, 0, 0, 0, 0])) # Girar Izquierda

def turn_right():
    global TURN_VEL
    conn.send(bytearray([2, 0, 100-TURN_VEL, 0, 0, 0, 0, 0])) # Girar Derecha

def stop_walking(pos):
    conn.send(bytearray([3, pos, 0, 0, 0, 0, 0, 0]))

def stop_action(pos):
    conn.send(bytearray([6, pos, 0, 0, 0, 0, 0, 0]))

def set_action(pos):
    conn.send(bytearray([5, pos, 0, 0, 0, 0, 0, 0]))

def set_head_angle(x, y):
    conn.send(bytearray([1, 0 if (x>0.0) else 1, int(abs(x)), \
                            1 if (y>0.0) else 0, int(abs(y)), 0, 0, 0]))

def set_led_head(color):
    # gui_led_func(color)
    conn.send(bytearray([4, color[0], color[1], color[2], 0, 0, 0, 0]))

def set_led_eyes(color):
    conn.send(bytearray([7, color[0], color[1], color[2], 0, 0, 0, 0]))

def look_around_loop():
    for pos in look_positions:
        set_head_angle(30*pos, 90)
        time.sleep(STEP_LOOK_AROUND)

lookThread = Thread(target = look_around_loop, args = ())

def look_around(dir):
    global look_positions, lookThread
    steps = TIME_LOOK_AROUND / STEP_LOOK_AROUND
    look_positions = np.sin(np.linspace(0, 2*np.pi, steps))
    lookThread = Thread(target = look_around_loop, args = ())
    lookThread.start()

def look_around_done():
    return not lookThread.isAlive()

if __name__ == '__main__':
    init(20073)
    while 1:
        x = input('input: ')

        if(x=='A1'):
            set_action(actions['SPEAK44'])

        if(x=='A2'):
            set_action(actions['SPEAK06'])

        if(x=='S1'):
            stop_action(actions['STAND'])

        if(x=='S2'):
            stop_action(actions['SIT_DOWN'])

        if(x=='C'):
            close()
            time.sleep(2)
            break
