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
        if 'Anmeldung fehlgeschlagen' in p.text:
            print('Login unsuccessful. Aborting script.')
            raise SystemExit()
        else:
            print('Successfully logged in as ' + username + '.')
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
    
def compare_pdfs(oldfile, newfile):
    if os.path.isfile(FILENAME):
        with open(oldfile, 'rb') as f:
            pdf_text_body_old = text_from_pdf(f)
        with open(newfile, 'rb') as f:
            pdf_text_body_new = text_from_pdf(f)
        if pdf_text_body_old == pdf_text_body_new:
            print('No changes since last download')
            return 0, pdf_text_body_old, pdf_text_body_new
        else:
            print('There have been changes since last download')
            return 1, pdf_text_body_old, pdf_text_body_new
    else:
        print('No previous file found')
        return 0, 0, 0
        
def get_total_result(text):
    re.findall()
        
def get_differences(text_old, text_new):
    return 1

FILENAME = 'studienverlauf.pdf'
FILENAME_TMP = 'tmp.pdf'

config = configparser.ConfigParser()
config.read('credentials.ini')

username = config['student account']['username']
password = config['student account']['password']

try:
    download_gradesheet(FILENAME_TMP, username, password)
    changed, text_old, text_new = compare_pdfs(FILENAME, FILENAME_TMP)
    if changed:
        differences = get_differences(text_old, text_new)
except SystemExit:
    print('Script aborted.')


#        print(r_studienverlauf_pdf.headers)
#        pretty_print_POST(r_studienverlauf_pdf.request)