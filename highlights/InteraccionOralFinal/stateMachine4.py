from OralInteraction import OralInteraction
from Cliente import Cliente
from missingDrink import MissingDrink
import time
#Diccionario de estados
DictionaryStates = {'start' : 1, 'waitForBarman' : 2, 'informNewChoice' : 3, 'waitForBarmanResponse':5, 'verifyBarmanResponse':7, 'returnToClients':8, 'takeBarPhoto':9, 'analyzeImage':10}
# Arreglo de clientes inventado para la máquina de estados
clients = [Cliente("Adelaida ","una gaseosa","no esta listo")]
# String con el nuevo pedido del cliente al que le falto la bebida
newOrder = "una gaseosa"
OralInteraction= OralInteraction()
missingDrink = MissingDrink(clients)
verificationAccepted = False

state = 'start'
while 1:
	print(state)
	if state == 'start':
		state = 'waitForBarman'

	if state == 'waitForBarman':
		input("Press enter if barman is ready to listen")
		state = 'informNewChoice'

	if state == 'informNewChoice':
		#Dice el nuevo pedido del cliente faltante
		OralInteraction.informNewChoice(clients, newOrder)
		state = 'waitForBarmanResponse'
	
	if state == 'waitForBarmanResponse':
		waitingBarman = OralInteraction.waitingBarmanResponse()
		if waitingBarman==True:
			state = 'takeBarPhoto'
		else:
			state = 'waitForBarmanResponse'

	if state == 'takeBarPhoto':
		done = missingDrink.takeBarPhoto()
		if done:
			state='analyzeImage'

	if state == 'analyzeImage':
		missingDrink.analyzeImage()
		state='checkOrder'

	if state == 'checkOrder':
		clients = missingDrink.checkOrder()
		state='listingMissingObject'

	if state == 'listingMissingObject':
		completeOrder = OralInteraction.listingMissingObjects(clients)
		if completeOrder == 1 :
			state = 'verifyCompleteOrder'
		else:
			state='verifyMissingObject'

	if state == 'verifyMissingObject':
		verificationAccepted= OralInteraction.verifyMissingObject()
		if verificationAccepted==True:
			state='returnToClients'
		else:
			verificationAccepted = False
			state='apology'

	if state == 'verifyCompleteOrder':
		OralInteraction.say_something("¿Estoy en lo correcto?")
		if OralInteraction.affirmationCheck(OralInteraction.captureAudio()):
			state = 'returnToClients'
		else:
			verificationAccepted = False
			state = 'apology'

	if state == 'apology':
		if verificationAccepted == False:
			OralInteraction.apologizeBarman()
			state = 'takeBarPhoto'

	if state == 'returnToClients':
		OralInteraction.returnToClients(clients)