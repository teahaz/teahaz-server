import socket
import json
import base64

################################################################################################################################################################################
# *this following is some specifications about the protocol used to communicate to the server*
# *do not expect these to stay the same*

# header 1 [len = 15] contains the length of the 2 other headers combined
    #this header is used to determain how much we need to recv

# the message itself is a dict/one line json, that can be converted via the json library
    #the dict would contain the users name and their message in following format
        #{"name":"users_name", "message":"users_message"}

### connections
# when connecting to the server the first message is a name with 20 padding

################################################################################################################################################################################


def send(session, text):
    #try:
    if True:
        ################### some exception raised bc name is not part of session???
        name, socc = session

        #name and data should be in json format
        data = {"name": name, "data": text}

        message = json.dumps(data)
        
        #message has to be encoded in bas64 as it could because it has the potential to cause formatting vulnerabilities
        message = base64.b64encode(message.encode("utf-8"), altchars=None)

        header = len(message)
    #except:
    else:
        return -1

    try:
        socc.send(f"{header:<20}".encode("utf-8")+message)
    except:
        return -2   



def connect(name, ip, port):
    #try:
    if True:
        socc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socc.connect((ip, port))

        #session has to be name and socc for consitency 
        if not send((name, socc), name): # if it doesnt return then its good
            pass
        else:
            return 0

        return (name, socc)
    else:
    #except:
        return 0



def listen(session):
    name, socc = session
    
    while True:
        #try recv the header of the message
        try:
            message_header = socc.recv(20)
        except:
            return -1

        
        if len(message_header) > 1:
            try:
                message_len = int(message_header.decode("utf-8").strip())
                
                mesb64 = socc.recv(message_len)

                return base64.b64decode(mesb64, altchars=None)
            except: 
                return -2
 


def check(session):
    name, socc = session
    
    #while True:
    #try recv the header of the message
    try:
        message_header = socc.recv(20)
    except:
        return -1
    
    if len(message_header) > 1:
        try:
            message_len = int(message_header.decode("utf-8").strip())
            
            mesb64 = socc.recv(message_len)

            return base64.b64decode(mesb64, altchars=None)
        except: 
            return -2



    
def get(session, time):
    name, socc = session
    time = str(time)

    #the server makes an exception for the header "get"
    header = "get"
    message = f"{header:<20}{time}"
    
    socc.send(message.encode("utf-8"))
    
    message_header = socc.recv(20)
    if len(message_header) == 0:
        return -1

    message_len = int(message_header.decode("utf-8").strip())

    #i am fully aware that this is not how i should be handling json
    unformatData = socc.recv(message_len).decode("utf-8")
    
    #the json/dictionaries are stored one by one bc it makes them a lot easier to handle in larger numbers
    #i am fully aware that this is not how i should be handling json
    messages = ""
    unformatData = unformatData.split("\n")
    for line in unformatData:
        # the last one can often be empty line and this is the simplest way of filtering it
        if len(line) > 5:
            formatData = json.loads(line.strip(",\n"))
            formatDataDec = base64.b64decode(formatData["message"])
            formatDataDec = formatDataDec.decode("utf-8")
            messages += formatDataDec+"\n"

    return messages


    
