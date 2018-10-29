# State machine used for testing object recognition
# Developed by Sinfonia Pepper Team
# Universidad Santo Tomas and Universidad de Los Andes
# Bogota, Colombia
# October 2018

import sys

# Importing class 'objectRecognition'
from objectRecognition import ObjectRecognition

# Possible states dictionary
dictionary_states = { 'greeting' : 1 , 'takingPhoto' : 2 , 'processingImage' : 3 , 'speakingObjects' : 4 , 'awaitingInput' : 5 , 'goodbye' : 6 }

# State variable used on the state machine
state = 'awaitingInput'

objectRecognition = ObjectRecognition()

# Endless loop used for the state machine
while True:
	if state == 'awaitingInput':
		input( "Presione ENTER para iniciar" )
		state = 'greeting'
	elif state == 'greeting':
		
		state = 'takingPhoto'
	elif state == 'takingPhoto':
		objectRecognition.takePhoto()
		state = 'processingImage'
	elif state == 'processingImage':
		objectRecognition.processPhoto()		
		state = 'speakingObjects'
	elif state == 'speakingObjects':
		objectRecognition.speakObjects()
		state = 'goodbye'
	elif state == 'goodbye':
		sys.exit()
	
