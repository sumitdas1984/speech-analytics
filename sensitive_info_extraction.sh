# !/bin/bash

if [ "$2" = "google" ]
then
    echo "transcription:: google based"

	path=$1
	xpath=${path%/*}
	xbase=${path##*/}
	xfext=${xbase##*.}
	xpref=${xbase%.*}
	# echo $xpath
	# echo $xbase
	# echo $xfext
	# echo $xpref

	wav_file=''
	flac_file=''

	if [ "$xfext" = "nmf" ]
	then
		# for input audio files as .nmf file
		python nmf_converter.py $1
		f_ending=_stream0.wav
		wav_file=$xpath/$xpref$f_ending
		flac_ext=.flac
		wav_file=$xpath/$xpref$f_ending
		flac_file=$xpath/$xpref$flac_ext
		# ffmpeg -i $wav_file -af aformat=s32:16000 -ac 1 $flac_file
		ffmpeg -i $wav_file -ar 16000 $flac_file
		rm $wav_file

		path=$flac_file

		xpath=${path%/*}
		xbase=${path##*/}
		xfext=${xbase##*.}
		xpref=${xbase%.*}
	fi

	# for input audio files as .flac file
	gsutil cp $path gs://im-audio-files

	gs_path=gs://im-audio-files/$xbase
	# echo $gs_path

	python google-speech-api/transcribe_asynchronous.py $gs_path
	printf '\n'

	python regex-extraction.py temp.txt word_timestamp_info.txt
	printf '\n'

	# # # gsutil rm $gs_path

	modified_file="$xpath"/"$xpref"_modified."$xfext"
	# cp $1 "$xpath"/"$xpref"_modified."$xfext"
	cp $path $modified_file

	while read line
	do
	# echo $line
	start_time="$(cut -d'#' -f3 <<<$line)"
	end_time="$(cut -d'#' -f4 <<<$line)"
	# echo $start_time
	# echo $end_time
	# ffmpeg "$1" -af "volume=enable='between(t,"$start_time","$end_time")':volume=0" $1
	speech_file=$modified_file
	speech_file_mod=$xpath/temp.flac
	ffmpeg -i $speech_file -af "volume=enable='between(t,$start_time,$end_time)':volume=0" $speech_file_mod
	rm $speech_file
	mv $speech_file_mod $speech_file
	done < sensitive_info.txt

	rm temp.txt word_timestamp_info.txt sensitive_info.txt
	rm $flac_file
	

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