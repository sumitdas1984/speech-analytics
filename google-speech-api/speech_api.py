#!/usr/bin/env python
# Requires PyAudio and PySpeech.
 
import speech_recognition as sr
import sys
from pydub import AudioSegment
import os

def stt_online(): 
	print "inside stt_online"
	
	# Record Audio
	r = sr.Recognizer()
	with sr.Microphone() as source:
	    print("Say something!")
	    audio = r.listen(source)
	 
	# Speech recognition using Google Speech Recognition
	try:
	    # for testing purposes, we're just using the default API key
	    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
	    # instead of `r.recognize_google(audio)`
	    output = r.recognize_google(audio)
	    print("You said: " + output)
	except sr.UnknownValueError:
	    print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
	    print("Could not request results from Google Speech Recognition service; {0}".format(e))


def stt_offline(input_audio_file):
	print "inside stt_offline"
	print("audio_file: " + input_audio_file)
	
	filename, file_extension = os.path.splitext(input_audio_file)
	print("file extension: " + file_extension)

	if file_extension == '.mp3':
		sound = AudioSegment.from_mp3(input_audio_file)
		sound.export("../data/converted.wav", format="wav")
		AUDIO_FILE = "../data/converted.wav"
	else:
		AUDIO_FILE = input_audio_file

	# use the audio file as the audio source	 
	r = sr.Recognizer()
	 
	with sr.AudioFile(AUDIO_FILE) as source:
	    #reads the audio file. Here we use record instead of
	    #listen
	    audio = r.record(source)  
	 
	try:
	    output = r.recognize_google(audio)
	    print("The audio file contains: " + output)
	    # f = open('output.txt', 'w')
	    # f.write(output)
	    # f.close()

	    if file_extension == '.mp3':
	    	os.remove("../data/converted.wav")
	 
	except sr.UnknownValueError:
	    print("Google Speech Recognition could not understand audio")
	 
	except sr.RequestError as e:
	    print("Could not request results from Google Speech Recognition service; {0}".format(e))


if __name__ == '__main__':
    # check input output file
    if (len(sys.argv) == 1):
        stt_online()
    else:
    	input_audio_file = sys.argv[1]
    	# print input_audio_file
    	stt_offline(input_audio_file)
