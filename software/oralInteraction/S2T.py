#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class
import os 
import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone(device_index = 5, sample_rate = 44100, chunk_size = 512) as source:
	r.adjust_for_ambient_noise(source, duration=1)
	print("Say something!")
	audio = r.listen(source,phrase_time_limit=5)


    #IBM_USERNAME = "0d53ad4a-5068-4a73-bcbb-8e119e6c9ff6"
	#IBM_PASSWORD = "GKNXDhqEfvAb"
#try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
	#print("Google thinks You said: " + r.recognize_google(audio, language='es-ES'))
#except sr.UnknownValueError:
	#print("Google Speech Recognition could not understand audio")
#except sr.RequestError as e:
	#print("Could not request results from Google Speech Recognition service; {0}".format(e))


try:
	print("IBM Speech to Text thinks you said: " + r.recognize_ibm(audio, language='es-ES', username="0d53ad4a-5068-4a73-bcbb-8e119e6c9ff6", password="GKNXDhqEfvAb"))
except sr.UnknownValueError:
	print("IBM Speech to Text could not understand audio")
except sr.RequestError as e:
	print("Could not request results from IBM Speech to xText service; {0}".format(e))