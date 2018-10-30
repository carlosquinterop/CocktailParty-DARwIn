from threading import Thread
from OralInteraction import OralInteraction
from Cliente import Cliente
from missingDrink import MissingDrink
import darwin_tcp.darwin as dw

OralInteraction = OralInteraction()
OralInteraction.setRedLedFunction(dw.set_led_head)
missingDrink = []
newClient = []
clientCount = 0
clients = []
capture = []
speakThread = []
signals = []
Recognized_name = []
alternatives = ''
newOrder = ''

def checkThreads():
    try:
        if speakThread.isAlive():
            signals['speaking'] = True
        else:
            signals['speaking'] = False
    except:
        signals['speaking'] = False

def launchGreet():
    global speakThread
    speakThread = Thread(target = OralInteraction.greet, args = ())
    speakThread.start()

def askPresentation():
    global newClient
    repeat = True
    while repeat:
        dw.set_led_head(dw.led_colors['GREEN'])
        OralInteraction.askForName()
        name = OralInteraction.listeningName(OralInteraction.captureAudio())
        while name == "":
            dw.set_led_head(dw.led_colors['GREEN'])
            OralInteraction.apologize()
            OralInteraction.askForName()
            name = OralInteraction.listeningName(OralInteraction.captureAudio())
        affirmate = True
        while affirmate:
            dw.set_led_head(dw.led_colors['GREEN'])
            OralInteraction.verifyName(name)
            affirmation = OralInteraction.affirmationCheck(OralInteraction.captureAudio())
            if affirmation == 0:
                affirmate = False
            if affirmation == 1:
                affirmate = False
                repeat = False
    newClient = Cliente(name,"","no esta listo")

def launchAskPresentation():
    global speakThread
    speakThread = Thread(target = askPresentation, args = ())
    speakThread.start()

def requestDrink():
    global newClient, clientCount, clients
    repeat = True
    while repeat:
        dw.set_led_head(dw.led_colors['GREEN'])
        OralInteraction.askForDrink()
        drink = OralInteraction.listeningDrink(OralInteraction.captureAudio())
        while drink == "":
            dw.set_led_head(dw.led_colors['GREEN'])
            OralInteraction.apologize()
            OralInteraction.askForDrink()
            drink = OralInteraction.listeningDrink(OralInteraction.captureAudio())
        affirmate = True
        while affirmate:
            dw.set_led_head(dw.led_colors['GREEN'])
            OralInteraction.verifyDrink(drink)
            affirmation = OralInteraction.affirmationCheck(OralInteraction.captureAudio())
            print('---- La Afirmacion es: ' + str(affirmation) + '---------')
            if affirmation == 0:
                affirmate = False
            if affirmation == 1:
                affirmate = False
                repeat = False
    newClient.cambiarPedido(drink)
    clients.append(newClient)
    print()
    clientCount+=1

def launchRequestDrink():
    global speakThread
    speakThread = Thread(target = requestDrink, args = ())
    speakThread.start()

def requestNewPerson():
    dw.set_led_head(dw.led_colors['GREEN'])
    OralInteraction.askForNewPerson()
    newPerson = OralInteraction.affirmationCheck(OralInteraction.captureAudio())
    while newPerson == -1:
        dw.set_led_head(dw.led_colors['GREEN'])
        OralInteraction.apologize()
        OralInteraction.askForNewPerson()
        newPerson = OralInteraction.affirmationCheck(OralInteraction.captureAudio())
    if(newPerson==1):
        dw.set_led_head(dw.led_colors['GREEN'])
        OralInteraction.say_something('De acuerdo')
        OralInteraction.say_something('Esperaré al siguiente cliente')
    else:
        dw.set_led_head(dw.led_colors['GREEN'])
        OralInteraction.say_something('Está bien')
        OralInteraction.say_something('Iré a realizar el pedido al bar')
    signals['newPerson'] = (newPerson == 1)


        # affirmate = True
        # while affirmate:
        #     dw.set_led_head(dw.led_colors['GREEN'])
        #     OralInteraction.verifyNewPerson(newPerson)
        #     affirmation = -1
        #     while affirmation == -1:
        #         affirmation = OralInteraction.affirmationCheck(OralInteraction.captureAudio())
        #     if affirmation == 0:
        #         affirmate = False
        #     if affirmation == 1:
        #         affirmate = False
        #         repeat = False

    # newPersonBoolean = OralInteraction.affirmationCheck(newPerson) == 1
    # signals['newPerson'] = newPersonBoolean

def launchRequestNewPerson():
    global speakThread
    speakThread = Thread(target = requestNewPerson, args = ())
    speakThread.start()

def listingRequest():
    global clients, missingDrink, alternatives

    #-----------------INDUCIR CLIENTES-----------------

    # clients = [		Cliente("Bryan","un vino","no esta listo"), \
    # 				            Cliente("Lyna","una gaseosa","no esta listo"), \
    # 				            Cliente("Fabián","café","no esta listo")]
    # dictionary = {'age':21,'gender':"male", 'smile':0, 'beard':0.2, 'glasses':"glasses", 'bald' : 0.2, 'hairColor' : "brown", 'eyeMakeUp':True, 'lipMakeUp':True,'headWear':0.9, 'mustache':0.1}
    # for i in range(len(clients)):
    #  	clients[i].assignAttributes(dictionary)

    #---------------------------------------------------

    missingDrink = MissingDrink(clients, capture)
    dw.set_led_head(dw.led_colors['GREEN'])
    OralInteraction.listingRequest(clients)
    waitingBarman = False
    while not waitingBarman:
        dw.set_led_head(dw.led_colors['GREEN'])
        waitingBarman = OralInteraction.waitingBarmanResponse()
    done = False
    takePhoto = True
    while takePhoto:
        while not done:
            done = missingDrink.takeBarPhoto()
        missingDrink.analyzeImage()
        clients = missingDrink.checkOrder()
        verify = True
        while verify:
            dw.set_led_head(dw.led_colors['GREEN'])
            OralInteraction.listingMissingObjects(clients)
            verificationAccepted = OralInteraction.verifyMissingObject()
            if verificationAccepted == 1:
                takePhoto = False
                verify = False
            elif verificationAccepted == 0:
                verify = False
            else:
                dw.set_led_head(dw.led_colors['GREEN'])
                OralInteraction.apologizeBarman()
    reqAlternatives = False
    for client in clients:
        if client.darEstadoPedido() == "no esta listo":
            reqAlternatives = True
            break
    while reqAlternatives:
        dw.set_led_head(dw.led_colors['GREEN'])
        OralInteraction.requestAlternatives()
        dw.set_led_head(dw.led_colors['GREEN'])
        alternatives = OralInteraction.listeningAlternatives()
        while alternatives == '':
            OralInteraction.apologizeBarman()
            alternatives = OralInteraction.listeningAlternatives()
        alternativesAccepted = -1
        while alternativesAccepted == -1:
            dw.set_led_head(dw.led_colors['GREEN'])
            alternativesAccepted = OralInteraction.verifyAlternatives(alternatives)
        if alternativesAccepted == 1:
            reqAlternatives = False
        else:
            dw.set_led_head(dw.led_colors['GREEN'])
            # OralInteraction.apologizeAlternatives()
            reqAlternatives = True
    dw.set_led_head(dw.led_colors['GREEN'])

    # alternatives = "gaseosa y café"

    OralInteraction.waveBarman()

def launchListingRequest():
    global speakThread
    speakThread = Thread(target = listingRequest, args = ())
    speakThread.start()

def launchRequestClients():
    global speakThread
    speakThread = Thread(target = OralInteraction.requestClients, args = ())
    speakThread.start()

def informOrderState():
    global clients, Recognized_name, newOrder
    dw.set_led_head(dw.led_colors['GREEN'])
    beverageFound = OralInteraction.informOrderState(clients, Recognized_name)
    if beverageFound:
        for i, client in enumerate(clients):
            if (Recognized_name == client.darNombre()):
                del clients[i]
                break
    elif beverageFound == False:
        dw.set_led_head(dw.led_colors['GREEN'])
        OralInteraction.apologizeClient()
        repeat = True
        while repeat:
            dw.set_led_head(dw.led_colors['GREEN'])
            OralInteraction.listingAlternatives(alternatives)
            dw.set_led_head(dw.led_colors['GREEN'])
            newOrder = OralInteraction.listeningDrink(OralInteraction.captureAudio())
            while newOrder == "":
                dw.set_led_head(dw.led_colors['GREEN'])
                OralInteraction.apologize()
                dw.set_led_head(dw.led_colors['GREEN'])
                OralInteraction.listingAlternatives(alternatives)
                dw.set_led_head(dw.led_colors['GREEN'])
                newOrder = OralInteraction.listeningDrink(OralInteraction.captureAudio())
            affirmate = True
            while affirmate:
                dw.set_led_head(dw.led_colors['GREEN'])
                confirmRes = OralInteraction.confirmOrder(newOrder)
                if confirmRes == 0:
                    affirmate = False
                if confirmRes == 1:
                    affirmate = False
                    repeat = False


def launch_informOrderState():
    global speakThread
    speakThread = Thread(target = informOrderState, args = ())
    speakThread.start()

def informNewChoice():
    global clients, newOrder
    dw.set_led_head(dw.led_colors['GREEN'])
    OralInteraction.informNewChoice(clients, newOrder)
    waitingBarman = False
    while not waitingBarman:
        dw.set_led_head(dw.led_colors['GREEN'])
        waitingBarman = OralInteraction.waitingBarmanResponse()
    clients[0].cambiarEstadoPedido('esta listo')
    dw.set_led_head(dw.led_colors['GREEN'])
    OralInteraction.listingMissingObjects(clients)
    dw.set_led_head(dw.led_colors['GREEN'])
    verificationAccepted = OralInteraction.verifyMissingObject()
    dw.set_led_head(dw.led_colors['GREEN'])
    OralInteraction.returnToClients(clients)

def launch_informNewChoice():
    global speakThread
    speakThread = Thread(target = informNewChoice, args = ())
    speakThread.start()

def askForMissingClient():
    dw.set_led_head(dw.led_colors['GREEN'])
    OralInteraction.askForMissingClient(clients)

def launch_askForMissingClient():
    global speakThread
    speakThread = Thread(target = askForMissingClient, args = ())
    speakThread.start()

def informReadyChoice():
    dw.set_led_head(dw.led_colors['GREEN'])
    OralInteraction.informReadyChoiceClient(clients)
    dw.set_led_head(dw.led_colors['GREEN'])
    OralInteraction.finalExit()

def launch_informReadyChoice():
    global speakThread
    speakThread = Thread(target = informReadyChoice, args = ())
    speakThread.start()
