# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 22:34:25 2017

@author: Jonas
"""
import re

def modules_to_dict(ind_first, ind_last):
    return dict

text_new = 'Vorläufiges Gesamtergebnis\n25/120\n2,3\n2511071\nTechnische Optik\n08.03.2017\nAN (RT)\n*\nKernbereich Mechatronik\n2412281\nSimulation komplexer Systeme\n5\n1F\nBE\n1,3\nProfilbereich Mechatronik\n2412481\nElektronische Fahrzeugsysteme\n21.03.2017\n5\n1F\nBE\n2,0\n2538091\nDigitale Schaltungstechnik\n09.03.2017\n5\n1F\nBE\n2,7\n4210401\nProgrammieren I für Studierende der Mechatronik\n1F\nAN\n*\nLaborbereich B Mechatronik\n2540241\nReibungs-und Kontaktflächenphysik\n01.03.2017\n5\n1F\nBE\n2,3\n'
text_old = 'Vorläufiges Gesamtergebnis\n15/120\n2,7\n2511071\nTechnische Optik\n08.03.2017\nAN (RT)\n*\nKernbereich Mechatronik\n2412281\nAutomatisierungstechnik 1\n(Automatisierungstechnik) \n27.02.2017\n5\n1F\nBE\n3,3\n2540103\nSimulation komplexer Systeme\n1F\nAN\n*\nProfilbereich Mechatronik\n2412481\nElektronische Fahrzeugsysteme\n21.03.2017\n1F\nAN\n*\n2538091\nDigitale Schaltungstechnik\n09.03.2017\n5\n1F\nBE\n2,7\n4210401\nProgrammieren I für Studierende der Mechatronik\n1F\nAN\n*\nLaborbereich B Mechatronik\n2540241\nReibungs-und Kontaktflächenphysik\n01.03.2017\n5\n1F\nBE\n2,3\n'

lst_text_old = text_old.split(sep='\n')
lst_text_new = text_new.split(sep='\n')

total_old_credits = lst_text_old[1]
total_old_grade = lst_text_old[2]
total_new_credits = lst_text_new[1]
total_new_grade = lst_text_new[2]

def get_modules(lst_text):
    lst_modules = []
    for index, value in enumerate(lst_text):
        if re.match(r'\d{7}', value):
            lst_modules.append([value, index])
            print(str(index) + ': ' + str(value))
    return lst_modules
    
def get_module_content(lst_text, start, end):
    lst_module = []
    for value in lst_text[start:end]:
        if not (('bereich' in value and 'Mechatronik' in value) or value == ''):
            lst_module.append(value)
    return lst_module
    
def get_module_contents(lst_text, lst_modules):
    lst_module_contents = []
    for index, tpl in enumerate(lst_modules):
        if not index == len(lst_modules) - 1:
            end = lst_modules[index + 1][1] - 1
        else:
            end = len(lst_text) - 1
        lst_module_contents.append(get_module_content(lst_text, index, end))
    return lst_module_contents
    
lst_modules_old = get_modules(lst_text_old)
lst_modules_new = get_modules(lst_text_new)

lst_modulecontents_old = get_module_contents(lst_text_old, lst_modules_old)