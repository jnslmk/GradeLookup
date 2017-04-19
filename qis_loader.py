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
            pdf_text_body_old = text_from_pdf(f)[0]
        with open(newfile, 'rb') as f:
            pdf_text_body_new = text_from_pdf(f)[0]
        if pdf_text_body_old == pdf_text_body_new:
            print('No changes since last download')
            return 0, pdf_text_body_old, pdf_text_body_new
        else:
            print('There have been changes since last download')
            return 1, pdf_text_body_old, pdf_text_body_new
    else:
        print('No previous file found')
        return 0, 0, 0
        
def replace_pdf(old_pdf, replacement):
    os.remove(old_pdf)
    os.rename(replacement, old_pdf)
    
def get_dict_total(lst_text):
    dict_total = {}
    dict_total['total_credits'] = lst_text[1]
    dict_total['total_grade'] = lst_text[2]
    return dict_total

def get_modules(lst_text):
    lst_modules = []
    for index, value in enumerate(lst_text):
        if re.match(r'\d{7}', value):
            lst_modules.append([value, index])
    return lst_modules
    
def get_module_content(lst_text, start, end):
    lst_module = []
    for value in lst_text[start + 1:end + 1]:
        if not (('bereich' in value and 'Mechatronik' in value) or value == ''):
            lst_module.append(value)
    return lst_module
    
def get_module_contents(lst_text, modules):
    dict_module_contents = {}
    for index, tpl in enumerate(modules):
        if index < len(modules) - 1:
            end = modules[index + 1][1] - 1
        else:
            end = len(lst_text) - 1
        dict_module_contents[tpl[0]] = get_module_content(lst_text, tpl[1], end)
    return dict_module_contents
    
def compare_module_contents(contents_old, contents_new):
    lst_modules_changed = []
    lst_modules_new = []
    for key, value in contents_new.items():
        if key in contents_old:
            if value != contents_old[key]:
                lst_modules_changed.append([value, contents_old[key]])
        else:
            lst_modules_new.append(value)
    return lst_modules_changed, lst_modules_new
    
def build_mailtext(dt_old, dt_new, lst_changed, lst_new):
    text = ''
    if dt_old['total_credits'] != dt_new['total_credits'] \
            and dt_old['total_grade'] != dt_new['total_grade']:
        text += 'Neue Gesamtnote: ' + dt_new['total_grade'] + ' bei ' \
                    + dt_new['total_credits'] + ',\n' \
                    + 'vorher ' + dt_old['total_grade'] + ' bei ' \
                    + dt_old['total_credits'] + '.\n\n'
    else:
        text += 'Unveränderte Gesamtnote ' + dt_new['total_grade'] \
                    + ' bei ' + dt_new['total_credits'] + '.\n\n'
    if len(lst_new) != 0:
        text += 'Neu hinzugefügte Module:\n'
        for module in lst_new:
            for entry in module[:-1]:
                text += entry + ' '
            text += module[-1] + '\n'
        text += '\n'
    if len(lst_changed[0]) != 0:
        text += 'Veränderte Module:\n'
        for module in lst_changed:
            for entry in module[0][:-1]:
                text += entry + ' '
            text += module[0][-1] + '\n'
            text += '('
            for entry in module[1][:-1]:
                text += entry + ' '
            text += module[1][-1] + ')\n'
    return text
    
def send_notification(text, pdf_file, email, recepient, api_key):
    p = requests.post(
        "https://api.mailgun.net/v3/sandboxf9f20535651b426ab55ebc05468cd3f1.mailgun.org/messages",
        auth=("api", api_key),
        data={"from": "Mailgun Sandbox <postmaster@sandboxf9f20535651b426ab55ebc05468cd3f1.mailgun.org>",
              "to": recepient + ' <' + email + '>',
              "subject": "Neue Moduleinträge im QIS-Portal",
              "text": text},
        files=[("attachment", open(pdf_file, 'rb'))]
        )
    if p.status_code == 200:
        print('Sent email successfully')
    else:
        print('Email sending not successful')

FILENAME = 'studienverlauf.pdf'
FILENAME_TMP = 'tmp.pdf'

config = configparser.ConfigParser()
config.read('credentials.ini')

username = config['student account']['username']
password = config['student account']['password']
email = config['email account']['email']
recepient = config['email account']['recepient']
api_key = config['email account']['api-key']

try:
    download_gradesheet(FILENAME_TMP, username, password)
    changed, text_old, text_new = compare_pdfs(FILENAME, FILENAME_TMP)
    replace_pdf(FILENAME, FILENAME_TMP)
    if changed:
        #Text handling
        lst_text_old = text_old.split(sep='\n')
        lst_text_new = text_new.split(sep='\n')
        dict_total_old = get_dict_total(lst_text_old)
        dict_total_new = get_dict_total(lst_text_new)
        modules_old = get_modules(lst_text_old)
        modules_new = get_modules(lst_text_new)
        dict_module_contents_old = get_module_contents(lst_text_old, modules_old)
        dict_module_contents_new = get_module_contents(lst_text_new, modules_new)
        lst_modules_changed, lst_modules_new = compare_module_contents(
            dict_module_contents_old, dict_module_contents_new)
        #mail handling
        mailtext = build_mailtext(dict_total_old, dict_total_new, \
                          lst_modules_changed, lst_modules_new)
        send_notification(mailtext, FILENAME, email, recepient, api_key)
    
except SystemExit:
    print('Script aborted.')