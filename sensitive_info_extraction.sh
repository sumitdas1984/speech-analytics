# !/bin/bash

if [ "$2" = "google" ]
then
    echo "transcription:: google based"
	gsutil cp $1 gs://im-audio-files
	a=$1
	b=$(basename $a)
	c=gs://im-audio-files
	d=$c/$b
	# printf '\n'

	python google-speech-api/cloud-client/transcribe_async.py $d
	printf '\n'

	python regex-extraction.py temp.txt
	printf '\n'

	gsutil rm $d
elif [ "$2" = "sphinx" ]
	then
    echo "transcription:: sphinx based"
	python sphinx-speech-api/pythonPocketSphinxTest.py $1
	printf '\n'

	python regex-extraction.py temp.txt
	printf '\n'
else
	echo "transcription:: out of scope"	
fi