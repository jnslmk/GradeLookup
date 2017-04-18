# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 22:34:25 2017

@author: Jonas
"""
import re
import requests

text_new = 'Vorläufiges Gesamtergebnis\n25/120\n2,3\n2511071\nTechnische Optik\n08.03.2017\nAN (RT)\n*\nKernbereich Mechatronik\n2412281\nAutomatisierungstechnik 1\n(Automatisierungstechnik) \n27.02.2017\n5\n1F\nBE\n3,3\n2540103\nSimulation komplexer Systeme\n5\n1F\nBE\n1,3\nProfilbereich Mechatronik\n2412481\nElektronische Fahrzeugsysteme\n21.03.2017\n5\n1F\nBE\n2,0\n2538091\nDigitale Schaltungstechnik\n09.03.2017\n5\n1F\nBE\n2,7\n4210401\nProgrammieren I für Studierende der Mechatronik\n1F\nAN\n*\nLaborbereich B Mechatronik\n2540241\nReibungs-und Kontaktflächenphysik\n01.03.2017\n5\n1F\nBE\n2,3\n'
text_old = 'Vorläufiges Gesamtergebnis\n15/120\n2,7\n2511071\nTechnische Optik\n08.03.2017\nAN (RT)\n*\nKernbereich Mechatronik\n2540103\nSimulation komplexer Systeme\n1F\nAN\n*\nProfilbereich Mechatronik\n2412481\nElektronische Fahrzeugsysteme\n21.03.2017\n1F\nAN\n*\n2538091\nDigitale Schaltungstechnik\n09.03.2017\n5\n1F\nBE\n2,7\n4210401\nProgrammieren I für Studierende der Mechatronik\n1F\nAN\n*\nLaborbereich B Mechatronik\n2540241\nReibungs-und Kontaktflächenphysik\n01.03.2017\n5\n1F\nBE\n2,3\n'

email = 'jns.lemke@gmail.com'
recepient = 'Jonas Lemke'
api_key = 'key-9936186767def6b1c2f7eeef9bdd41bc'

lst_text_old = text_old.split(sep='\n')
lst_text_new = text_new.split(sep='\n')

dict_total_old = {}
dict_total_new = {}
dict_total_old['total_credits'] = lst_text_old[1]
dict_total_old['total_grade'] = lst_text_old[2]
dict_total_new['total_credits'] = lst_text_new[1]
dict_total_new['total_grade'] = lst_text_new[2]

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
    lst_modules_changed.append([])
    lst_modules_changed.append([])
    lst_modules_new = []
    for key, value in contents_new.items():
        if key in contents_old:
            if value != contents_old[key]:
                lst_modules_changed[0].append(value)
                lst_modules_changed[1].append(contents_old[key])
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
    
def send_notification(text, email, recepient, api_key):
    p = requests.post(
        "https://api.mailgun.net/v3/sandboxf9f20535651b426ab55ebc05468cd3f1.mailgun.org/messages",
        auth=("api", api_key),
        data={"from": "Mailgun Sandbox <postmaster@sandboxf9f20535651b426ab55ebc05468cd3f1.mailgun.org>",
              "to": recepient + ' <' + email + '>',
              "subject": "Neue Moduleinträge im QIS-Portal",
              "text": text}
        )
    if p.status_code == 200:
        print('Sent email successfully')
    else:
        print('Email sending not successful')
modules_old = get_modules(lst_text_old)
modules_new = get_modules(lst_text_new)

dict_module_contents_old = get_module_contents(lst_text_old, modules_old)
dict_module_contents_new = get_module_contents(lst_text_new, modules_new)

lst_modules_changed, lst_modules_new = \
    compare_module_contents(dict_module_contents_old, dict_module_contents_new)

mailtext = build_mailtext(dict_total_old, dict_total_new, \
                          lst_modules_changed, lst_modules_new)
print(mailtext)
#send_notification(mailtext, email, recepient, api_key)