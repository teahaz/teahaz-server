""" Internal functions to handle users """

import dbhandler as database
import security_th as security

# setup logging
from logging_th import logger
global log
log = logger()


def add_user(username: str, password: str, chatroomID: str):
    """ Add user to chatroom. """


    # make sure password is long enough
    pwlength, status = database.check_settings(chatroomID, "min_password_length")
    if status != 200:
        return "Internal server error while checking password length setting.", 500

    if len(password) < pwlength:
        return f"Password too short. According to chatroom settings your password has to be at least {pwlength} characters long.", 400


    # save user creds
    userID, status = database.write_user(chatroomID, username, password)
    if status != 200:
        return userID, status


    return userID, 200



def auth_user(chatroomID: str, userID: str, password: str):
    """ Authenticate user """

    info, status = database.fetch_user_creds(chatroomID, userID)
    if status != 200:
        return info, status

    if not security.checkpw(password, info['password']):
        return "Password is incorrect", 401

    return "Logged in!", 200



def set_cookie(chatroomID: str, userID: str):
    """ Generate and store a cookie for a user """
    cookie = security.gen_uuid()

    res, status = database.store_cookie(chatroomID, userID, cookie)
    if status != 200:
        return res, status

    return cookie, 200


def check_cookie(chatroomID: str, cookie: str, userID: str):
    if not userID or not cookie:
        print('userID: ',userID , type(userID))
        print('cookie: ',cookie , type(cookie))
        return False

    cookies, status = database.get_cookies(chatroomID, userID, cookie)
    if status != 200:
        return False


    for i in cookies:
        if i == cookie:
            return True

    return False


