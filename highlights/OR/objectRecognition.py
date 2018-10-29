# Clase para la identificacion de objetos a partir de una imagen con text to speech.
# Desarrollado por Sinfonia Pepper Team
# Universidad de Los Andes
# Bogota, Colombia
# Octubre de 2018


#------------------------
#	CONFIGS
#------------------------

# Puerto de la camara a usar por parte del programa.
camera_port = 1

# Direccion de salida de las imagenes
img_file_path = "img.jpg"


#------------------------
#	LIBRERIAS
#------------------------

# CV2 librery used for image capture and processing.
import cv2

# Lightnet library used for image processing and object recognition
import lightnet

import os
from gtts import gTTS

class ObjectRecognition():

	# Constructor method
	def __init__(self):
		self.cap = cv2.VideoCapture( camera_port )
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
		self.cap.set(cv2.CAP_PROP_FPS, 10)
		self.model = lightnet.load('yolo')
		self.objects = []
		self.es_dict = { 	"bottle" : "una botella" , \
							'keyboard':'un teclado' , \
							'diningtable':'una mesa' , \
							'cup':'una taza' , \
							'laptop':'un portatil' , \
							'wine glass': 'una copa' }

	# Takes a phot and saves it into a .jpg file
	def takePhoto(self):
		for i in range(10):
			self.cap.read()
		ret, frame = self.cap.read()
		frame = frame[115:600, 320:960]
		frame = cv2.flip(frame,0)
		frame = cv2.flip(frame,1)
		# TODO voltear la camara de DARWIN
		cv2.imwrite( img_file_path , frame )

	# Get objects names from the taken photo
	def processPhoto(self):
		image = lightnet.Image.from_bytes( open( img_file_path , 'rb' ).read() )
		boxes = self.model( image )
		for obj in boxes:
			self.objects.append( obj[1] )

	# T2S objects
	def speakObjects(self):
		txt_line = "He detectado "
		for obj in self.objects:
			txt_line += self.es_dict[ obj ]
			txt_line += ", "
		print( txt_line )
		tts = gTTS( text=txt_line , lang='es' )
		tts.save("audio.mp3")
		os.system( "mpg123 audio.mp3" )

	def sayHello(self):
		txt_line = "Hola, voy a reconocer que objetos tengo frente a mi"
		tts = gTTS( text=txt_line , lang='es' )
		tts.save("audio.mp3")
		os.system( "mpg123 audio.mp3" )
