# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
import re
import os.path
import PyPDF2
import configparser

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

LOGIN_URL = 'https://vorlesungen.tu-bs.de/qisserver/rds?state=user&type=1&category=auth.login&startpage=portal.vm&breadCrumbSource=portal'
URL_NOTENSPIEGEL = 'https://vorlesungen.tu-bs.de/qisserver/rds?state=notenspiegelStudent&next=list.vm&nextdir=qispos/notenspiegel/student&createInfos=Y&struct=auswahlBaum&nodeID=auswahlBaum%7Cabschluss%3Aabschl%3D88%7Cstudiengang%3Astg%3D104%2Cstgnr%3D11%2Cpversion%3D2&expand=0&asi='
URL_NOTENSPIEGEL2 = '#auswahlBaum%7Cabschluss%3Aabschl%3D88%7Cstudiengang%3Astg%3D104%2Cstgnr%3D11%2Cpversion%3D2'
URL_STUDIENVERLAUF_PDF = 'https://vorlesungen.tu-bs.de/qisserver/rds?state=hisreports&status=receive&publishid=pruef_all,de,0&vmfile=no&moduleCall=NotenspiegelTUBS&lastState=notenspiegelStudent&asi='
FILENAME = 'studienverlauf.pdf'

config = configparser.ConfigParser()
config.read('credentials.ini')

USERNAME = config['student account']['username']
PASSWORD = config['student account']['password']

payload = {
           'asdf': USERNAME,
           'fdsa': PASSWORD
           }

with requests.Session() as s:
    p = s.post(LOGIN_URL, data = payload)
    asi = re.findall(r'topitem=functions&amp;subitem=myLecturesWScheck&amp;asi=(.+)" class="auflistung "', p.text)[0]
    print('asi: ', asi)
    
    r_notenspiegel = s.get(URL_NOTENSPIEGEL + asi + URL_NOTENSPIEGEL2)

#    headers = {
#               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#               'Accept-Encoding': 'gzip, deflate, sdch, br',
#               'Accept-Language': 'de-DE,de;q=0.8,en;q=0.6,es;q=0.4,zh-TW;q=0.2,zh;q=0.2',
#               'Host': 'vorlesungen.tu-bs.de',
#               'Referer': 'https://vorlesungen.tu-bs.de/qisserver/rds?state=notenspiegelStudent&next=list.vm&nextdir=qispos/notenspiegel/student&createInfos=Y&struct=auswahlBaum&nodeID=auswahlBaum%7Cabschluss%3Aabschl%3D88%7Cstudiengang%3Astg%3D104%2Cstgnr%3D11%2Cpversion%3D2&expand=0&asi=' + asi,
#               'Upgrade-Insecure-Requests': '1',
#               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
#               }

    with open('tmp.pdf', 'wb') as f:
        r_studienverlauf_pdf = s.get(URL_STUDIENVERLAUF_PDF + asi, stream=True)
        if r_studienverlauf_pdf.headers['Content-Type'] == 'application/pdf':
            print('Request successful')
        else:
            print('Request failed')
        f.write(r_studienverlauf_pdf.content)
        
    if os.path.isfile(FILENAME):
        with open(FILENAME, 'rb') as f1:
            with open('tmp.pdf', 'rb') as f2:
                pdfReader1 = PyPDF2.PdfFileReader(f1)
                pageObj1 = pdfReader1.getPage(0)
                pdfText1 = pageObj1.extractText()
                pdfReader2 = PyPDF2.PdfFileReader(f2)
                pageObj2 = pdfReader2.getPage(0)
                pdfText2 = pageObj2.extractText()
                if pdfText1 == pdfText2:
                    print('No changes since last download')
                else:
                    print('There have been changes since last download')
    else:
        print('No previous file found')

#        print(r_studienverlauf_pdf.headers)
#        pretty_print_POST(r_studienverlauf_pdf.request)