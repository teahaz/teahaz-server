# this file should sort out everything related to users

#globls
import sqlite3

# local
import security_l as security
import dbhandler as database
from logging_l import logger as log



def assign_cookie(json_data):
    # get the data needed for this function
    try:
        username = json_data['username']
        password = json_data['password']
        twofactor = json_data['2fa']
    except:
        log(level='warning', msg='[server/users/login/0] one or more of the required arguments are not supplied')
        return 'one or more of the required arguments are not supplied, needed=[username, password, 2fa]', 400

    # check that all data is given
    if len(username) == 0:
        return 'no username sent', 400
    # password has to be at least 10 chars, this will also be checked during sign up
    elif len(password) < 10:
        return 'invalid password length', 400
    # later we will need 2fa
    elif twofactor.upper() != "false".upper():
        return "invalid response sent for 2fa. Can only be boolian 'true' or 'false'", 501

    # must hash
    password = security.hashpw(password)

    # check if the username and password combination exists
    if not database.checkuser(username, password):
        return "username or password incorrect, login failed", 401

    # we dont yet have 2fa
    if twofactor.upper() == "true".upper():
        return "this feature has not yet been implemented", 501



    #method to get cookie
    # i think i need to implement the master password first


