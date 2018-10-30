#from Cliente import Cliente
from T2SThread import T2SThread
import os
import speech_recognition as sr
import csv
import time
import os
import sys
from ListasEntendimiento import ListasEntendimiento
import random
from gtts import gTTS
# import playsound
from Saludos import Saludos

class OralInteraction():
    def __init__(self):
        #super(MainWindow, self).__init__()
        self.t2sThread = T2SThread()
        #self.t2sThread = T2S()
        self.t2sThread.start()
        self.saludos = Saludos()
        #Declaración de Strings necesarios
        self.ListasEntendimiento = ListasEntendimiento()
        #self.clientes = []
        self.listaNombres = self.ListasEntendimiento.darListaNombres()
        self.listaPedidos = self.ListasEntendimiento.darListaPedidos()
        self.listaAfirmaciones = self.ListasEntendimiento.darListaAfirmaciones()
        self.listaNegaciones = self.ListasEntendimiento.darListaNegaciones()
        self.listaBartender = self.ListasEntendimiento.darListaBartender()
        self.listaAlternativas = self.ListasEntendimiento.darListaAlternativas()
        self.listaAjustePedido = self.ListasEntendimiento.darListaAjustePedido()
        self.listNameBegin = ["llamo", "es", "soy"]
        self.listNameEnd = ["y", "estudio"]
        self.prep = ["la", "La", "el", "El"]
        #self.totalClientes = 1
        #self.alternativas = ""
        #self.alternativaReemplazo = ""
        #self.clienteFaltante = Cliente("", "", "no esta listo")

    # ------------------------------------------------------------------------------
    # -------------------------- Métodos Principales -------------------------------
    # ------------------------------------------------------------------------------

    # ---------------------- Interacción con los clientes --------------------------
    #Saludo al cliente
    def greet(self):
        string = self.saludos.darSaludos(random.randint(1,3))
        self.say_something(string)

    #Disculparse por comprender mal el nombre
    def apologize(self):
        string = self.saludos.disculpar(random.randint(1,3))
        self.say_something(string)

    #Asks the client for name
    def askForName(self):
        string = self.saludos.solicitarNombre(random.randint(1,3))
        self.say_something(string)

    #Obtains the name upon a string
    def listeningName(self, string):
        words = string.split()
        for i in (self.listNameBegin):
            if i in words:
                beginingName = words.index(i)+1
        for j in (self.listNameEnd):
            if j in words:
                endName = words.index(j)-1
        name = self.buildString(words[beginingName:endName])
        return name

    #Asks the client for drink
    def askForDrink(self):
        string = self.saludos.solicitarPedidos(random.randint(1,3))
        self.say_something(string)

    #Obtains the drink upon a string
    def listeningDrink(self, string):
        palabras = string.split()
        pedido = ""
        for i in palabras:
            if i in self.listaPedidos:
                auxPedido = palabras[(palabras.index(i)):(len(palabras))]
            else:
                auxPedido = palabras
        for i in self.listaAjustePedido:
            if i in auxPedido:
                auxPedido.remove(i)

        pedido = self.buildString(auxPedido)
        print(pedido)
        return pedido

    #Asks the client for newPerson
    def askForNewPerson(self):
        string = self.saludos.masClientes(random.randint(1,3))
        self.say_something(string)

    #Confirms the understood name
    def verifyName(self, pName):
        verificacionInicial = self.saludos.verificarNombres(random.randint(1,3))
        verificacionFinal = self.saludos.verificarFinal(random.randint(1,3))
        string = verificacionInicial + pName + verificacionFinal
        self.say_something(string)

    #Confirms the understood drink
    def verifyDrink(self, pDrink):
        verificacionInicial = self.saludos.verificarPedidos(random.randint(1,3)) + pDrink
        verificacionFinal = self.saludos.verificarFinal(random.randint(1,3))
        string = verificacionInicial + verificacionFinal
        self.say_something(string)

    #Confirms the understood newPerson
    def verifyNewPerson(self, pNewPerson):
        string = "Comprendí que " + pNewPerson + " hay una nueva persona. Estoy en lo correcto?"
        self.say_something(string)

    #If there are no more clients
    def exit(self):
        string = self.saludos.noMasClientes(random.randint(1,3))
        self.say_something(string)

 # ------------------------------------- Interacción con el Bartender ---------------------------------
    # Informar al bartender los pedidos obtenidos
    def listingRequest(self, clientes):
        self.say_something("Hola, Héctor, los pedidos que recibí son los siguientes:")
        x = 0
        while x < len(clientes):
            self.clientAttributes(clientes[x])
            x+=1
        self.say_something("Avísame cuando esten listos")

    def waitingBarmanResponse(self):
        alternativesReady = 0
        string = self.captureAudio()
        response = string.split()
        listado = []
        for i in response:
            if i in self.listaBartender:
                alternativesReady = 1
        return alternativesReady

    # Escuchar al bartender las alternativas disponibles
    def listingMissingObjects(self, clientes):
        ordenCompleta = 0
        for i in clientes:
            if(i.darEstadoPedido() == "no esta listo"):
                ordenCompleta = 0
                clienteFaltante = i
            else:
                ordenCompleta = 1
        if ordenCompleta:
            self.say_something("Veo que la orden está completa")
        else:
            self.askForAlternatives(clienteFaltante)

        return ordenCompleta

    def verifyMissingObject(self):
        self.say_something("¿Estoy en lo correcto?")
        return self.affirmationCheck(self.captureAudio())

    def requestAlternatives(self):
        self.say_something("¿Que alternativas tienes?")

    def introduction(self):
        string = "Hola, mi nombre es Darwin. ¿Tú quién eres?"
        # self.t2sThread.say_something(string)
        self.say_something(string)
        # time.sleep(5)

    #Disculparse por comprender mal el nombre
    def answerIntroduction(self, name, university):
        string = "Hola" + name + ". ¿Qué estudias en "+ university+ "?"
        # self.t2sThread.say_something(string)
        self.say_something(string)
        # time.sleep(7)

    #def listeningPresentation(self):
    #    string = self.captureAudio()
    #    words = string.split()
    #    for i in (self.listNameBegin):
    #        if i in words:
    #            beginingName = words.index(i)
    #    for j in (self.listNameEnd):
    #        if j in words:
    #            endName = words.index(j)
    #    name = self.buildString(words[beginingName:endName])

    def listeningUniversity(self,string):
        words = string.split()
        for a in (self.prep):
            if a in words:
                beginingUniversity = words.index(a)
        university = self.buildString(words[beginingUniversity:len(words)])
        return university

    def listeningAlternatives(self):
        string = self.comprensionAlterntivas(self.captureAudio())
        return string

    def verifyAlternatives(self, alternatives):
        self.verifyAlternativesBartender(alternatives)
        return self.affirmationCheck(self.captureAudio())

    def waveBarman(self):
        farewellBarman = ("Listo. Le avisaré a los clientes")
        self.say_something(farewellBarman)

    def apologizeBarman(self):
        self.say_something("Disculpa verifique mal, verificaré de nuevo")

    def apologizeAlternatives(self):
        self.say_something("Que pena, te entendí mal, podrías repetirlo?")

    # ------------------------ Segunda interacción con el Cliente -------------------------------
    def requestClients(self):
        self.say_something("Por favor, acérquense las personas que ordenaron algo")

    def informOrderState(self, clients, nombre):
        for i in clients:
            if (nombre == i.darNombre()):
                cliente = i

        bFound = 0
        if( cliente.darEstadoPedido() == "esta listo"):
            string = "Hola" + cliente.darNombre() + "tu pedido está listo en la barra"
            self.say_something(string)
            bFound = 1
        else:
            string = "Hola" + cliente.darNombre() + "tu pedido no está disponible en el momento"
            self.say_something(string)
            bFound = 0
        return bFound

    def apologizeClient(self):
        self.say_something("Disculpa por el inconveniente")

    def listingAlternatives(self, alternatives):
        self.say_something("Puedes pedir alguna de las siguientes alternativas: " + alternatives + " ¿Cúal deseas?")

    def listenChoice(self):
        string = self.captureAudio()
        palabras = string.split()
        auxAlternativas =[]
        for i in palabras:
            if i in self.listaAlternativas:
                auxAlternativas = palabras[(palabras.index(i)+1):(len(palabras))]
                if "por" in auxAlternativas:
                    auxAlternativas.remove("por")
                if "porfavor" in auxAlternativas:
                    auxAlternativas.remove("porfavor")
                if "favor" in auxAlternativas:
                    auxAlternativas.remove("favor")
                if "gracias" in auxAlternativas:
                    auxAlternativas.remove("gracias")
                if "y" in auxAlternativas:
                    auxAlternativas.remove("y")
                if ("esta" in auxAlternativas):
                    auxAlternativas.remove("esta")
                if ("está" in auxAlternativas):
                    auxAlternativas.remove("está")
                if ("bien" in auxAlternativas):
                    auxAlternativas.remove("bien")
                alternativa = self.buildString(auxAlternativas)
                if ("quiero" in auxAlternativas):
                    auxAlternativas.remove("quiero")
            elif len(palabras)<=2:
                alternativa = string
        return alternativa

    def confirmOrder(self, newAlternative):
        self.verifyDrink(newAlternative)
        string = self.captureAudio()
        return self.affirmationCheck(string)

    def askForRepeat(self):
        self.say_something("¿Podrías repetirme tu elección?")

    # --------------------------- Segunda interacción con el Bartender ----------------------
    def informNewChoice(self, clients, newOrder):
        for i in clients:
            if(i.darEstadoPedido() == "no esta listo"):
                clienteFaltante = i
        string = "Hola Héctor, " + clienteFaltante.darNombre() + " cambió su pedido por " + newOrder + " Avísame cuando este listo"
        self.say_something(string)

    def returnToClients(self, clients):
        for i in clients:
            if(i.darEstadoPedido() == "esta listo"):
                clienteFaltante = i
        self.say_something("Le informaré " + clienteFaltante.darNombre() + " que su nuevo pedido está listo. Gracias")


    #-------------------------- Tercera interacción con los clientes-----------------------------
    def askForMissingClient(self, clients):
        for i in clients:
            if(i.darEstadoPedido() == "no esta listo"):
                clienteFaltante = i
        self.say_something(clienteFaltante.darNombre() +", podría pedirte el favor de que te ubiques frente a mi?")

    def informReadyChoiceClient(self, clients):
        for i in clients:
            if(i.darEstadoPedido() == "no esta listo"):
                clienteFaltante = i
        self.say_something("Hola, "+ clienteFaltante.darNombre() + " el cambio de tu pedido está listo.")

    def finalExit(self):
        self.say_something("Hasta pronto, nos vemos en Australia")

    # ---------------------------------------------------------------------------------------------
    # ------------------------------------ Sub-procesos -------------------------------------------
    # ---------------------------------------------------------------------------------------------
    #Builds the bartender string with the requests
    def stringBartender(self, nombre, pedido):
        string = nombre + "me pidió" + pedido
        self.say_something(string)
        time.sleep(4)

    #Asks  the bartender for alternatives
    def askForAlternatives(self, clienteFaltante):
        string = "Veo que falta el pedido de " + clienteFaltante.darNombre()
        self.say_something(string)
        time.sleep(6)

    #Informs the client the available alternatives
    def informAlternativas(self, alternativas, clienteFaltante):
        string = "Lo siento" + clienteFaltante.darNombre() + " . No tengo " + clienteFaltante.darPedido() + ". Podría ofrecerte: " + self.alternativas + ". ¿Que te gustaría?"
        self.say_something(string)
        time.sleep(5)

    #comprensionBartender
    #Returns true when the bartender is ready with the drinks
    def listeningBartender(self, string):
        palabras = string.split()
        entendido = False
        for i in palabras:
            if i in self.listaBartender:
                entendido = True
        return entendido

    #comprensionAlternativas
    #Obtains the avilable alternativs upon a string
    def listeningAlternativesBartender(self, string):
        opciones = string.split()
        listado = []
        for i in opciones:
            if i == "son":
                listado = opciones[opciones.index(i)+1:len(opciones)]
        alternativas = self.buildString(listado)
        return alternativas

    #compresionAlternativaCliente
    #obtains the chosen alternative from the client upon a string
    def listeningAlternativesClient(self,string):
        palabras = string.split()
        auxAlternativas =[]
        for i in palabras:
            if i in self.listaAlternativas:
                auxAlternativas = palabras[(palabras.index(i)+1):(len(palabras))]
            else:
                auxAlternativas = palabras
        alternativa = self.buildString(auxAlternativas)
        return alternativa

    #verificarAlternativas
    #verifies the understood avilable alternatives
    def verifyAlternativesBartender(self, alternatives):
        verificacionInicial = "Comprendí las alternativas son "
        verificacionFinal = self.saludos.verificarFinal(random.randint(1,3))
        string = verificacionInicial + alternatives + verificacionFinal
        self.say_something(string)

    #Métodos adicionales
    #Reconstruccion de strings
    def buildString(self,lista):
        reconstruido = ""
        for i in lista:
            reconstruido +=i
            reconstruido +=" "
        return reconstruido

    #Encuentra el cliente que pidio el objeto faltante
    def objetoFaltante(self):
        self.csvfile_reader()
        self.clienteFaltante =  Cliente("","","")
        for i in self.clientes:
            if i.darEstadoPedido() == "no esta listo":
                self.clienteFaltante = self.clientes[self.clientes.index(i)]
        return self.clienteFaltante

    #"Una bolella de agua" -> "botella de agua"
    #Quitar el articulo en el pedido
    def ajustePedido(self,pPedido):
        separado = pPedido.split()
        final = self.buildString(separado[1:len(separado)])
        return final

    #Afirmacion no negacion
    def affirmationCheck(self, string):
        palabras = string.split()
        afirmacion = False
        for i in palabras:
            if i in self.listaAfirmaciones:
                afirmacion = True
        return afirmacion

    def comprensionAlterntivas(self, string):
        opciones = string.split()
        listado = []
        for i in opciones:
            if i == "son":
                listado = opciones[opciones.index(i)+1:len(opciones)]
        alternatives = self.buildString(listado)
        return alternatives

    # --------------------------------- Métodos de audio -----------------------------------
    # Captura de audio (S2T)
    def captureAudio(self):
        r = sr.Recognizer()
        with sr.Microphone(device_index = 0, sample_rate = 44100, chunk_size = 512) as source:
            r.adjust_for_ambient_noise(source, duration=2)
            print("Recording")
            audio = r.listen(source, phrase_time_limit=5)
        #try:
        #    audio1 =r.recognize_ibm(audio, language='es-ES', username="0d53ad4a-5068-4a73-bcbb-8e119e6c9ff6", password="GKNXDhqEfvAb")
        #    print(audio1)
        #except sr.UnknownValueError:
        #    audio1 = "IBM Speech to Text could not understand audio"
        #except sr.RequestError as e:
        #    audio1 = "Could not request results from IBM Speech to xText service"
        try:
            audio1 = r.recognize_google(audio, language='es-ES')
            print(audio1)
        except sr.UnknownValueError:
            audio1 = " "
        except sr.RequestError as e:
            audio1 = " "
        return audio1

    # Método de habla (T2S)
    def say_something(self,text):
        grabacion = gTTS(text = text, lang = 'es')
        grabacion.save('output.mp3')
        os.system("mpg321 -q output.mp3")



    #------------------------------------------------------------------------------------
    # ------------------------------- Codigo pasado -------------------------------------
    #------------------------------------------------------------------------------------
    #Informar al cliente de las alternativas dispinibles, escucha y verifica la respeusta
    def clienteAlternativaReemplazo(self):
        self.informarAlternativas(self.alternativas, self.clienteFaltante)
        time.sleep(10)
        self.alternativaReemplazo = self.compresionAlternativaCliente(self.capturarAudio())
        self.verificarPedido(alternativaReemplazo)

    #Le infroma al bartender de la alternativa reemplzao
    def bartenderAlternativaReemplazo(self):
        self.stingBartender(self.clienteFaltante.darNombre(),self.clienteFaltante.darPedido())
        time.sleep(10)

    def todosLosMetodos(self):
    	self.pedidos()
    	self.bartender()
    	self.alternativasProductoFaltante()
    	self.clienteAlternativaReemplazo()
    	self.bartenderAlternativaReemplazo()


    ##################################

    def clientAttributes(self, client):
        nombre = client.darNombre()
        pedido = client.darPedido()
        age = client.giveAge()

        if client.giveGlasses() == "glasses":
            glasses = "tiene gafas"
        else:
            glasses = "no tiene gafas"
        color = {'blonde': "mono", 'black':"negro", 'red':"rojo",'brown':"cafe"}
        hairColor = color[client.giveHairColor()]
        if client.giveHeadWear() > 0.7:
            cabeza = "tiene sombrero"
        elif client.giveBald() > 0.7:
            cabeza = "es calvo"
        else:
            hairColor = color[client.hairColor]
            cabeza = "tiene pelo " + hairColor

        if client.giveBeard() < 0.3:
            barba = "no tiene barba"
        elif client.giveBeard() > 0.7:
            barba = "tiene barba"
        else:
            barba = "tiene poca barba"

        if client.giveEyeMakeUp():
            eyeMakeUp = ""
        else:
            eyeMakeUp = "no"

        if client.giveLipMakeUp():
            lipMakeUp = ""
        else:
            lipMakeUp = "no"

        if client.giveGender() == "male":
            gender = "hombre"
            string = nombre + " quien " + cabeza + ", " + glasses + " y " + barba + "me pidio " + pedido
            tiempo = 8
        else :
            gender = "mujer"
            string = nombre + " quien " + cabeza + ", " + glasses + ", " + eyeMakeUp + "tiene maquillaje en los ojos y" + lipMakeUp + " tiene labial me pidió " + pedido
            tiempo = 10

        self.say_something(string)
