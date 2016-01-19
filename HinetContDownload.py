#!/usr/bin/python
import multiprocessing
import os.path

import requests
from bs4 import BeautifulSoup
import time
import cookielib

# specify user name and password
user = "username"
passwd = "password"

# base url for continuous waveform data
url_login='https://hinetwww11.bosai.go.jp/auth/?LANG=en'
url_download='https://hinetwww11.bosai.go.jp/auth/download/cont/cont_download.php'
url_status='https://hinetwww11.bosai.go.jp/auth/download/cont/cont_status.php?LANG=en&page=1'

s = requests.Session()
#gcookie = cookielib.CookieJar()

def download(params):
    d = s.get(url_download, params=params, stream=True, verify=False)
#    d = requests.get(url_status, params=params, cookies = gcookie, stream=True, verify=False)
#    global gcookie
#    gcookie = d.cookies
#    if d.status_code == 401:
#        print("Unauthorized.")
#        sys.exit()

    # file size
    size = int(d.headers['Content-Length'].strip())
    # file name
    disposition = d.headers['Content-Disposition'].strip()
    fname = disposition.split('filename=')[1].strip('\'"')

    print("Downloading %s ..." % (fname))
    if not os.path.exists(fname):
        with open(fname, "wb") as fd:
            self = 0
            for chunk in d.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    fd.write(chunk)
                    fd.flush()
                self += len(chunk)
        print("Download Successfully: " + fname)


def cont_download(id):
    """Download continuous waveform data of specified id"""
    params = {"id": id}
    download(params)


def get_ids():
    ids = []
    # new
#    login_para = {'auth_un': user, 'auth_pw':passwd }
    data = {'auth_un': user, 'auth_pw':passwd }
#    s = requests.Session()
    r = s.get(url_login, verify=False)
    r = s.post(url_login, data)
    r = s.get(url_status, verify=False)
#    global gcookie
#    gcookie = r.cookies
    if r.status_code == 401:
        print("Unauthorized.")
        sys.exit()
    soup = BeautifulSoup(r.content)

    for data in soup.find_all("tr", class_="bglist2"):
        ids.append(str(data.contents[0].string))

    return ids[::-1]  # return id in reverse order


if __name__ == '__main__':
    while True:
        ids = get_ids()
        if len(ids) == 0:
            print("Waiting For Requesting...")
            time.sleep(20)
            continue
        else:
#            if len(ids) > 4:
#                proc = 8
#            else:
#                proc = len(ids)
#            pool = multiprocessing.Pool(processes = proc)
#            pool.map(cont_download, ids)
#            pool.close()
#            pool.join()
            for id in ids:
                cont_download( id )
