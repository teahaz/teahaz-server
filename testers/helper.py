import base64
import requests

def sendfile(url, json, filename):


    with open(filename, 'rb')as infile:
        contents = infile.read()

    contents = base64.b64encode(contents).decode('utf-8')


    # get file extension bc mimetype sucks sometimes
    extension = filename.split(".")[-1]
    print('extension: ',extension , type(extension))


    a = {
        'username': json["username"],
        'cookie': json["cookie"],
        'chatroom': json["chatroom"],
        'type': "file",
        'extension': extension,
        'data': contents
            }

    return requests.post(url=url, json=a)
