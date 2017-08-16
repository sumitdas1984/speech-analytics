#!/usr/bin/ python
 
import sys
import os
import re
# import pocketsphinx
from pocketsphinx.pocketsphinx import *
 
if __name__ == "__main__":
 
	# hmdir = "/usr/share/pocketsphinx/model/hmm/wsj1"
	# lmdir = "/usr/share/pocketsphinx/model/lm/wsj/wlist5o.3e-7.vp.tg.lm.DMP"
	# dictd = "/usr/share/pocketsphinx/model/lm/wsj/wlist5o.dic"

	# hmdir = "/usr/share/pocketsphinx/model/hmm"
	# lmdir = "/usr/share/pocketsphinx/model/lm/en-70k-0.1.lm.dmp"
	# dictd = "/usr/share/pocketsphinx/model/dictd/cmu07a.dic"

	# Paths
	BASE_PATH = os.path.dirname(os.path.realpath(__file__))
	HMDIR = os.path.join(BASE_PATH, "hmm")
	LMDIR = os.path.join(BASE_PATH, "lm/en-70k-0.1.lm.dmp")
	DICTD = os.path.join(BASE_PATH, "dict/cmu07a.dic")

	wavfile = sys.argv[1]

	# config = pocketsphinx.Decoder.default_config()
	config = Decoder.default_config()
	config.set_string('-hmm', HMDIR)
	config.set_string('-lm', LMDIR)
	config.set_string('-dict', DICTD) 

	# speech_rec = pocketsphinx.Decoder(config)
	speech_rec = Decoder(config)

	# # speechRec = pocketsphinx.Decoder(hmm = hmdir, lm = lmdir, dict = dictd)
	# wavFile = open(wavfile,'rb')
	# # speech_rec.decode_raw(wavFile)
	# speech_rec.process_raw(wavFile, False, False)
	# result = speech_rec.get_hyp()

	# print result

	# r = decode_phrase(speech_rec, wavfile)
	# print "DETECTED: ",r

	speech_rec.start_utt()
	stream = open(wavfile, "rb")
	while True:
		buf = stream.read(1024)
		if buf:
			speech_rec.process_raw(buf, False, False)
		else:
			break
	speech_rec.end_utt()
	framerate = 100
	words = []
	# [words.append(seg.word) for seg in speech_rec.seg()]
	speech_start_frame = 0
	for i, seg in enumerate(speech_rec.seg()) :
		if i == 0 :
			speech_start_frame = seg.start_frame/framerate

		pair = (seg.word,str(seg.start_frame/framerate - speech_start_frame))
		# print(pair)
		words.append(pair)		
	# print "DETECTED: ",words

	text = ''
	text_ts = ''
	for w, t in words :
		if not re.search('<s>|</s>|<sil>|[NOISE]|[SPEECH]',w) :
			w = re.sub('\(\d\)','',w)
			text = text + ' ' + w
			text_ts = text_ts + ' ' + w + '##' + t
	# print(text)
	print(text_ts)

    # f = open('sphinx-speech-api/temp.txt', 'w')
	f = open('temp.txt', 'w')
	f.write(text)
	f.close()
