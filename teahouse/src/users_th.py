""" Internal functions to handle users """

import dbhandler as database
import security_th as security

# setup logging
from logging_th import logger
global log
log = logger()


def add_user(chatroomID: str, username: str, nickname: str, password: str):
    """ Add user to chatroom. """


    # make sure password is long enough
    pwlength, status = database.check_settings(chatroomID, "min_password_length")
    if status != 200:
        return "Internal server error while checking password length setting.", 500

    if len(password) < pwlength:
        return f"Password too short. According to chatroom settings your password has to be at least {pwlength} characters long.", 400


    # save user creds
    res, status = database.write_user(chatroomID, username, nickname, password)
    if status != 200:
        return res, status


    return username, 200



def auth_user(chatroomID: str, username: str, password: str):
    """ Authenticate user """

    info, status = database.fetch_user_creds(chatroomID, username)
    if status != 200:
        return info, status

    if not security.checkpw(password, info['password']):
        return "Password is incorrect", 401

    return "Logged in!", 200



def set_cookie(chatroomID: str, username: str):
    """ Generate and store a cookie for a user """
    cookie = security.gen_uuid()

    res, status = database.store_cookie(chatroomID, username, cookie)
    if status != 200:
        return res, status

    return cookie, 200


def check_cookie(chatroomID: str, cookie: str, username: str):
    if not username or not cookie:
        print('username: ',username , type(username))
        print('cookie: ',cookie , type(cookie))
        return False

    cookies, status = database.get_cookies(chatroomID, username, cookie)
    if status != 200:
        return False


    for i in cookies:
        if i == cookie:
            return True

    return False


