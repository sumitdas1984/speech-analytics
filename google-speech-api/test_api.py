#!/usr/bin/env python
# Requires PyAudio and PySpeech.

import requests
import base64
import json

# encoding audio file with Base64 (~200KB, 15 secs)
with open('../data/Power_English_Update.mp3', 'rb') as speech:
    speech_content = base64.b64encode(speech.read())

payload = { 
    'initialRequest': {
        'encoding': 'FLAC',
        'sampleRate': 16000,
    },
    'audioRequest': {
        'content': speech_content.decode('UTF-8'),
    },
}

# POST request to Google Speech API
r = requests.post(url, data=json.dumps(payload))