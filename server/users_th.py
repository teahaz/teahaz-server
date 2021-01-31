#this file should sort out everything related to users

#globls
import sqlite3

# local
import dbhandler as database
import security_th as security
from logging_th import logger as log



# handle logins
def set_cookie(json_data, email=True):
    # get the data needed for this function

    email_ad = json_data.get('email')
    username = json_data.get('username')
    password = json_data.get('password')

    # if email verification is off then null email even if a user sends one
    if not email:
        email_ad = None

    # if both email and username are missing then it cannot log in
    if not email_ad and not username:
        log(level='warning', msg=f'[server/users_th/set_cookie/0] no email or username sent')
        return 'no email or username sent', 400

    # password has to be at least 10 chars, this will also be checked during sign up
    elif len(password) < 10:
        log(level='warning', msg=f'failed login from user: {username}')
        return 'password must be at least 10 chars', 400

    # check if the username and password combination exists
    if not database.checkuser(username=username, email=email_ad, password=password):
        log(level='warning', msg=f'failed login from user: {username}')
        return "username/email or password incorrect, login failed", 401

    cookie = security.generate_cookie()

    database.store_cookie(username=username, email=email_ad, new_cookie=cookie)

    return cookie, 200




def check_cookie(cookie, data):
    username = data['username']
    stored_cookies = database.get_cookies(username)

    # if the user has no stored cookies
    if not stored_cookies:
        return False

    # check if the cookie of the user is among the stored ones
    if cookie in stored_cookies:
        return True
    else:
        return False



def add_user(json_data, email=True):
    log(level="log", msg="adding new user")
    log(level="warning", msg="rn new users are not checked and not verified, users can be added freely")

    email_ad = json_data.get('email')
    username = json_data.get('username')
    nickname = json_data.get('nickname')
    password = json_data.get('password')

    if not username or not nickname or not password:
        log(level='warning', msg='[server/users/register/1] one or more of the required arguments are not supplied')
        return 'username, nickname or password not supplied', 400

    if email == True and not email_ad:
        log(level='warning', msg='[server/users/register/1] email not sent')
        return 'thi servers policy requires you to send an email address', 400


    if not database.save_new_user(username=username, email=email_ad, nickname=nickname, password=password):
        log(level='fail', msg='[server/users/register/2] could not save user for some reason')
        return "internal server error", 500


    return "succesfully registered", 200





