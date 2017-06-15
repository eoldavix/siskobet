#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys

salida = ""

try:
  for line in sys.stdin.readlines():

    if re.search("^[*]*[\s]*[0-9]+[.:][0-9]+", line) \
       or re.search("[pP][tT][sS]* [eE][/]*[wW]", line) \
       or re.search("[pP][tT][sS]* [wW][iI][nN]", line) \
       or re.search("datos-apuesta", line) \
       or "points per line" in line.lower() \
       or "No selections today" in line \
       or re.search("[0-9]+ [pP][oO][iI][nN][tT][sS]*", line):

      if "Recommendation" in line:
        m = re.match(".*(Recommendation.*)", line)
        salida += m.group(1) + "\n"
      elif "datos-apuesta" in line:
        m = re.match("^.*(http.*datos-apuesta[\S]*).*$", line)
        salida += "Enlace al Pick de Inma Molero: \n"
        salida += m.group(1)

      else:
        salida += line.replace("*", "")

  print salida


except:
  pass
