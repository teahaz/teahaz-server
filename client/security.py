# explination of all this shit
# 1, session is manditory
# 2, the first time the user connects [s]he will give a username and a password, a hashed password and a plain text username will be stored in the `path_to_saved_creds` 
    # so password_auth== True when the user has not been authenticated on this device yet(does not have a creds file), otherwhise it should be false
# 3, 4 should be obvi, they are only taken into account if password_auth is True
#5 is the path to the creds file, ofc this could be anywhere i just set './.creds' as a default. you can change it however you like, knock yourself out
def authenticate(session, password_auth=True, username="", password="", path_to_saved_creds="./.creds"):
    pass






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
def clientKeys();
    pass
    
