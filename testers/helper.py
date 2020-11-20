import mimetypes
import base64
import requests

def sendfile(url, json, filename):
    mime = mimetypes.MimeTypes().guess_type(filename)[0]
    print('mime: ',mime, type(mime))


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
        'mimetype': str(mime),
        'extention': extension,
        'data': contents
            }

    return requests.post(url=url, json=a)
