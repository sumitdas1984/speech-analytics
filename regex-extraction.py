import re

# def cfor_cc(text):
# 	cc_regex = r"([0-9]{4}-){3}[0-9]{4}|([0-9]{4}\s){3}[0-9]{4}|[0-9]{16}" 
# 	cc_list = []
# 	for m in re.finditer(cc_regex, text):
# 		cc_list.append(m.group())
# 	return cc_list

def cfor_cc(text):
	cc_regex = re.compile(r'\d{4}-\d{4}-\d{4}-\d{4}|\d{4}\s*\d{4}\s*\d{4}\s*\d{4}|\d{16}')
	f=re.findall(cc_regex, text)
	return f

def cfor_ssn(text):
 	ssn_regex = re.compile(r'\d{3}-\d{2}-\d{4}|\d{3}\s*\d{2}\s*\d{4}|\d{9}')
	f=re.findall(ssn_regex, text)
	return f


if __name__ == "__main__":

# 	text = "the card 5610-5910-8101-8250 is sent to John. the other card is 5610 6910 8101 1234" 

	with open("sample.txt","r") as fh:
	    for line in fh.readlines():
	    	print(line)
	    	cc_list = cfor_cc(line)
	        ssn_list = cfor_ssn(line)

	        if len(cc_list) != 0:
	            print('CC: '+str(cc_list))
	        if len(ssn_list) != 0:
	            print('SSN: '+str(ssn_list))
