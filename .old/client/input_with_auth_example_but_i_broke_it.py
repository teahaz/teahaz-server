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

######################################################### i promise i didnt change anything out side of this
######################################################### this code is just to show how auth should work, you should probably make it more as you like,
## needed for timing or idk
client.send(session,'this is a socket test and not a timing thing btw')

import security

# explination of argumets to security.auth
# 1, session is manditory
# 2, the first time the user connects [s]he will give a username and a password, a hashed password and a plain text username will be stored in the `path_to_saved_creds` 
    # so password_auth== True when the user has not been authenticated on this device yet(does not have a creds file), otherwhise it should be false
    # the reason for username not being hashed is that this way the saved_creds file can store the username displayed to others as well as be used for automatic logins
# 3, 4 should be obvi, they are only taken into account if password_auth is True
#5 is the path to the creds file, ofc this could be anywhere i just set './.creds' as a default. you can change it however you like, knock yourself out
    #IMPORTANT path_to_saved_creds is needed when using password_auth as well, in this case the passowrd in path_to_saved_creds will be overwritten by a new one
    # saving creds isnt fully implemented yet but will come soon, for now just hardcode the username or something idk
security.authenticate(session, password_auth=True, username="username", password="password", path_to_saved_creds="./.creds")



######################################################### /this code is just to show how auth should work, you should probably make it more as you like

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
