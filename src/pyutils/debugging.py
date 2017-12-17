#!/usr/bin/env python

import time

debugOn = False

def timeprint(*args):
  data = [[time.clock()],[": "],args]
  data = ''.join(map(str,[l for s in data for l in s]))
  print(data)

def debug(*debuginfo):
  if debugOn:
    print(''.join(map(str,debuginfo)))

