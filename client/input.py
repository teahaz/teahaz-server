#!/usr/bin/env python3

## this is pretty underdeveloped rn but its a good proof of concept

##todo:
#   command system with '!' prefix or something
#   maybe time info in input prompt to show the last sent time

import sys,threading
import mesClient as client

DEBUG = True

def dbg(s,f=0):
    if DEBUG or f:
        print(':: '+s)

ip = "127.0.0.1"
port = 8001

### log in -> same as display.py, but here you can force a diff user with sys args for testing
if len(sys.argv) == 1:
    from login import name
else:
    name = sys.argv[1]

## connect
session = client.connect(name, ip, port)

## error checking
if session == 0:
    dbg('Connection failure in login.')
    sys.exit()

## needed for timing or idk
client.send(session,'login')

## temporary input system
while True:
    client.send(session,input(name+': '))
