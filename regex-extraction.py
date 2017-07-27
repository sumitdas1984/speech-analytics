import sys
import re

def normalize(text):
	text_norm = ''
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
	# ssn_regex = re.compile(r'\b\d{3}-\d{2}-\d{4}\b|\b\d{3}\s*\d{2}\s*\d{4}\b|\b\d{9}\b')
	ssn_regex = re.compile(r'\b\d{3}-\d{2}-\d{4}\b|\b\d{9}\b')
	f=re.findall(ssn_regex, text)
	return f

if __name__ == "__main__":

# 	text = "the card 5610-5910-8101-8250 is sent to John. the other card is 5610 6910 8101 1234" 

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

		print('::Sensitive Info::')
		if len(cc_list) != 0:
			print('CC: '+str(cc_list))
		if len(ssn_list) != 0:
			print('SSN: '+str(ssn_list))
