# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 22:34:25 2017

@author: Jonas
"""

import difflib

text_new = 'Vorläufiges Gesamtergebnis\n25/120\n2,3\n2511071\nTechnische Optik\n08.03.2017\nAN (RT)\n*\nKernbereich Mechatronik\n2412281\nSimulation komplexer Systeme\n5\n1F\nBE\n1,3\nProfilbereich Mechatronik\n2412481\nElektronische Fahrzeugsysteme\n21.03.2017\n5\n1F\nBE\n2,0\n2538091\nDigitale Schaltungstechnik\n09.03.2017\n5\n1F\nBE\n2,7\n4210401\nProgrammieren I für Studierende der Mechatronik\n1F\nAN\n*\nLaborbereich B Mechatronik\n2540241\nReibungs-und Kontaktflächenphysik\n01.03.2017\n5\n1F\nBE\n2,3\n'
text_old = 'Vorläufiges Gesamtergebnis\n15/120\n2,7\n2511071\nTechnische Optik\n08.03.2017\nAN (RT)\n*\nKernbereich Mechatronik\n2412281\nAutomatisierungstechnik 1\n(Automatisierungstechnik) \n27.02.2017\n5\n1F\nBE\n3,3\n2540103\nSimulation komplexer Systeme\n1F\nAN\n*\nProfilbereich Mechatronik\n2412481\nElektronische Fahrzeugsysteme\n21.03.2017\n1F\nAN\n*\n2538091\nDigitale Schaltungstechnik\n09.03.2017\n5\n1F\nBE\n2,7\n4210401\nProgrammieren I für Studierende der Mechatronik\n1F\nAN\n*\nLaborbereich B Mechatronik\n2540241\nReibungs-und Kontaktflächenphysik\n01.03.2017\n5\n1F\nBE\n2,3\n'

print(''.join(difflib.ndiff(text_new, text_old)))