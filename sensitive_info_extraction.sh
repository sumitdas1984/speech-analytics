# !/bin/bash

if [ "$2" = "google" ]
then
    echo "google-speech-api"
	gsutil cp $1 gs://im-audio-files
	a=$1
	b=$(basename $a)
	c=gs://im-audio-files
	d=$c/$b
	# printf '\n'

	python google-speech-api/cloud-client/transcribe_async.py $d
	printf '\n'

	python regex-extraction.py google-speech-api/cloud-client/temp.txt
	printf '\n'

	gsutil rm $d
else
    echo "sphinx-speech-api"
	python sphinx-speech-api/pythonPocketSphinxTest.py $1
	printf '\n'

	python regex-extraction.py temp.txt
	printf '\n'
fi

# gsutil cp $1 gs://im-audio-files
# a=$1
# b=$(basename $a)
# c=gs://im-audio-files
# d=$c/$b
# # printf '\n'

# python google-speech-api/cloud-client/transcribe_async.py $d
# printf '\n'

# python regex-extraction.py google-speech-api/cloud-client/temp.txt
# printf '\n'

# gsutil rm $d