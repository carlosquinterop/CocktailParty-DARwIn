#PLEASE CHECK IMPORTS FOR AVOIDING DUPLICATION
import sys
import random
#import pylab
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFrame, QLabel, QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QComboBox
from PyQt5.QtWidgets import QListWidgetItem, QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
#from PIL import Image

#######################################################################################

#CREATING WINDOW
class App(QWidget):

    def __init__(self, _states, _signals):
        super().__init__()
        self.states = _states
        self.signals = _signals
        self.old_signals = _signals
        self.gemma_color = [0, 0, 0]
        self.title = 'Darwin Party Monitor'
        self.left = 460
        self.top = 90
        self.width = 1900
        self.height = 1000
        self.initUI()

    attributes = [ \
    {'Name': '', 'Age':'', 'Gender':'', 'Glasses':'', \
        'Hair Color':'', 'Eye Makeup':'', 'Lip Makeup':'', \
        'Mustache':'', 'Beard':''}, \
    {'Name': '', 'Age':'', 'Gender':'', 'Glasses':'', \
        'Hair Color':'', 'Eye Makeup':'', 'Lip Makeup':'', \
        'Mustache':'', 'Beard':''}, \
    {'Name': '', 'Age':'', 'Gender':'', 'Glasses':'', \
        'Hair Color':'', 'Eye Makeup':'', 'Lip Makeup':'', \
        'Mustache':'', 'Beard':''} ]

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

#DICTIONARIES AND UPDATE

        # states = {  'reset':0, 'at_door':1, 'look_around1':2, 'door2center':3, \
        #     'look_around2':4, 'turn_left1':5, 'dw_stop1':6, 'center2client':7, \
        #     'ask4request':8, 'wait4person':9, 'ask4presentation':10, \
        #     'requestDrink':11,'requestNewPerson':12, 'waitChangePerson':13,\
        #     'turn_right1':14, 'dw_stop2':15, 'client2center':16, 'center2bar':17,
        #     'wait4barman':18, 'listingRequest':19, 'turn_left2':20, 'dw_stop3':21, \
        #     'bar2center':22, 'center2client2':23, 'requestClients':24, 'wait4person2':25, \
        #     'recognition':26, 'informOrderState':27, 'waitChangePerson2':28, \
        #     'turn_right2':29, 'dw_stop4':30, 'client2bar2':31, 'wait4barman2':32, \
        #     'informNewChoice':33, 'turn_left3':34, 'dw_stop5':35, 'bar2client2':36, \
        #     'ask4client2':37, 'wait4person3':38, 'informReadyChoice':39, 'END':40, 'dummy':41}

        # signals = { 'time_delay':0, 'door':False, 'dwFinished':False, 'onTarget':False, \
        #     'client_on_camera':False, 'dwLookFinished':False, 'speaking':False, \
        #     'person_on_camera':False, 'center_on_camera':False, 'newPerson':False}



        state = 0
#######################################


#########################################################################################
#CONFIG VARIABLES

        self.updateRate = 25

#######################################################################################
#FUNCTIONS DEFINITION


#DICTIONARIES
        def dictionariesLoad():

            # self.signals = signals
            self.originalStates = self.states

            self.signalsCurr = { 'time_delay':10, 'door':True, 'dwFinished':False, 'onTarget':False, \
            'client_on_camera':False, 'dwLookFinished':False, 'speak_ready':False, \
            'person_on_camera':False}

            self.signalsPrev = { 'time_delay':0, 'door':False, 'dwFinished':False, 'onTarget':True, \
            'client_on_camera':False, 'dwLookFinished':False, 'speak_ready':False, \
            'person_on_camera':False}

            self.signalsFoll = { 'time_delay':1, 'door':True, 'dwFinished':False, 'onTarget':False, \
            'client_on_camera':False, 'dwLookFinished':True, 'speak_ready':False, \
            'person_on_camera':True}

            self.state = state

            self.states = {val:key for (key, val) in self.originalStates.items()}

#UI
        def updateTimer():
            self.timer = QTimer()
            self.timer.timeout.connect(update)
            self.timer.start(self.updateRate)

        def update():
            # aux=self.signalsPrev
            # self.signalsPrev=self.signalsCurr
            # self.signalsCurr=self.signalsFoll
            # self.signalsFoll=aux
            #self.readSignals()

            # Update State
            strState = list(self.originalStates.keys())[list(self.originalStates.values()).index(self.state)]
            self.labelState.setText(strState)

            # Update Signals
            if self.signals != self.old_signals:
                self.table.insertRow(0)
                self.populateTableSignals(self.signals,0)
            self.old_signals = self.signals.copy()

            # self.updateDarwinPhoto([0,0,0])

        def tableSignalCreator():
            self.table = QTableWidget(5,4,self)
            self.table.setGeometry(0,0,75,75)
            self.table.setRowCount(1)
            self.table.setColumnCount(len(self.signals))
            self.model = QStandardItemModel(self)
            self.configTable(self.signals)
            self.populateTableSignals(self.signals,0)
            self.table.clicked.connect(self.cell_was_clicked)

        def tableOrderCreator():
            self.table2 = QTableWidget(5,4,self)
            self.table2.setGeometry(0,0,75,75)
            self.table2.setRowCount(len(self.attributes[0]))
            self.table2.setColumnCount(3)
            self.model2 = QStandardItemModel(self)
            self.configTable01()
            self.populateTableAttributes()
            #self.table2.clicked.connect(self.cell_was_clicked)

        def buttonCreator():
            self.button0 = QPushButton('Go to State', self)
            self.button0.clicked.connect(self.on_click)
            self.button1 = QPushButton('Ampliar grafo', self)
            self.button1.clicked.connect(self.on_click1)
            self.buttonSSS = QPushButton('Simulate signal change', self)
            self.buttonSSS.clicked.connect(self.on_clickSSS)

        def comboBoxCreator():
            self.comboBox = QComboBox(self)
            self.comboUpdate()
            self.comboDox = QComboBox(self)

        def comboDarwin():
            self.comboDarwin = QComboBox(self)

        def comboDarwinItems():
            self.comboDarwin.addItem("DarwinGemaO")
            self.comboDarwin.addItem("DarwinGemaRL")
            self.comboDarwin.addItem("DarwinGemaGL")
            self.comboDarwin.addItem("DarwinGemaBL")
            self.comboDarwin.addItem("DarwinGemaWL")

        def textInputCreator():
            self.textbox = QLineEdit(self)

        def mainLabel():
            self.labelStateT = QLabel()
            self.labelStateT.setText('Darwin\'s party current state: ')
            self.labelStateT.setStyleSheet('color: blue')
            self.labelState = QLabel()
            self.labelState.setStyleSheet('font: bold; font-size: 28px')
            self.labelState.setText(self.states.get(7))


        def ordersLabel():
            self.labelStateT2 = QLabel()
            self.labelStateT2.setText('Darwin\'s orders summary: ')
            self.labelStateT2.setStyleSheet('color: blue')
            self.labelState2 = QLabel()
            self.labelState2.setStyleSheet('font: bold; font-size: 28px')
            self.labelState2.setText("Darwin\'s orders and clients")

        def photoCreator():
            self.photo = QLabel(self)
            pixmap = QPixmap('DarwinGemaO.jpg')
            pixmap = pixmap.scaled(200,200)
            self.photo.setPixmap(pixmap)

        def graphFigureCreator():
            self.graph = QLabel(self)
            pixmapGraph = QPixmap('graph.png')
            pixmapGraph = pixmapGraph.scaled(593,450)
            self.graph.setPixmap(pixmapGraph)

        def graphCreator():
            A=np.matrix([
                # [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                # [1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                # [0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0],
                # [0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0],
                # [0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0],
                # [0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0],
                # [0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0],
                # [0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0],
                # [0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0],
                # [0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0],
                # [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1]
                [-1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  -1,  0,  0,  0,  0,  0,  0,  0],
                ])
            G = nx.DiGraph()
            statesArray = []
            for key,val in self.states.items():
                statesArray.append(val)
            for i in range(len(self.signals)):
                self.table.setColumnWidth(i, 100)
            a=list(self.signals.keys())
            signalsArray=[]
            for key in a:
                signalsArray.append(key)
            it=0
            for i in range(len(A)):
                for j in range(len(A)):
                    for k in range(len(A.transpose())):
                        if A[i,k] == -1 and A[j,k] == 1:
                            G.add_edge( statesArray[i], statesArray[j], weight=signalsArray[it])
                            if it<(len(signalsArray)-1):
                                it=it+1
            val_map = {'A': 1.0,'L': 0.0}
            values = [val_map.get(node, 0.25) for node in G.nodes()]
            red_edges = []
            edge_colours = ['black' if not edge in red_edges else 'red'
                        for edge in G.edges()]
            black_edges = [edge for edge in G.edges() if edge not in red_edges]
            pos = nx.shell_layout(G)
            nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_color = 'skyblue', node_size = 300)
            nx.draw_networkx_labels(G, pos)
            edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)])
            nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels, color='red')
            nx.draw_networkx_edges(G, pos, edgelist=black_edges, color='red', arrows=True)
            plt.axis('off')
            plt.savefig("graph.png")
            #print(G.edges(data=True))

        def layoutCreator():
#vbox is the main containter
            self.vbox = QVBoxLayout(self)
            self.vbox.addWidget(self.labelStateT)
            self.vbox.addWidget(self.labelState)
#hbox0 is an horizontal part including table and photo
            self.hbox0 = QHBoxLayout()
            self.hbox0.addWidget(self.table)
            self.hbox0.addWidget(self.photo)
            self.vbox.addLayout(self.hbox0)
#Labels for the second table are set
            self.vbox.addWidget(self.labelStateT2)
            self.vbox.addWidget(self.labelState2)
#Second table
            self.hbox1 = QHBoxLayout()
            self.hbox1.addWidget(self.table2)
            self.hbox1.addWidget(self.chat1)
            self.hbox1.addWidget(self.chat2)
            self.hbox1.addWidget(self.graph)
            self.vbox.addLayout(self.hbox1)
# #hbox1 is an horizontal part including 4 elements
#             self.hbox2 = QHBoxLayout()
#             # self.hbox2.addWidget(self.comboBox)
#             # self.hbox2.addWidget(self.button0)
#             # self.hbox2.addWidget(self.comboDox)
#             # self.hbox2.addWidget(self.button1)
#             self.vbox.addLayout(self.hbox2)
# #hbox2 is an horizontal part incluidng simulation elements
#             self.hbox3 = QHBoxLayout()
#             # self.hbox3.addWidget(self.buttonSSS)
#             # self.hbox3.addWidget(self.comboDarwin)
#             self.vbox.addLayout(self.hbox3)
# #Finishing and showing vbox container within all elements
#             self.hbox4= QHBoxLayout()
#             self.vbox.addLayout(self.hbox4)
            #self.vbox.addStretch()
            self.setLayout(self.vbox)
            self.show()

########################################################################################
#ONCE EXECUTION
        dictionariesLoad()
        updateTimer()
        tableSignalCreator()
        tableOrderCreator()
        photoCreator()
        graphCreator()
        graphFigureCreator()
        # buttonCreator()
        # comboBoxCreator()
        # comboDarwin()
        # comboDarwinItems()
        mainLabel()
        ordersLabel()
        self.chat1 = QListWidget(self)
        self.chat1.setWordWrap(True)
        self.chat2 = QListWidget(self)
        self.chat2.setWordWrap(True)
        layoutCreator()
        self.currentState(self.states)

        self.updateDarwinPhoto([0,0,0])

#############################################################################
#############################################################################
    @pyqtSlot()
    def on_click(self):
        self.labelUpdate()
        # aux=self.signalsPrev
        # self.signalsPrev=self.signalsCurr
        # self.signalsCurr=self.signalsFoll
        # self.signalsFoll=aux

    def on_click1(self):
        #self.graphCreator()
        plt.show()

    def on_clickSSS(self):
        self.readSignals()
        self.table.insertRow(0)

    def labelUpdate(self):
        self.originalStates.get(self.comboBox.currentText())
        self.labelState.setText(self.comboBox.currentText())

    def configTable(self,signals):
        for i in range(len(signals)):
            self.table.setColumnWidth(i, 100)
        a=list(signals.keys())
        headers=[]
        for key in a:
            headers.append(key)
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setVerticalHeaderLabels(["Previous State","Current State", "Next State"])


    def configTable01(self):
        for i in range(len(self.attributes[0])):
            self.table2.setColumnWidth(i, 100)
        a=list(self.attributes[0].keys())
        headers=[]
        for key in a:
            headers.append(key)
        # self.table2.setHorizontalHeaderLabels(headers)
        # self.table2.setVerticalHeaderLabels(["Client 1","Client 2", "Client 3"])
        self.table2.setVerticalHeaderLabels(headers)
        self.table2.setHorizontalHeaderLabels(["Client 1","Client 2", "Client 3"])

    def readSignals(self):
        self.signals = { 'time_delay':random.randint(1,21), 'door':bool(random.randint(0,1)), 'dwFinished':bool(random.randint(0,1)), 'onTarget':bool(random.randint(0,1)), \
            'client_on_camera':bool(random.randint(0,1)), 'dwLookFinished':bool(random.randint(0,1)), 'speak_ready':bool(random.randint(0,1)), \
            'person_on_camera':bool(random.randint(0,1))}

    def populateTableSignals(self,signals,value):
        keys = signals.items()
        a=list(signals.keys())
        if value == 0:
           h = 55
        else:
            h = 0
        values = keys
        for i in range(1):
            row = []
            for item in range(len(values)):
                cell = QStandardItem(str(item))
                row.append(cell)
                self.table.setItem(value, item, QTableWidgetItem())
                signal = signals.get(a[item])
                if signal == True and type(signal)==bool:
                    self.table.setItem(value, item, QTableWidgetItem("T"))
                    self.table.item(value,item).setBackground(QColor(0,200+h,0))
                    self.table.item(value,item).setTextAlignment(Qt.AlignHCenter)
                elif signal == False and type(signal)==bool:
                    self.table.setItem(value, item, QTableWidgetItem("F"))
                    self.table.item(value,item).setBackground(QColor(200+h,0,0))
                    self.table.item(value,item).setTextAlignment(Qt.AlignHCenter)
                else:
                    self.table.setItem(value,item, QTableWidgetItem(str(signal)))
                    self.table.item(value,item).setBackground(QColor(0,200+h,200+h))
                    self.table.item(value,item).setTextAlignment(Qt.AlignHCenter)


    def populateTableAttributes(self):
        keys = self.attributes[0].items()
        a=list(self.attributes[0].keys())
        values = keys
        for i in range(3):
            row = []
            for item in range(len(values)):
                cell = QStandardItem(str(item))
                row.append(cell)
                # self.table2.setItem(value, item, QTableWidgetItem())
                attribute =  self.attributes[i].get(a[item])
                self.table2.setItem(item,i, QTableWidgetItem(str(attribute)))


    def cell_was_clicked(self):
        self.row = self.table.currentItem().row()
        self.column = self.table.currentItem().column()
        print("Row %d and Column %d was clicked" % (self.row, self.column))
        item = self.table.itemAt(self.row, self.column)

    def currentState(self,states):
        self.state=int(self.state)

    def button_clicked(self):
        gotText = self.textbox.text()
        print(gotText)
        self.button0.setText(gotText);
        print("Hello darkdness my old friend")

    def comboUpdate(self):
        for key,val in self.states.items():
            self.comboBox.addItem(val + " : [" + str(self.originalStates.get(val)) + "]")

    def updateDarwinPhoto(self, color):
        print('--- LED CHANGED ---')
        if color == [0, 0, 0]:
            pixmap = QPixmap('DarwinGemaO.jpg')
        elif color == [255, 0, 0]:
            pixmap = QPixmap('DarwinGemaRL.jpg')
        elif color == [0, 255, 0]:
            pixmap = QPixmap('DarwinGemaGL.jpg')
        elif color == [0, 0, 255]:
            pixmap = QPixmap('DarwinGemaBL.jpg')
        else:
            pixmap = QPixmap('DarwinGemaWL.jpg')
        pixmap = pixmap.scaled(400,400)
        self.photo.setPixmap(pixmap)

    def add_chat_item(self, talker, text):
        if talker == 'Darwin':
            item = QListWidgetItem(talker + ': ' + text)
            item.setFont(QFont("Arial", 15))
            item.setForeground(QColor(255,0,0))
            item.setTextAlignment(Qt.AlignLeft)
            self.chat1.addItem(item)
            item = QListWidgetItem(talker + ': ' + text)
            item.setFont(QFont("Arial", 15))
            item.setForeground(QColor(255,255,255))
            item.setTextAlignment(Qt.AlignLeft)
            self.chat2.addItem(item)
        else:
            item = QListWidgetItem(talker + ': ' + text)
            item.setFont(QFont("Arial", 15))
            item.setForeground(QColor(0,0,255))
            item.setTextAlignment(Qt.AlignRight)
            self.chat2.addItem(item)
            item = QListWidgetItem(talker + ': ' + text)
            item.setFont(QFont("Arial", 15))
            item.setForeground(QColor(255,255,255))
            item.setTextAlignment(Qt.AlignRight)
            self.chat1.addItem(item)
        self.chat1.scrollToBottom()
        self.chat2.scrollToBottom()

    def update_clients(self, clients):
        self.attributes = [ \
            {'Name': '', 'Age':'', 'Gender':'', 'Glasses':'', \
                'Hair Color':'', 'Eye Makeup':'', 'Lip Makeup':'', \
                'Mustache':'', 'Beard':''}, \
            {'Name': '', 'Age':'', 'Gender':'', 'Glasses':'', \
                'Hair Color':'', 'Eye Makeup':'', 'Lip Makeup':'', \
                'Mustache':'', 'Beard':''}, \
            {'Name': '', 'Age':'', 'Gender':'', 'Glasses':'', \
                'Hair Color':'', 'Eye Makeup':'', 'Lip Makeup':'', \
                'Mustache':'', 'Beard':''} ]
        for i in range(len(clients)):
            self.attributes[i]['Name'] = str(clients[i].darNombre())
            self.attributes[i]['Age'] = str(clients[i].age)
            self.attributes[i]['Gender'] = str(clients[i].gender)
            self.attributes[i]['Glasses'] = str(clients[i].glasses)
            self.attributes[i]['Hair Color'] = str(clients[i].hairColor)
            self.attributes[i]['Eye Makeup'] = str(clients[i].eyeMakeUp)
            self.attributes[i]['Lip Makeup'] = str(clients[i].lipMakeUp)
            self.attributes[i]['Mustache'] = str(clients[i].mustache)
            self.attributes[i]['Beard'] = str(clients[i].beard)
        self.populateTableAttributes()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
