import os
from gtts import gTTS


class OralInteraction():

	def __init__(self):
		print("Ready to use")

	def sayHello(self):
		txt_line = "Hola, espera un instante mientras me aprendo tu cara."
		tts = gTTS( text=txt_line , lang='es' )
		tts.save("audio.mp3")
		os.system( "mpg123 -q audio.mp3" )

	def sayAttributes(self , attributes):
		txt_line = ""
		for attribute in attributes:
			txt_line += attribute
			txt_line += " "
		tts = gTTS( text=txt_line , lang='es' )
		tts.save("audio.mp3")
		os.system( "mpg123 -q audio.mp3" )
