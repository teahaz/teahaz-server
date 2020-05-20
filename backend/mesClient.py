import socket
import json
import base64

################################################################################################################################################################################
# *this following is some specifications about the protocol used to communicate to the server*
# *do not expect these to stay the same*

### packet structure
    #the following structure must be followed by both send and the recv

## packets are sent with 2 headers

# header 1 [len = 15] contains the length of the 2 other headers combined
    #this header is used to determain how much we need to recv

# header 2 [len = 20] is the name of the sender
    # i will not be dealing with this header but leave balazs to deal with it as he likes

### connections
# when connecting to the server the first message is a name with 20 padding

################################################################################################################################################################################


def send(session, text):

    #try:
    if True:
        print(session)
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



# we dont need 2 headers bc balazs can deal with the username
def listen(session):
    name, socc = session
    
    while True:
        #try recv the header of the message
        try:
            message_header = socc.recv(20)
        except:
            return -1

        
        if len(message_header) > 1:
            #try:
            message_len = int(message_header.decode("utf-8").strip())
            return socc.recv(message_len)
            #except: 
            #    return -2
    
def get(session, time):

    name, socc = session
    time = str(time)

    #the server makes an exception for the header "get"
    header = "get"
    message = f"{header:<20}{time}"
    
    socc.send(message.encode("utf-8"))
    
    print("getting message") 
    message_header = socc.recv(20)
    print("getting message") 
    if len(message_header) == 0:
        return -1

    print("getting message") 
    message_len = int(message_header.decode("utf-8").strip())
    return socc.recv(message_len)



    
