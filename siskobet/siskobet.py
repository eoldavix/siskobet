#!/usr/bin/env python
# -*- coding: utf-8 -*-

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

""" Siskobetting """

import re
import sys

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

def html_to_text(texto):
    """ De HTML a texto """

    salida = ""

    if "datos-apuesta" in texto:
        for line in texto.split('\n'):
            matching = re.match(r"^.*(http.*datos-apuesta[\S]*).*$", line)
            if matching:
                salida += matching.group(1) + "\n"

        return salida.split('\n') or u''
    elif "Advised Odds" in texto:
        salida = "Advised Odds\n"
        
        lineas = texto.split('\n')

        for i in range(0, len(lineas)):
            if "Advised Odds" in lineas[i]:
                apuesta = ""
                for z in range(1, 7):
                    apuesta += lineas[i+z].replace('\t', '').replace('Odds for this selection provided by', '')
                    apuesta += ' - '
                salida += apuesta[:-2] + '\n'
        return salida
    else:
        return BeautifulSoup(texto, "lxml").body.get_text(separator=u'\n').split('\n')

def parsea_texto(texto):
    """ Buscamos la información que queremos """

    salida = ""

    regexes = [r"^[*]*[\s]*[0-9]+[.:][0-9]+",
               r"[pP][tT][sS]* [eE][/]*[wW]",
               r"[pP][tT][sS]* [wW][iI][nN]",
               r"[0-9]+ [pP][oO][iI][nN][tT][sS]*",
               r"^Tip #",
              ]

    combined = "(" + ")|(".join(regexes) + ")"
    if "Advised Odds" in texto:
        return texto
    try:
        for line in texto:
            if re.search(combined, line) \
               or "points per line" in line.lower() \
               or "No selections today" in line \
               or "datos-apuesta" in line:

                if "Recommendation" in line:
                    matching = re.match(".*(Recommendation.*)", line)
                    salida += matching.group(1) + "\n"
                elif "datos-apuesta" in line:
                    matching = re.match(r"^.*(http.*datos-apuesta[\S]*).*$", line)
                    salida += "Enlace al Pick de Inma Molero: \n"
                    salida += matching.group(1) + "\n"
                else:
                    salida += line.replace("*", "") + "\n"

        return salida


    except:
        pass

def main():
    texto = unicode(sys.stdin.read(), errors='ignore')

    # for link in html.body.find_all('a'):
    #     if datos-apuesta in link:
    #         print(link.get('href'))

    print parsea_texto(html_to_text(texto))
    #html_to_text(texto)

if __name__ == '__main__':
    main()
