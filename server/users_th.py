#this file should sort out everything related to users

#globls
import sqlite3

# local
import dbhandler as database
import security_th as security
from logging_th import logger as log



def set_cookie(json_data):
    # get the data needed for this function
    try:
        userId = json_data['userId']
        password = json_data['password']
    except:
        log(level='warning', msg='[server/users/login/0] one or more of the required arguments are not supplied')
        return 'one or more of the required arguments are not supplied, needed=[username, password]', 400

    # check that all data is given
    if len(userId) == 0:
        return 'no username sent', 400
    # password has to be at least 10 chars, this will also be checked during sign up
    elif len(password) < 10:
        return 'password must be at least 10 chars', 400

    # check if the username and password combination exists
    if not database.checkuser(userId, password):
        return "username or password incorrect, login failed", 401

    cookie = security.generate_cookie()

    database.store_cookie(userId, cookie)

    return cookie, 200




def check_cookie(cookie, data):
    userId = data['userId']
    stored_cookies = database.get_cookies(userId)

    if cookie in stored_cookies:
        return True
    else:
        return False



def add_user(json_data):
    log(level="log", msg="adding new user")
    log(level="warning", msg="rn new users are not checked and not verified, users can be added freely")

    userId = security.generate_userId()
    try:
        nickname = json_data['nickname']
        password = json_data['password']
    except:
        log(level='warning', msg='[server/users/register/0] one or more of the required arguments are not supplied')
        return 'username or password not supplied', 400

    if not nickname or not password:
        log(level='warning', msg='[server/users/register/1] one or more of the required arguments are not supplied')
        return 'username or password not supplied', 400

    if not userId:
        log(level='fail', msg='[server/users/register/2] did not create userId')
        return "internal server error", 500


    if not database.save_new_user(userId, nickname, password):
        log(level='fail', msg='[server/users/register/3] could not save user for some reason')
        return "internal server error", 500


    return "succesfully registered", 200





