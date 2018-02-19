# speech-analytics

Tools need to be installed
--------------------------
1. google-cloud-speech (it's a python library. install using pip)
2. ffmpeg (install this as linux program)
3. gsutils (install using gcloud. after installing gcloud configure gcloud using 'gcloud init')

Configuration
-------------
Need to set evironment variable GOOGLE_APPLICATION_CREDENTIALS to the path of google-speech-api/speechapi-6a5961bb84d3.json

Input Data
-----------
Create 'data' directory in repo folder and put input audio file in .flac format, 16000 Hz and Mono channel format

Running sensitive information extraction script
-----------------------------------------------
./sensitive_info_extraction.sh data/sample_recording.flac google

Output reducted speech file
---------------------------
sample_recording_modified.flac



Creating required input speech file
-----------------------------------
For speech recording
audacity
format saved .wav

convert the .wav file to .flac format (16000Hz and mono channel)
ffmpeg -i in.wav -ar 16000 -ac 1 out.flac

move the .flac file to data directory

