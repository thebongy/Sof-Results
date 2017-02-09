import requests
import threading
from time import sleep,time

#God first

std_code = raw_input('Enter the school code: ')
std_class = raw_input('Enter the class: ').zfill(2)
olymp = raw_input("Choose an olympiad: ")

section_end = ord(raw_input("Enter the last section: ").upper())
sections = [chr(ch) for ch in range(65,section_end+1)]

limit = 50*len(sections)
conc = 50
URL = 'http://results.sofworld.org/results'
rolls=[]
for i in range(1,limit+1):
        for j in sections:
                rolls.append([i,j])
                
##rolls = [str(i).zfill(3) for i in range(1,limit+1)]
olymps = {'NCO':'n','IMO':'im','NSO':'z','ISKO':'s','ICSO':'m'}

results = []
removed = []
if olymp in olymps:
	olymp = olymps[olymp]
else:
	olymp = 'n'

fields = ['Student Name:','School Rank:','Roll No:','International Rank:','Qualified For 2nd Level:']
data = {'form_id': 'ac_result_cards_enter_rollid_form', 'rollid1': std_code, 'rollid3': sections[0], 'rollid2': std_class, 'olympiad_selected': olymp,'rollid4':'temp'}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def get_roll_result():
        while len(rolls) != 0:
                idn = rolls.pop(0)
                payload = dict(data)
                payload['rollid4'] = str(idn[0]).zfill(3)
                success=False
		

                while not success:
                        payload['rollid3'] = idn[1]
                        try:
                                r = requests.post(URL, data=payload, headers=headers,timeout=3)
                                success=True
                        except:
                                success = False
                                
                if r.text.find('wrong')==-1:
                        std_data = []
                        for field in fields:
                                search = '<label>'+field+'</label></td><td>'
                                loc_ns = r.text.find(search) + len(search)
                                loc_ne = r.text.find('</td>',loc_ns)
                                std_data.append(r.text[loc_ns:loc_ne])
                        results.append(std_data)

                        section_index = sections.index(idn[1])
                        loop = False
                        for i in sections[:section_index]:
                                if i not in removed:
                                        loop = True
                                        removed.append(i)
                        if loop:
                                for i in rolls:
                                        if (ord(idn[1])-ord(i[1]))*(idn[0]-i[0])<0:
                                                try:
                                                        rolls.remove(i)
                                                        print i
                                                except:
                                                        stuff=1
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


def filterrolls(x):
        if x[1].isdigit():
                return int(x[1])
        else:
                return x[1]


results.sort(key=filterrolls)
formatting = '%30s %15s %18s %23s %8s'
print formatting % tuple(fields)
for result in results:
	print formatting % tuple(result)
