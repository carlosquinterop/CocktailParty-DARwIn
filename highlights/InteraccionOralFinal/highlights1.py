#Adaptacion de OralInteraction para highlights
#Maquina de estados vuelta al cliente
from OralInteraction import OralInteraction
import darwin_tcp.darwin as dw
#from missingDrink import MissingDrink
#from Cliente import Cliente
States = {'start' : 1, 'introduction' : 2, 'listening' : 3,'answer':4,'final':5}

dw.init(20063)

OralInteraction = OralInteraction()

state = States['start']
while True:

	if state == States['start']:
		input("Presione enter para empezar")
		state = States['introduction']

	if state == States['introduction']:
		dw.set_action(dw.actions['SPEAK06'])
		OralInteraction.introduction()
		dw.stop_action(dw.actions['STAND'])
		state = States['listening']

	if state == States['listening']:
		string = OralInteraction.captureAudio()
		name = OralInteraction.listeningName(string)
		print("Nombre: " + str(name))
		university = OralInteraction.listeningUniversity(string)
		print("Universidad: "+ str(university))
		state = States['answer']

	if state == States['answer']:
		dw.set_action(dw.actions['SPEAK06'])
		OralInteraction.answerIntroduction(name,university)
		dw.stop_action(dw.actions['STAND'])
		state = States['final']

	if state == States['final']:
		print("final")
