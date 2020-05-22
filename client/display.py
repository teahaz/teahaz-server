#!/usr/bin/env python3

import sys,json,os,datetime
import mesClient as client

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


# listens until it gets a messge and it returns either that or an error
def check(session):
    a = client.check(session)
    
    # these arent necessary true, you can never tell why a socket fails but usually they are good
    if a == -1:
        dbg("Connection closed.")
        return 0
    elif a == -2:
        dbg("Malformed packet from server.")
        return 0
    else:
        return(a.decode("utf-8"))


def border(y,s=''):
    '''
    /--------------------\ 
              {s}
    \--------------------/
    '''
    
    b = '\n'.join(['\n/'+(tWidth-4)*'-'+'\ ', s.center(tWidth),'\\'+(tWidth-4)*'-'+'/\n'])
    
    if y:
        sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y,0,b))
        sys.stdout.flush()
    else:
        print(b)


def printMsg(msgIndex):
    # _msgIndex: index into messages
    # uses global name, messages, height
    global height 
    
    try:
        msg = json.loads(messages[msgIndex])
    
    #already dict
    except TypeError:
        msg = messages[msgIndex]

    previousName = json.loads(messages[msgIndex-1])['name']
    text = '  '+msg['data'].replace('\\n','\n')
 
    if msgIndex == 0 or msg['name'] != previousName:
        #height += 2
        print('\n ',msg['name'],':',sep='')

    print(text)



################################################################################

os.system('clear')

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
border(y=0,s='teahaz')

#move cursor down
print('\033[5;0f')
print(' teahaz:\n  Checking messages...')

# bottom border
border(y=tHeight-3,s=str(datetime.datetime.now())[:19])


#needs server side fixes
#oldMessages = json.load(open('message_history','r'))
#messages = [m for m in oldMessages]


### main loop
# checks messages, adds them to array and displays
while True:
   
    ## get new messages
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
        ov = int(len(json.loads(msg)['data'])/tWidth)
        #print(nl,ov)
        height += ov + nl + 1
        
    os.system('clear')


    ## print
    #top border
    border(y=0,s='teahaz')

    #move cursor down
    print('\033[5;0f')

    #body
    for i in range(len(messages)):
        printMsg(i)
        #pass

    #bottom border 
    #print(tHeight,height)
    if height > tHeight-10:
        border(y=tHeight,s=str(datetime.datetime.now())[:19])
    else:
        border(y=tHeight-3,s=str(datetime.datetime.now())[:19])
