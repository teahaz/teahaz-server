

# again, no im not storing passwords hashed without salt, its just for sending to the server, where it is hashed again
# this hash serves no purpose in secutity, but more just to avoid chars that could break the system
# if its slow then i will replace this with base64 encoding
def hashpassword(password):
    import hashlib
    import base64

    m = hashlib.sha256()
    m.update(password.encode("utf-8"))
    hashed_password = base64.b64encode(m.digest())

    return hashed_password.decode("utf-8")


# explination of all this shit
# 1, session is manditory
# 2, the first time the user connects [s]he will give a username and a password, a hashed password and a plain text username will be stored in the `path_to_saved_creds` 
    # so password_auth== True when the user has not been authenticated on this device yet(does not have a creds file), otherwhise it should be false
    # the reason for username not being hashed is that this way the saved_creds file can store the username displayed to others as well as be used for automatic logins
# 3, 4 should be obvi, they are only taken into account if password_auth is True
#5 is the path to the creds file, ofc this could be anywhere i just set './.creds' as a default. you can change it however you like, knock yourself out
    #IMPORTANT path_to_saved_creds is needed when using password_auth as well, in this case the passowrd in path_to_saved_creds will be overwritten by a new one
def authenticate(session, password_auth=True, username="", password="", path_to_saved_creds="./.creds"):
    import json

    name, socc = session
    if password_auth:
        hashed_password = hashpassword(password)

        # write user creds in json format, so bazsi wont get angry at me
        creds = {"username": username, "password": hashed_password}
        with open(path_to_saved_creds, "w+")as outfile:
            outfile.write(json.dumps(creds))


    else:
        with open(path_to_saved_creds, "r")as infile:
            creds = infile.read()
        creds = json.loads(creds)

        username = creds["username"]
        hashed_password = creds["password"]


    # method for sending the cred
    message = f"{username} {hashed_password}"
    header = str(len(message))
    socc.send(f"{header:<20}{username} {hashed_password}".encode("utf-8"))






def register():
    pass #?

def keyexchange():
    pass

def encrypt():
    pass

def decrypt():
    pass


# as we are e2ee all the clients need to store the keys of all the other clients
# i am really not sure how this will work but we will see
# im half contemplating the sin of not doing e2ee
def clientKeys():
    pass
    
