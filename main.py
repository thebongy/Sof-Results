import requests
import threading
from time import sleep,time
std_code = 'KA0138'
std_class = 11
olymp = 'NCO'
sections = ['A','B','C','D']
limit = 100
conc = 30
URL = 'http://results.sofworld.org/results'
rolls = [str(i).zfill(3) for i in range(1,limit+1)]
olymps = {'NCO':'n'}

results = []
if olymp in olymps:
	olymp = olymps[olymp]
else:
	olymp = 'n'



data = {'form_id': 'ac_result_cards_enter_rollid_form', 'rollid1': std_code, 'rollid3': sections[0], 'rollid2': std_class, 'olympiad_selected': olymp}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def get_roll_result(initial=None):
	while len(rolls) != 0:
		id4 = rolls.pop()
		payload = dict(data)
		payload['rollid4'] = id4
		success=False
		for section in sections:
			while not success:
				payload['rollid3'] = section
				try:
					r = requests.post(URL, data=payload, headers=headers,timeout=3)
					success=True
				except:
					success = False
			if r.text.find('wrong') == -1:
				results.append((id4,section))
				break
			else:
				success=False

def main():
	threads = []
	for i in range(conc):
		x = threading.Thread(target=get_roll_result)
		x.start()
		threads.append(x)



	for thread in threads:
		thread.join()


t=time()
main()
print time()-t

for result in results:
	print result
