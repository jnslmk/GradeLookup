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
    
def download_gradesheet(filename, username, password):
    LOGIN_URL = 'https://vorlesungen.tu-bs.de/qisserver/rds?state=user&type=1&category=auth.login&startpage=portal.vm&breadCrumbSource=portal'
    URL_NOTENSPIEGEL = 'https://vorlesungen.tu-bs.de/qisserver/rds?state=notenspiegelStudent&next=list.vm&nextdir=qispos/notenspiegel/student&createInfos=Y&struct=auswahlBaum&nodeID=auswahlBaum%7Cabschluss%3Aabschl%3D88%7Cstudiengang%3Astg%3D104%2Cstgnr%3D11%2Cpversion%3D2&expand=0&asi='
    URL_NOTENSPIEGEL2 = '#auswahlBaum%7Cabschluss%3Aabschl%3D88%7Cstudiengang%3Astg%3D104%2Cstgnr%3D11%2Cpversion%3D2'
    URL_STUDIENVERLAUF_PDF = 'https://vorlesungen.tu-bs.de/qisserver/rds?state=hisreports&status=receive&publishid=pruef_all,de,0&vmfile=no&moduleCall=NotenspiegelTUBS&lastState=notenspiegelStudent&asi='

    payload = {
           'asdf': username,
           'fdsa': password
           }
    
    with requests.Session() as s:
        p = s.post(LOGIN_URL, data = payload)
        asi = re.findall(r'topitem=functions&amp;subitem=myLecturesWScheck&amp;asi=(.+)" class="auflistung "', p.text)[0]
        print('asi: ', asi)
        
        s.get(URL_NOTENSPIEGEL + asi + URL_NOTENSPIEGEL2)
    
        with open('tmp.pdf', 'wb') as f:
            r_studienverlauf_pdf = s.get(URL_STUDIENVERLAUF_PDF + asi, stream=True)
            if r_studienverlauf_pdf.headers['Content-Type'] == 'application/pdf':
                print('Request successful')
            else:
                print('Request failed')
            f.write(r_studienverlauf_pdf.content)
    
def text_from_pdf(filestream):
    """Parse text from pdf and return relevant body of grade file"""
    pdfReader = PyPDF2.PdfFileReader(filestream)
    pageObj = pdfReader.getPage(0)
    pdfText = pageObj.extractText()
    return re.findall(r'\nNote\n(.+)Erläuterungen:', pdfText, re.DOTALL)

FILENAME = 'studienverlauf.pdf'

config = configparser.ConfigParser()
config.read('credentials.ini')

username = config['student account']['username']
password = config['student account']['password']

download_gradesheet('tmp.pdf', username, password)
        
if os.path.isfile(FILENAME):
    with open(FILENAME, 'rb') as f:
        pdfTextBody_old = text_from_pdf(f)
    with open('tmp.pdf', 'rb') as f:
        pdfTextBody_new = text_from_pdf(f)
    if pdfTextBody_old == pdfTextBody_new:
        print('No changes since last download')
    else:
        print('There have been changes since last download')
else:
    print('No previous file found')

#        print(r_studienverlauf_pdf.headers)
#        pretty_print_POST(r_studienverlauf_pdf.request)