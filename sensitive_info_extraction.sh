# !/bin/bash

gsutil cp $1 gs://im-audio-files
a=$1
b=$(basename $a)
c=gs://im-audio-files
d=$c/$b

python google-speech-api/cloud-client/transcribe_async.py $d
python regex-extraction.py google-speech-api/cloud-client/temp.txt

gsutil rm $d