#!/usr/bin/env python3

## this is pretty underdeveloped rn but its a good proof of concept

##todo:
#   command system with '!' prefix or something
#   maybe time info in input prompt to show the last sent time

import sys,os,json
import mesClient as client

DEBUG = True

def dbg(s,f=0):
    if DEBUG or f:
        print(':: '+s)

# creates a file with cmd in it for display to handle
def sendCommand(inp):
    curdir = os.path.dirname(__file__)
    inp = inp[1:]

    with open(os.path.join(curdir,'th_cmd'),'w') as f:
        cmd = {
                'name': name,
                'data': inp
                }

        f.write(json.dumps(cmd))

    print('sent '+inp)


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
client.send(session,'this is a socket test and not timing btw')

## temporary input system
while True:
    inp = input(name+': ')

    if len(inp):
        if inp[0] == '!':
            sendCommand(inp)
            continue
    
    # this works like an else for both ifs
    for s in inp.split(';'):
        if not s == '':
            if s[0] == '!':
                sendCommand(s)
            else:
                client.send(session,s)
