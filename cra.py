import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

def alldata(datalist):
    spacelist = datalist.find_all("td",{"class":"local first"})
    titlelist = datalist.find_all("td",{"class":"title"})
    timedatalist = datalist.find_all("td",{"class":"data"})
    paylist = datalist.find_all("td",{"class":"pay"})
    regdatalist = datalist.find_all("td",{"class":"regData last"})

    bigdatalist = []
    spacedatalist = []
    titledatalist = []
    timedatadatalist = []
    paydatalist = []
    regdatedatalist = []
    for space in spacelist:
        spacedatalist.append(space.text)
    for title in titlelist:
        titledatalist.append(title.find("span").text)
    for timedata in timedatalist:
        timedatadatalist.append(timedata.text)

    for pay in paylist:
        moneylist = pay.find_all("span")
        moneyback = ""
        for money in moneylist:
            moneyback += money.text
        paydatalist.append(moneyback)

    for regdate in regdatalist:
        regdatedatalist.append(regdata.text)

    for go in range(len(spacelist)):
        smalldata =[]
        smalldata.append(spacedatalist[go].replace('\xa0',''))
        smalldata.append(titledatalist[go])
        smalldata.append(timedatadatalist[go])
        smalldata.append(paydatalist[go])
        smalldata.append(regdatedatalist[go])
        bigdatalist.append(smalldata)
    return bigdatalist

def workjob(work_url):
    result = requests.get(work_url)
    soup = BeautifulSoup(result.text,"html.parser")
    datalist = soup.find("div",{"class":"goodList goodsJob"}).find("table",{"cellspacing":{"0"}}).find("tbody")

    try:
        return alldata(datalist)
    except:
        pass

def insidejob(inside_url,company):
    print(inside_url)
    result = requests.get(inside_url)
    soup = BeautifulSoup(result.text,"html".parser)
    listcount = int(soup.find("div",{"id":"NormalInfo"}).find("p").find("strong").text.replace(",",""))
    bigdataforcvs = []
    if listcount % 50 == 0:
        pagecount = int(listcount / 50)
    else:
        pagecount = 1 + int(listcount / 50)
    for i in range(1,pagecount+1):
        try:
            pageurl = f"{inside_url}job/brand/?page={i}&pagesize=50&areacd=&workaddr1=&workaddr2=&jobkind=&jobkindsub=&jobkindmulti=&gendercd=&agelimitcd=&agelimit=0&worktime=&weekdays=&searchterm=&paycd=&paystart=&payend=&workperiodcd=&workstartdt=&workenddt=&workchkyn=&workweekcd=&targetcd=&streetunicd=&streetstationcd=&unicd=&schnm=&schtext=&orderby=freeorder&acceptmethod=&eleccontract=&careercd=%20&lastschoolcd=&welfarecd=&careercdunrelated=&lastschoolcdunrelated=&strAreaMulti=&genderunrelated=&special=&hiretypecd=&totalCount={listcount}"
            bigdataforcvs.append(workjob(pageurl))
            print(f"크롤링 중 Page({i}/{pagecount})")
        except:
            pageurl = f"{inside_url}?page={i}&pagesize=50&areacd=&workaddr1=&workaddr2=&jobkind=&jobkindsub=&jobkindmulti=&gendercd=&agelimitcd=&agelimit=0&worktime=&weekdays=&searchterm=&paycd=&paystart=&payend=&workperiodcd=&workstartdt=&workenddt=&workchkyn=&workweekcd=&targetcd=&streetunicd=&streetstationcd=&unicd=&schnm=providercd&schtext=BP4,BP5,BP6,BP7&orederby=freeorder&acceptmethod=&eleccontract=&totalCount={listcount}&viewtype="  
            bigdataforcvs.append(workjob(pageurl))
            print(f"크롤링 중 Page({i}/{pagecount})")
        save(bigdataforcvs,company)

def save(bigdataforcvs,company):
    file = open(f"day7/csv/{company}.csv",mode="w")
    writer = csv.writer(file)
    writer.writerow(["place","title","time","pay","data"])

    for pages in bigdataforcvs:
        for jobs in pages:
            writer.writerow(jobs)
    return

def start_over():
    result = requests.get(alba_url)
    soup = BeautifulSoup(result.text,"html.parser")
    inside = soup.find('div',{"id":"MainSuperBrand"}).find("url",{"class":"goodsBox"}).find_all("a",{"class":"goodsBox-info"})
    for joburl in inside:
        company = joburl.find("span",{"class":"company"}).text
        print(company)
        insidejob(joburl["href"],company)
        print("csv 저장완료")        