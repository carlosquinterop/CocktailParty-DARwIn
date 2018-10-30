from PyQt5.QtCore import QThread
from espeak import espeak
import time

class T2SThread(QThread):

    def __init__(self):
        super(T2SThread, self).__init__()
        self.speak = espeak.ESpeak()
        self.speak.voice = 'es-la'
        self.speak.speed = 190
        self.speak.pitch = 75
        self.speak.amplitude = 80
        self.running = False
        self.onSpeak = False
        self.text = ""
        self.delay = 0

    def run(self):
        self.running = True
        while self.running:
            time.sleep(0.01)
            if self.onSpeak:
                self.speak.say(self.text)
                self.onSpeak = False

    def stop(self):
        self.running = False

    def say_something(self, text, delay = 0):
        self.text = text
        self.delay = delay
        self.onSpeak = True

    def get_on_speak(self):
        return self.onSpeak