import requests
import threading
from time import sleep
std_code = 'KA0138'
std_class = 11
olymp = 'NCO'
sections = ['A','B','C','D']
limit = 50
conc = 10
URL = 'http://results.sofworld.org/results'
rolls = [str(i).zfill(3) for i in range(limit)]
olymps = {'NCO':'n'}

results = []
if olymp in olymps:
	olymp = olymps[olymp]
else:
	olymp = 'n'


	
data = {'form_id': 'ac_result_cards_enter_rollid_form', 'rollid1': std_code, 'rollid3': sections[0], 'rollid2': std_class, 'olympiad_selected': olymp}


def get_roll_result(initial=None):
	while len(rolls) != 0:
		id4 = rolls.pop()
		payload = dict(data)
		payload['rollid4'] = id4
		success = False
		for section in sections:
			while not success:
				payload['rollid3'] = section
				try:
					r = requests.post(URL, data=payload, timeout=5)
					success=True
				except:
					success = False
			if r.text.find('wrong') == -1:
				results.append((id4,section))
				break

def main():
	threads = []
	for i in range(conc):
		x = threading.Thread(target=get_roll_result)
		x.start()
		threads.append(x)
	
	
	
	for thread in threads:
		thread.join()

main()

for result in results:
	print result