import time
import json

#https://pypi.org/project/file-read-backwards/
from file_read_backwards import FileReadBackwards



def save(filename, text):
    #dict for jason dump
    data = {"time":str(time.time()),"message": text }
    data = json.dumps(data)

    with open(filename, "a+")as outfile:
        outfile.write(f"{data},\n")




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

            #the contents of the file can sometimes be a bit messy
            #doing lstripped bc the ',' at the end is neede else where
            lstripped = l.strip(" ")
            lstripped = lstripped.strip("\n")
            lstripped = lstripped.strip(" ")
            lstripped = lstripped.strip(",")

            #after each \n check the time
            line = json.loads(lstripped)
            senderTime = int(float(line["time"]))


            # no need to json.loads the return bc its simple to do it client side
            if senderTime < time:
                return reqLines

            # in the end we want to send all and not just one line
            reqLines = reqLines + str(l)

    # if the file ended and the time requested still didnt match then send the whole file
    return reqLines






