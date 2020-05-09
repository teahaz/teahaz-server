#!/usr/bin/env python3

#Basic imports
#maybe this should be done with socketserver but fuck it ima build my own   
import socket
import threading

#globals
global PORT
PORT = 8000

global HEADERLEN
HEADERLEN = 50

########### some temp stuff
def send(socc):
    while True:
        a = input()
        name = "server"
        f = f"{name:<{HEADERLEN}}{a}".encode("utf-8")
        socc.send(f)


def recv(socc):
    while True:
        a = socc.recv(1024)
        if len(a) > 6:
            a = a.decode("utf-8")
            print(a)


########### some temp stuff


# main process called as a thread to handle connections
def main(socc, addr):
    print(f"conneciton from {addr}")
    
    #some testing

    s = threading.Thread(target=send, args=(socc,))
    s.start()

    recv(socc)



# some server setup
if __name__ == "__main__":
    while True:
        #set handler 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #needed to not get addr in use error
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #listen for connections
        s.bind(("", PORT)) 
        s.listen()
        socc, addr = s.accept()
        #start main as a thread with the new connection
        x = threading.Thread(target=main, args=(socc,addr))
        x.start()


