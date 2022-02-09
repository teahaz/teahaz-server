""" Internal functions to handle users """

import dbhandler as database
import security_th as security

# setup logging
from logging_th import logger
LOG = logger()


def add_user(chatroom_id: str, username: str, nickname: str, password: str):
    """ Add user to chatroom. """

    # make sure password is long enough
    pwlength, status = database.check_settings(chatroom_id, "min_password_length")
    if status != 200:
        return "Internal server error while checking password length setting.", 500

    if len(password) < pwlength:
        return f"Password too short. According to chatroom settings your password has to be at least {pwlength} characters long.", 400


    # save user creds
    user_data, status = database.write_user(chatroom_id, username, nickname, password)
    if status != 200:
        return user_data, status


    return user_data, 200


def auth_user(chatroom_id: str, username: str, password: str):
    """ Authenticate user """

    user_data, status = database.fetch_user(chatroom_id, username, include_private=True)
    if status != 200:
        return user_data, status

    correct_password = user_data['private']['password']

    if not security.checkpw(password, correct_password):
        return "Password is incorrect", 401

    return "Logged in!", 200


def set_cookie(chatroom_id: str, username: str):
    """ Generate and store a cookie for a user """
    cookie = security.gen_uuid()

    if not chatroom_id or not username:
        return "internal server error while setting cookies", 500

    res, status = database.store_cookie(chatroom_id, username, cookie)
    if status != 200:
        return res, status

    return cookie, 200


def check_cookie(chatroom_id: str, cookie: str, username: str):
    """ Check if a cookie value is valid for the specified user """

    if not username or not cookie:
        print('username: ',username , type(username))
        print('cookie: ',cookie , type(cookie))
        return False


    cookies, status = database.get_cookies(chatroom_id, username, cookie)
    if status != 200:
        return False

    for i in cookies:
        if i == cookie:
            return True

    return False
