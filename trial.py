import requests

std_code = raw_input('Enter the school code')
std_class = raw_input('Enter the class')
olymp = raw_input('Enter the NCO,IMO,NSO,IEO,etc.')


olymps = {'NCO':'n'}


if olymp in olymps:
	olymp = olymps[olymp]
else:
	olymp = 'n'

	
data = {'form_id': 'ac_result_cards_enter_rollid_form', 'rollid1': std_code, 'rollid3': 'A', 'rollid2': std_class, 'rollid4': '001', 'olympiad_selected': olymp}
section_start = 65
section_end = 67
roll_limit = 20


count=0
i = 1
while i<=roll_limit:
	current = str(i).zfill(3)
	print data['rollid3']
	data['rollid4'] = current
	r = requests.post('http://results.sofworld.org/results',data=data)
	if r.text.find('wrong') == -1:
		search = '<label>Student Name:</label></td><td>'
		loc_ns = r.text.find(search) + len(search)
		loc_ne = r.text.find('</td>',loc_ns)
		print data['rollid4']
		count = 0
	else:
		count+=1
	i+=1
	rollid3=data['rollid3']
	if count == 11:
		data['rollid3']=chr(ord(rollid3)+1)
		i-=11
		count = 0
		if ord(rollid3) == section_end:
			break
	
