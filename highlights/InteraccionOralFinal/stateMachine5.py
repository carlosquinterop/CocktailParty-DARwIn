from OralInteraction import OralInteraction
from Cliente import Cliente
DictionaryStates = {'start':1, 'askForClient':2, 'waitForClient':3, 'informReadyChoice':4,'die':5}

OralInteraction= OralInteraction()
# Arreglo de clientes inventado para la máquina de estados
clients = [Cliente("Adelaida ","un cóctel","no esta listo"), Cliente("Juan José","una gaseosa","esta listo"), Cliente("Pedro","un cafe con leche","esta listo")]

state = 'start'
while True:
	print(state)
	if state == 'start':
		state = 'askForClient'

	if state == 'askForClient':
		OralInteraction.askForMissingClient(clients)
		state = 'waitForClient'

	if state == 'waitForClient':
		input("Press enter for informReadyChoice")
		state = 'informReadyChoice'

	if state == 'informReadyChoice':
		OralInteraction.informReadyChoiceClient(clients)
		state = 'die'

	if state == 'die':
		OralInteraction.finalExit()