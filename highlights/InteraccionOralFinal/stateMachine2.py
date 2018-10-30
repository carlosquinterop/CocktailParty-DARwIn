#Maquina de estados bartender
from OralInteraction import OralInteraction
from missingDrink import MissingDrink
from Cliente import Cliente

DictionaryStates = {'barArrive' : 1, 'waitingPerson' : 2, 'listingRequest' : 3,'waitingBarmanResponse':4,'verifyAvailableDrinks':5, 'listingMissingObject':6, 'verifyMissingObjects':7,'requestAlternatives': 8, 'listeningAlternatives': 9, 'verifyAlternatives':10,'returnToClients':11, 'arriveToClient':12, 'apology':13, 'exit':14, 'takeBarPhoto':15, 'analyzeImage':16, 'checkOrder':17,'waveBarman':18}
 

#Arreglo con los cliente de prueba para la maquina de estados. Comentar si es necesario.
#Cliente = Cliente("","","no esta disponible")
clients = [Cliente("Adelaida Zuluaga","un guarito","no esta listo"), Cliente("Juan José","una gaseosa","no esta listo"), Cliente("Juana","un cafe","no esta listo")]
#clients = [Cliente("","","no esta listo")]
OralInteraction= OralInteraction()
missingDrink= MissingDrink(clients) 
waitingBarman= False 
verificationAccepted= False
alternativesAccepted=False
alternatives = ""

dictionary = {'age':21,'gender':"female", 'smile':0, 'beard':0.2, 'glasses':"glasses", 'bald' : 0.2, 'hairColor' : "brown", 'eyeMakeUp':True, 'lipMakeUp':True,'headWear':0.9, 'mustache':0.1}
for i in range(len(clients)):
 	clients[i].assignAttributes(dictionary)


state = 'barArrive'
while 1:
	print( state )
	if state == 'barArrive':
		state='waitingPerson'

	if state == 'waitingPerson':
 		input("Press Enter to state waitingPerson")
 		state='listingRequest'

	if state == 'listingRequest':
		OralInteraction.listingRequest(clients)
		state = 'waitingBarmanResponse'

	if state == 'waitingBarmanResponse':
		waitingBarman = OralInteraction.waitingBarmanResponse()
		if waitingBarman==True:
			state = 'takeBarPhoto'
		else:
			state = 'waitingBarmanResponse'

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
		OralInteraction.listingMissingObjects(clients)
		state='verifyMissingObject'

	if state == 'verifyMissingObject':
		verificationAccepted= OralInteraction.verifyMissingObject()
		if verificationAccepted==True:
			state='requestAlternatives'
		else:
			state='apology'

	if state == 'apology':
		if verificationAccepted == False:
			OralInteraction.apologizeBarman()
			state = 'takeBarPhoto'
		elif alternativesAccepted== False:
			OralInteraction.apologizeAlternatives()
			state='requestAlternatives'

	if state == 'requestAlternatives':
		OralInteraction.requestAlternatives()
		state='listeningAlternatives'

	if state == 'listeningAlternatives':
		alternatives = OralInteraction.listeningAlternatives()
		state='verifyAlternatives'
		
	if state == 'verifyAlternatives':
		alternativesAccepted = OralInteraction.verifyAlternatives(alternatives)
		if alternativesAccepted==True:
			state='waveBarman'
		else:
			state='apology'

	if state == 'waveBarman':
		OralInteraction.waveBarman()
		state='returnToClients'
		
	if state == 'returnToClients':
		input("Press Enter to state returnToClients")
		state='arriveToClient'

	if state == 'arriveToClient':
		input("Press Enter to state arriveToClient")
		state='exit'

	if state == 'exit':
		OralInteraction.exit()