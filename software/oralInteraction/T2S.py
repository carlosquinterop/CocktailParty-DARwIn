from PyQt5 import uic, QtWidgets
from T2SThread import T2SThread
from PyQt5.QtWidgets import QApplication
from Cliente import Cliente
from gtts import gTTS
from Saludos import Saludos
from ListasEntendimiento import ListasEntendimiento
import speech_recognition as sr
import os 
import csv
import time
import os 
import sys
import random
import playsound

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.fn_init_ui()
        self.t2sThread = T2SThread()
        #self.t2sThread = T2S()
        self.t2sThread.start()
        self.saludos = Saludos()    

        #Declaración de Strings necesarios
        self.ListasEntendimiento = ListasEntendimiento()
        self.clientes = []
        self.listaNombres = self.ListasEntendimiento.darListaNombres()
        self.listaPedidos = self.ListasEntendimiento.darListaPedidos()
        self.listaAfirmaciones = self.ListasEntendimiento.darListaAfirmaciones()
        self.listaNegaciones = self.ListasEntendimiento.darListaNegaciones()
        self.listaBartender = self.ListasEntendimiento.darListaBartender()
        self.listaAlternativas = self.ListasEntendimiento.darListaAlternativas()
        self.totalClientes = 1
        self.alternativas = "agua o cerveza"
        self.alternativaReemplazo = ""
        self.clienteFaltante = Cliente("Juan José", "una gaseosa", "no esta listo")
        
    #Arranque
    def fn_init_ui(self):
        uic.loadUi("t2sUi.ui", self)
        self.btnSpeak.clicked.connect(self.prueba)

    def say_something(self,text):
    	grabacion = gTTS(text = text, lang = 'es')
    	grabacion.save('output.mp3')
    	playsound.playsound('output.mp3',True)

    def prueba(self):
    	self.say_something("Hola Hector, como estas?")
    	time.sleep(20)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())