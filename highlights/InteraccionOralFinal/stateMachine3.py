#Maquina de estados vuelta al cliente 
from OralInteraction import OralInteraction
#from missingDrink import MissingDrink
from Cliente import Cliente 
DictionaryStates = {'arriveToClient' : 1, 'requestClients' : 2, 'clientArrived' : 3,'identifyClient':4,'informOrderState':5, 'apology':6, 'listingAlternatives': 9, 'listenChoice':10,'confirmOrder':11, 'returnToBar':13, 'exit':14, 'arrivedNewClient':15, 'confirmUnderstoodNewChoice' : 16}
clients = [Cliente("Adelaida","un guarito","no esta listo"),Cliente("Juan","un cafe","esta listo"),Cliente("José","un milo","esta listo")]
OralInteraction= OralInteraction()
#missingDrink= MissingDrink() 
beverageFound= False
# Variable para la nueva orden
newOrder= " "
# Numero de clientes totales
totalClients = len(clients)-1
# Variable de iteración
i = 0
# Alternativas dadas por el bartender previamente
alternatives = " agua, gaseosa o cerveza"
# arreglo de nombres que le pueden pasar dependiendo de la persona que identifica, en la practica solo es el string que se identifica en IdentifyClient
nombres = ["Adelaida", "Juan", "José"]
missUnderstoodNewOrder = False
apologizeBeveerageNotFound = False

state = 'arriveToClient'
while 1:
	if state == 'arriveToClient':
		input("Press Enter to state arriveToClient")
		state='requestClients'

	if state == 'requestClients':
 		OralInteraction.requestClients()
 		state='clientArrived'
	
	while i <= totalClients:
		print(state)
		print(i)
		if state == 'clientArrived':
 			input("Press Enter to state identifyClient ")
 			state='identifyClient'

		if state == 'identifyClient':
 			input("Press Enter to state informOrderState")
 			state='informOrderState'
	
		if state == 'informOrderState':
 			beverageFound = OralInteraction.informOrderState(clients, nombres[i])
 			if beverageFound== True:
 				#if i == totalClients:
 				#	state='returnToBar'
 				#else:
 				i = i + 1
 				clients.remove(clients[i])
 				if i > totalClients:	
 					state='returnToBar'
 				else:
 					state = 'arrivedNewClient'
 			elif beverageFound==False:
 				apologizeBeveerageNotFound = True
 				state= 'apology'
		
		if state == 'arrivedNewClient':
			input("Press Enter to state identifyClient")
			state='identifyClient'

		if state == 'apology':
 			
 			if apologizeBeveerageNotFound:
 				OralInteraction.apologizeClient()
 				state = 'listingAlternatives'
 				apologizeBeveerageNotFound = False

 			if missUnderstoodNewOrder:
 				OralInteraction.apologize()
 				missUnderstoodNewOrder = False
 				OralInteraction.askForRepeat()
 				state = 'listenChoice'

		if state == 'listingAlternatives':
 			OralInteraction.listingAlternatives(alternatives)
 			state='listenChoice'
 			#retornar lista 

		if state == 'listenChoice':
 			newOrder = OralInteraction.listeningDrink(OralInteraction.captureAudio())
 			print(newOrder)
 			state='confirmOrder'

		if state == 'confirmOrder':
 			if OralInteraction.confirmOrder(newOrder):
	 			i += 1
	 			state='confirmUnderstoodNewChoice'
	 		else:
	 			missUnderstoodNewOrder = True
	 			state = 'apology'
 			#mandar como parámetro el nuevo order 
		if state == 'confirmUnderstoodNewChoice':
			OralInteraction.exit()
			state = 'arrivedNewClient'

	if state == 'returnToBar':
		print(state)
		input("Press Enter to state returnToBar")