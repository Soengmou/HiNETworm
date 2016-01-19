#!/usr/bin/python
import sys
import os
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
from dateutil import rrule
import zipfile
import numpy as np

url_login='https://hinetwww11.bosai.go.jp/auth/?LANG=en'
url_request='https://hinetwww11.bosai.go.jp/auth/download/cont/cont_request.php'
url_status='https://hinetwww11.bosai.go.jp/auth/download/cont/cont_status.php?LANG=en&page=1'

#code_list=[]
user="username"
passwd="password"


def cont_request(org,net,startTime,span,arc,volc):
#    payload = {
#        'org1': org,
#        'org2': net,
#        'year': startTime.strftime("%Y"),
#        'month': startTime.strftime("%m"),
#        'day': startTime.strftime("%d"),
#        'hour':startTime.strftime("%H"),
#        'min': startTime.strftime("%M"),
#        'span': str(span),
#        'arc': arc,
#        'size': '93680',
#        'LANG': 'en',
#        'rn': str(int((datetime.now() - datetime(1970, 1, 1)).total_seconds()))
#    }
#    if len(volc) > 1:
#        payload['volc'] = volc
    year = startTime.strftime("%Y")
    month = startTime.strftime("%m")
    day = startTime.strftime("%d")
    hour = startTime.strftime("%H")
    minu = startTime.strftime("%M")
    size = '93680'
    lang = 'en'
    rn = str(int((datetime.now() - datetime(1970, 1, 1)).total_seconds()))

    data = {'auth_un': user, 'auth_pw':passwd }
    s = requests.Session()
    s = requests.Session()
    url = url_request + "?org1=" + org + "&org2=" + net + "&year=" + year + "&month=" + month + "&day=" + day + "&hour=" + hour + "&min=" + minu + "&span=" + span + "&arc=" + arc + "&size=" + size + "&LANG=" + lang + "&volc=" + volc + "&rn=" +rn
    r = s.get(url_login, verify=False)
    r = s.post(url_login, data)
    r = s.get(url)
    r = s.get(url_status)
    soup = BeautifulSoup(r.content)
    id = str(soup.find("tr",class_="bglist1").contents[0].string)

    # check data status
    while True:
        r = s.get(url_status)
        soup = BeautifulSoup(r.content)
        if str(soup.find("tr", class_="bglist1").contents[0].string) == id:
            time.sleep(3)  # still preparing data
        elif str(soup.find("tr", class_="bglist2").contents[0].string) == id:
            break          # data avaiable
        elif str(soup.find("tr", class_="bglist3").contents[0].string) == id:
            print("What's bglist3?")
        elif str(soup.find("tr", class_="bglist4").contents[0].string) == id:
            print("Error!")

if __name__ == "__main__":
    code = '030240'
#    code = '010512'
    arc = 'ZIP'
    span = '60'
    org,net,volc = code[0:2], code[2:4], code[0:]
    startTime = datetime(2015,11,22,0)
    endTime = datetime(2015,11,30) 
    
    for singleTime in rrule.rrule( rrule.HOURLY, dtstart = startTime, until = endTime):
        fs = singleTime.isoformat()
        fname = '03_02_40_' + fs[0:4] + fs[5:7] + fs[8:10] + fs[11:13] + '00_60.zip'
#        fname = '01_05_12_' + fs[0:4] + fs[5:7] + fs[8:10] + fs[11:13] + '00_60.zip'
        if os.path.isfile(fname):
            if not zipfile.is_zipfile(fname):
                print "Zip File is broken: " + fname
                os.system('rm ' + fname)
                cont_request(org, net, singleTime, span, arc, volc)
        else:
						print "File Not Exists: " + fname
						cont_request(org, net, singleTime, span, arc, volc)
