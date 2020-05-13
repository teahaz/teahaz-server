import time
import json

#https://pypi.org/project/file-read-backwards/
from file_read_backwards import FileReadBackwards



def save(filename, text):
    #dict for jason dump
    data = {"time":str(time.time()),"message": text }
    data = json.dumps(data)
    
    with open(filename, "a+")as outfile:
        outfile.write(f"{data}\n")




def get(filename, time):
    # the client will send a time indicating how old messages it wants
    time = int(float(str(time).strip()))


    # one line in the logfile
    line = ""
    #all thr requested lines
    reqLines = ""

    #read file backwards
    with FileReadBackwards(filename , encoding="utf-8") as frb:
        while True:
            #read until file has ended
            l = frb.readline()
            if not l:
                break
            #after each \n check the time
            line = json.loads(l)
            senderTime = int(float(line["time"]))

            if senderTime < time:
                return reqLines

            reqLines = reqLines + str(line)



        

    
    
