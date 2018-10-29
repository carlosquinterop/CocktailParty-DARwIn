# State machine used for testing object recognition
# Developed by Sinfonia Pepper Team
# Universidad Santo Tomas and Universidad de Los Andes
# Bogota, Colombia
# October 2018

import sys
from characterization import Characterization
from oralInteraction import OralInteraction
import darwin_tcp.darwin as dw
import time

dw.init(20070)

C = Characterization()

# Possible states dictionary
dictionary_states = { 'greeting' : 1 , 'takingPhotos' : 2 , 'learningPerson' : 3 , 'speakingAttributes' : 4 , 'awaitingInput' : 5 , 'goodbye' : 6 }
dictionary_atributes ={'male' : 'hombre', 'female' : 'mujer', 'eyeglasses': 'tienes gafas', \
						'noglasses' : 'no tienes gafas', 'brown' : 'cafe', 'blond' : 'rubio', 'red' : 'rojo', \
						'gray' : 'gris', 'black' : 'negro', 'other' : 'otro color'}
# State variable used on the state machine
state = 'awaitingInput'

oralInteraction = OralInteraction()

attributes = ['cabello negro']
person_name = 'Person16'

# Endless loop used for the state machine
while True:
	if state == 'awaitingInput':
		input( "Presione ENTER para iniciar" )
		state = 'greeting'
	elif state == 'greeting':

		dw.stop_action(dw.actions['SPEAK06'])
		oralInteraction.sayHello()
		time.sleep(2)
		state = 'takingPhotos'
	elif state == 'takingPhotos':
		dw.set_head_angle(0,110)
		time.sleep(1)
		C.add_person(person_name)
		state = 'speakingAttributes'
	# elif state == 'learningPerson':
	# 	input( "Estado aprendiendo persona" )
	# 	state = 'speakingAttributes'
	elif state == 'speakingAttributes':

		attributes = ['Reconozco que eres ' + dictionary_atributes[C.get_person_attribute(person_name)['gender']] \
						+ ', ' +  dictionary_atributes[C.get_person_attribute(person_name)['glasses']] \
						+ ' y tu color de cabello es ' + dictionary_atributes[C.get_person_attribute(person_name)['hairColor']]]
		dw.stop_action(dw.actions['SPEAK06'])
		oralInteraction.sayAttributes(attributes)
		state = 'goodbye'
	elif state == 'goodbye':
		sys.exit()
