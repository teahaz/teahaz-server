#!/usr/bin/env python3

import sys,json,os,datetime,time,signal
import mesClient as client

# detect program exit
def onExit(signum,frame):
    global keepGoing

    keepGoing = False #break while loop
    print('exiting')
    sys.exit()

signal.signal(signal.SIGINT,onExit)
signal.signal(signal.SIGTSTP,lambda: print('you arent supposed to do this'))

# cursor movement:
# http://www.tldp.org/HOWTO/Bash-Prompt-HOWTO/x361.html
#  \033[<L>;<C>f
#  puts the cursor at line L and column C.

#from https://stackoverflow.com/a/3010495 ; get terminal size
def terminal_size():
    import fcntl, termios, struct
    h, w, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return w, h

def dbg(s):
    with open(os.path.join(os.path.dirname(__file__),'log'),'a') as f:
        f.write(' '+s+'\n')


# listens until it gets a messge and it returns either that or an error
def check(session):
    a = client.check(session)
    
    # these arent necessary true, you can never tell why a socket fails but usually they are good
    if a == -1:
        print("Connection closed.")
        return 0
    elif a == -2:
        print("Malformed packet from server.")
        return 0
    else:
        return(a.decode("utf-8"))


def border(y,s=''):
    '''
    /-=-=-=-=-=-=-=-=-=-=-\ 
    |         {s}         |
    \-=-=-=-=-=-=-=-=-=-=-/
    '''
    
    line1 = '/'+int((tWidth-4)/2)*'-='+'-'+'\ '
    line2 = '|'+s.center(tWidth-2)[:-1]+'|'
    line3 = '\\'+int((tWidth-4)/2)*'-='+'-'+'/ '
    b = '\n'.join([line1,line2,line3])

    #b = '\n'.join(['\n/'+(tWidth-4)*'-'+'\ ', s.center(tWidth),'\\'+(tWidth-4)*'-'+'/\n'])
    
    if y:
        sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y,0,b))
        sys.stdout.flush()
    else:
        print(b)


def printMsg(msgIndex):
    # _msgIndex: index into messages
    # uses global name, messages, height
    # note: because of the server format this needs a dict as a string

    #global height 
    
    msg = json.loads(messages[msgIndex])
    previousName = json.loads(messages[msgIndex-1])['name']
    sameName = (previousName == msg['name'])
    time = epochToDT(msg['time'])
    
    
    if showIcons:
        icons = [' ','.','-','=','-','.']
        if sameName:
            icon = icons[msgIndex % len(icons)]
        else: 
            icon = icons[0]
    else:
        icon = ''
 

    if msgIndex == 0 or not sameName:
        print('\n ',msg['name'],':',sep='')
 

    text = '  '+icon+'  '+msg['message'].replace('\\n','\n')
    if showTime:
        timePad = tWidth-len(text)-14
        text += timePad*' '+icon+'  '+time

    print(text)


def handleCommand(cmd):
    global showTime,showIcons
    
    dbg('cmd: '+cmd)
    cmd = cmd.lower()

    if cmd in ['c','clr','clear']:
        os.system('clear')
        
        global messages
        messages = [] 

    elif cmd in ['st','showtime']:
        showTime = not showTime
        showIcons = not showIcons

    elif cmd in ['si','showicons']:
        showIcons = not showIcons
    

    else:
        return -1
    return 1


def epochToDT(t):
    return time.strftime('%H:%M:%S', time.localtime(float(t)))



################################################################################

os.system('clear')

curdir = os.path.dirname(__file__)
tWidth,tHeight = terminal_size()
ip = "127.0.0.1"
port = 8001

### log in
## this uses login.py, its temporary and i only needed it for easy login with the same name but its gonna work similarly
from login import name 
session = client.connect(name, ip, port)

## error checking
if session == 0:
    dbg('Connection failure in login.')
    sys.exit()

## to avoid <socket mumbo-jumbo>
client.send(session,'login')

### initialization
messages = []
height = 0

## "loading" message (mostly placeholder)
# top border
border(y=0,s=name+' @ teahaz')

#move cursor down
print('\033[5;0f')
print(' teahaz:\n  Checking messages...')

# bottom border
border(y=tHeight-3,s=str(datetime.datetime.now())[:19])

# safeguard
if 'th_cmd' in os.listdir(curdir):
    os.remove(os.path.join(curdir,'th_cmd'))

# create log file
open(os.path.join(os.path.dirname(__file__),'log'),'w').close

#needs server side fixes
#oldMessages = json.load(open('message_history','r'))
#messages = [m for m in oldMessages]


showTime = True
showIcons = True


### main loop
# checks messages, adds them to array and displays
# needed so that onExit can terminate the loop
skip = False
keepGoing = True
while keepGoing:

    ## handle commands sent by input
    if 'th_cmd' in os.listdir(curdir):
        cmd = json.load(open(os.path.join(curdir,'th_cmd'),'r'))
        os.remove(os.path.join(curdir,'th_cmd'))
        dbg('received '+cmd['data'])
        if cmd['name'] == name:
            handleCommand(cmd['data'])    
            skip = True

   
    ## get new messages
    if not skip:
        msg = check(session)
    
    ## add to array
    # errors are already printed in check, but theyll be logged to a file probably so this just ignores them
    if isinstance(msg,str):
        messages.append(msg)
   
        ## originally the idea was to have it count the lines and only display what fits the screen
        ## but i realized scrollback would be a mess so i decided against it, but imma leave some code i had for it just in case
        
        # add height
        #newlines 
        nl = msg.count('\\n')

        #overflows
        ov = int(len(json.loads(msg)['message'])/tWidth)
        #print(nl,ov)
        height += ov + nl + 1
        
    os.system('clear')


    ## print
    #top border
    border(y=0,s=name+' @ teahaz')

    #move cursor down
    print('\033[5;0f')

    #body
    for i in range(len(messages)):
        printMsg(i)

    #bottom border 
    if height > tHeight-10:
        border(y=tHeight,s=str(datetime.datetime.now())[:19])
    else:
        border(y=tHeight-3,s=str(datetime.datetime.now())[:19])

    skip = False

if not keepGoing:
    os.system('clear')
