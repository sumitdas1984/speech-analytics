import sys
import re

def normalize(text):
	text_norm = ''
	text = re.sub(r'\.', r'', text)
	# a = re.split(r"[\s]+", text)
	a = re.split(r"[\s-]+", text)
	for w in a:
		w_n = ''
		if w == 'zero': w_n = '0'
		elif w == 'one': w_n = '1'
		elif w == 'two': w_n = '2'
		elif w == 'three': w_n = '3'
		elif w == 'four': w_n = '4'
		elif w == 'five': w_n = '5'
		elif w == 'six': w_n = '6'
		elif w == 'seven': w_n = '7'
		elif w == 'eight': w_n = '8'
		elif w == 'nine': w_n = '9'
		else : w_n = w
		text_norm += ' ' + w_n
	text_norm = re.sub(r'(\d+)\s+(?=\d)',r'\1', text_norm)
	return text_norm

def cfor_cc(text):
	# cc_regex = re.compile(r'\d{4}-\d{4}-\d{4}-\d{4}|\d{4}\s*\d{4}\s*\d{4}\s*\d{4}|\d{16}')
	cc_regex = re.compile(r'\b\d{4}-\d{4}-\d{4}-\d{4}\b|\b\d{16}\b')
	# cc_regex = re.compile(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})\b')
	f=re.findall(cc_regex, text)
	return f

def cfor_ssn(text):
 	# ssn_regex = re.compile(r'\d{3}-\d{2}-\d{4}|\d{3}\s*\d{2}\s*\d{4}|\d{9}')
	ssn_regex = re.compile(r'\b\d{3}-\d{2}-\d{4}\b|\b\d{9}\b')
	f=re.findall(ssn_regex, text)
	return f

def cfor_ph(text):
	ph_regex = re.compile(r'\b\d{10}\b')
	f=re.findall(ph_regex, text)
	return f

def word_index(text, word, type):
	approx_start_index = text.split().index(word) + 1
	if type == 'CC' :
		approx_end_index = approx_start_index + 4
	elif type == 'SSN' :
		approx_end_index = approx_start_index + 3
	elif type == 'PH' :
		approx_end_index = approx_start_index + 3
	else :
		approx_end_index = approx_start_index + 1

	# print(word + ': ' + str(approx_start_index) + ',' + str(approx_end_index))
	return (approx_start_index,approx_end_index)

def sensitive_info_index(text, cc_list, ssn_list, ph_list, tts_list) :

	# print cc_list
	# print ssn_list
	# print ph_list

	token_start_time_list = []
	token_end_time_list = []
	for tts in tts_list:
		tts_pair = tts.split(',')
		token_start_time_list.append(tts_pair[0])
		token_end_time_list.append(tts_pair[1]) 
	# print(token_start_time_list)
	# print(token_end_time_list)


	token_list = text.split()
	cc_count = 0
	ssn_count = 0
	ph_count = 0
	sensitive_info_list = []
	for index, token in enumerate(token_list) :
		if token in cc_list :
			token_type = 'CC'
			token_start_index = (index+1) + cc_count*4 + ssn_count*3 + ph_count*3
			token_end_index = token_start_index + 4
			cc_count = cc_count + 1
			# print 'token_start_index: '+str(token_start_index)
			# print 'token_end_index: '+str(token_end_index)
			# sensitive_info_line = token_type + '#' + token + '#' + str(token_start_index) + '#' + str(token_end_index)
			sensitive_info_line = token_type + '#' + token + '#' + str(token_start_time_list[token_start_index]) + '#' + str(token_end_time_list[token_end_index])
			# print 'sensitive_info_line: '+sensitive_info_line
			sensitive_info_list.append(sensitive_info_line)
		elif token in ssn_list :
			token_type = 'SSN'
			token_start_index = (index+1) + cc_count*4 + ssn_count*3 + ph_count*3
			token_end_index = token_start_index + 3
			ssn_count = ssn_count + 1
			sensitive_info_line = token_type + '#' + token + '#' + str(token_start_time_list[token_start_index]) + '#' + str(token_end_time_list[token_end_index])
			sensitive_info_list.append(sensitive_info_line)
		elif token in ph_list :
			token_type = 'PH'
			token_start_index = (index+1) + cc_count*4 + ssn_count*3 + ph_count*3
			token_end_index = token_start_index + 3
			ph_count = ph_count + 1
			sensitive_info_line = token_type + '#' + token + '#' + str(token_start_time_list[token_start_index]) + '#' + str(token_end_time_list[token_end_index])
			sensitive_info_list.append(sensitive_info_line)
	
	return sensitive_info_list


if __name__ == "__main__":

	# text = "the card 56 10 59 1081 018250 is sent to John. His SSN is 821 935 117. My register mobile number is 8983 934 849." 
	# text = "the card 56 10 59 1081 018250 is sent to John. His SSN is 821 935 117." 

	# check input output file
	if (len(sys.argv) == 1):
		print("input file required...")
	else:
		input_file = open(sys.argv[1], 'r')
		text = input_file.read()
		print('::STT output::')
		print(text)
		text = normalize(text)
		# print(text)
		cc_list = cfor_cc(text)
		ssn_list = cfor_ssn(text)
		ph_list = cfor_ph(text)

		wts_list_source = open(sys.argv[2], 'r').readlines()
		# print(wts_list_source)
		wts_list = []
		for wts in wts_list_source:
			wts = re.sub('\n','',wts)
			wts_list.append(wts)

		print('\n')
		print('::Sensitive Info::')
		sensitive_info_list = sensitive_info_index(text, cc_list, ssn_list, ph_list, wts_list)
		print(sensitive_info_list)

		f_sensitive_info = open('sensitive_info.txt', 'w')
		# f_sensitive_info.write('\n'.join(sensitive_info_list))
		for sensitive_info_line in sensitive_info_list:
			f_sensitive_info.write(sensitive_info_line + '\n')
		f_sensitive_info.close()


		# if len(cc_list) != 0:
		# 	print('CC')
		# 	for cc in cc_list:
		# 		index = word_index(text, cc, 'CC')
		# 		print(cc + '\t' + str(index))
		# if len(ssn_list) != 0:
		# 	print('SSN')
		# 	for ssn in ssn_list:
		# 		index = word_index(text, ssn, 'SSN')
		# 		print(ssn + '\t' + str(index))
		# if len(ph_list) != 0:
		# 	print('PH')
		# 	for ph in ph_list:
		# 		index = word_index(text, ph, 'PH')
		# 		print(ph + '\t' + str(index))
