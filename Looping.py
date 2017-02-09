import requests
import threading
from time import sleep,time
sections = ['A','B']
for rishit in range(10):
        for apurva in range(100,150,10):
                std_code = 'KA0138'
                std_class = 11
                olymp = 'NSO'
                limit = 120
                conc = apurva
                URL = 'http://results.sofworld.org/results'
                rolls = [str(i).zfill(3) for i in range(1,limit+1)]
                olymps = {'NCO':'n','IMO':'im','NSO':'z','ISKO':'s','ICSO':'m'}

                results = []
                if olymp in olymps:
                        olymp = olymps[olymp]
                else:
                        olymp = 'n'

                fields = ['Student Name:','School Rank:','Roll No:','International Rank:','Qualified For 2nd Level:']

                data = {'form_id': 'ac_result_cards_enter_rollid_form', 'rollid1': std_code, 'rollid3': sections[0], 'rollid2': std_class, 'olympiad_selected': olymp}
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

                def get_roll_result():
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
                                                std_data = []
                                                for field in fields:
                                                        search = '<label>'+field+'</label></td><td>'
                                                        loc_ns = r.text.find(search) + len(search)
                                                        loc_ne = r.text.find('</td>',loc_ns)
                                                        std_data.append(r.text[loc_ns:loc_ne])
                                                results.append(std_data)
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
                print "Time: ",time()-t
                print "Sections: ",sections
		print "Threads: ",conc
		print

##                def filterrolls(x):
##                        if x[1].isdigit():
##                                return int(x[1])
##                        else:
##                                return x[1]
##
##                results.sort(key=filterrolls)
##                formatting = '%40s%3s%20s%7s%4s'
##                print formatting % tuple(fields)
##                for result in results:
##                        print formatting % tuple(result)
        sections.append(chr(ord(sections[-1])+1))
