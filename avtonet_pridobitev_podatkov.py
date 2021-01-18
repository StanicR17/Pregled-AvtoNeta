import requests
from bs4 import BeautifulSoup
import time
import re
import json

def ustvari_h_refe():
    tapravi_h_refi = []
    url = 'https://www.avto.net/Ads/results.asp?znamka=&model=&modelID=&tip=&znamka2=&model2=&tip2=&znamka3=&model3=&tip3=&cenaMin=0&cenaMax=999999&letnikMin=0&letnikMax=2090&bencin=0&starost2=999&oblika=&ccmMin=0&ccmMax=99999&mocMin=&mocMax=&kmMin=0&kmMax=9999999&kwMin=0&kwMax=999&motortakt=&motorvalji=&lokacija=0&sirina=&dolzina=&dolzinaMIN=&dolzinaMAX=&nosilnostMIN=&nosilnostMAX=&lezisc=&presek=&premer=&col=&vijakov=&EToznaka=&vozilo=&airbag=&barva=&barvaint=&EQ1=1000000000&EQ2=1000000000&EQ3=1000000000&EQ4=100000000&EQ5=1000000000&EQ6=1000000000&EQ7=1110100120&EQ8=1010000001&EQ9=100000000&KAT=1010000000&PIA=&PIAzero=&PSLO=&akcija=&paketgarancije=0&broker=&prikazkategorije=&kategorija=&zaloga=10&arhiv=&presort=&tipsort=&stran='
    for i in range(1,22):
        print(i)
        a = url+str(i)
        r =requests.get(a, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'})
        rhtml = BeautifulSoup(r.text, 'html.parser')
        vsi_h_refi = rhtml.find_all("a")
        for i in vsi_h_refi:
            if 'class="stretched-link"' in str(i) and "www.avto.net" not in str(i):
                string= str(i)
                string = "https://www.avto.net" + string[34:string.index(";")]
                tapravi_h_refi.append(string)
                print(string)
    return tapravi_h_refi



def ustvari_json(sez):
    seznam_dict=[]
    print("begin timer")
    count = 0
    n = len(sez)
    for j in sez:
        print(j)
        seznam =[]
        print(count)
        vsi_td_ji = []
        rr =requests.get(str(j), headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'})
        rrhtml = BeautifulSoup(rr.text, 'html.parser', from_encoding="windows-1250")
        vsi_tr_ji = rrhtml.find_all("tr")
        tr_ji = vsi_tr_ji[2:13]
        if(len(tr_ji) != 4):
            cena = rrhtml.find('p', attrs={'class' : 'h2 font-weight-bold align-middle py-4 mb-0'})
            count += 1
            if cena != None:
                cena = str(cena)
                if(str(cena).find(".") == -1):
                    cena = cena[60:64]
                else:   
                    cena = cena[60:str(cena).find(".")+4]
                    cena = int(cena[0:str(cena).find(".")]+ cena[(str(cena).find(".")+1):])
            if cena == '' or cena == None:
                cena = rrhtml.find('p', attrs={'class' : 'h2 font-weight-bold text-danger mb-3'})
                if cena != None:
                    cena = re.findall(r'\d{1,}.\d{1,}',str(cena))
                    cena = str(cena[0])
                    print(cena)
                    if len(cena) > 3:
                        d = len(cena)
                        cena= cena[:(d-4)]+cena[(d-3):]        
            Znamka_in_tip =  rrhtml.title
            Znamka_in_tip = str(Znamka_in_tip)[7:(len(Znamka_in_tip)-23)]
            Znamka = Znamka_in_tip.split(' ', 1)[0]
            Tip = Znamka_in_tip[(len(Znamka)+1):]
            prva_registracija = re.findall(r'\d{1,4}',str(tr_ji[1]))
            leto_proizvodnje = re.findall(r'\d{4,4}',str(tr_ji[2]))
            if ((len(re.findall("Leto",str(tr_ji[2]))) == 0) and (len(re.findall("Motor",str(tr_ji[2]))) == 0)):
                tr_ji.insert(2, '')
                leto_proizvodnje = "null"
            #tuki vmes se lahko certifikat prkaze
            if((len(re.findall(r'\d{1,}',str(tr_ji[3])))>1) and(len(re.findall("Motor",str(tr_ji[2]))) == 0)):
                del tr_ji[3]
            prevozeni_kilometri =  re.findall(r'\d{1,}',str(tr_ji[3]))
            if((len(re.findall(r'\d{1,4}',str(tr_ji[4]))) != 2) and (len(re.findall("Motor",str(tr_ji[2]))) == 0)):
                tr_ji.insert(4, '')
            Motor = re.findall(r'\d{1,}',str(tr_ji[5]))
            stevilo_vrat = re.findall(r'\d{1,}',str(tr_ji[9]))
            Gorivo = re.findall('<td>\s*(.*?)\s*</td>',str(tr_ji[6]))
            Menjalnik = re.findall('<td>\s*(.*?)\s*</td>',str(tr_ji[7]))
            Starost = re.findall('<td>\s*(.*?)\s*</td>',str(tr_ji[0]))
            starost=[]
            if len(re.findall("rabljeno", str(Starost[0]))) == 1:
                starost.append("rabljeno")
            if len(re.findall("garancijo", str(Starost[0]))) == 1:
                starost.append("ima garancijo")
            if len(re.findall("jamstvo", str(Starost[0]))) == 1:
                starost.append("ima jamstvo")
            if len(re.findall("novo", str(Starost[0]))) == 1:
                starost.append("novo")
            if((len(re.findall("Prevoeni km",str(tr_ji[1]))) == 1) and (len(re.findall("Motor",str(tr_ji[2]))) == 1)):
                Motor = re.findall(r'\d{1,}',str(tr_ji[2]))
                stevilo_vrat = re.findall(r'\d{1,}',str(tr_ji[6]))
                Gorivo = re.findall('<td>\s*(.*?)\s*</td>',str(tr_ji[3]))
                Menjalnik = re.findall('<td>\s*(.*?)\s*</td>',str(tr_ji[4]))
                prevozeni_kilometri =  re.findall(r'\d{1,}',str(tr_ji[1]))
                prva_registracija = []
                leto_proizvodnje = ["2020"]

                
            vsi_enoelementni = [leto_proizvodnje,prevozeni_kilometri,stevilo_vrat,Gorivo,Menjalnik,starost]
            for e in range(0,len(vsi_enoelementni)):
                if(len(vsi_enoelementni[e])==0):
                    e =[""]
            if(Menjalnik[0] != "5 vr."):        
                thisdict = {
                    "znamka":Znamka,
                    "tip" : Tip,
                    "cena" : cena,
                    "prva registracija" : prva_registracija,
                    "leto prozivodnje": leto_proizvodnje,
                    "prevozeni kilometri" :prevozeni_kilometri,
                    "KM; kW; ccm" : Motor,
                    "stevilo vrat":stevilo_vrat,
                    "gorivo":Gorivo,
                    "menjalnik":Menjalnik,
                    "starost": starost
                    }                  
                seznam_dict.append(thisdict.copy())
                if count % 10000000 == 0:
                    cas1 =time.time()
                    cas2= time.time()
                    l=0
                    while cas2-cas1 < 60:
                        print("2 min pavza")
                        cas2= time.time()
                        l +=1
                        if l % 1000000 == 0:
                            print("se traja pavza")
    return seznam_dict
sez =ustvari_h_refe()
p = ustvari_json(sez)
p = json.dumps(p)   
with open("avtoneadsadsadsas4t.json",'w', encoding='windows-1250') as f:
	f.write(p)
	f.close()
