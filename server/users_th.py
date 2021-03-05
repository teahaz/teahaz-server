#this file should sort out everything related to users
import dbhandler as database
import security_th as security
from logging_th import logger as log



# handle logins
def set_cookie(json_data, email=True):
    email_ad   = json_data.get('email')
    username   = json_data.get('username')
    password   = json_data.get('password')
    chatroomId = json_data.get('chatroom')

    # if the email verification setting is turned off then make email NULL even if the users serts one
    if not email:
        email_ad = None


    # if both email and username are missing then it cannot login
    if not email_ad and not username:
        return 'no email or username sent', 401


    # password has to be at least 10 chars, this will also be checked during sign up
    elif len(password) < 10:
        return 'password must be at least 10 chars', 401


    # check if the username and password combination exists
    response, status = database.checkuser(chatroomId, username=username, email=email_ad, password=password)
    if status != 200:
        return response, status


    #get a randomly generated cookie
    cookie = security.generate_cookie()

    # store the cookies in teh database
    response, status = database.store_cookie(chatroomId, username=username, email=email_ad, new_cookie=cookie)

    # check if storing was succesful
    if status == 200:
        log(level='log', msg=f'"{username}" just logged in')
        return cookie, 200
    else:
        # if not succesful, send the response back to the user
        return response, status


def check_cookie(cookie, data, chatroomId):
    username   = data.get('username')

    # check if username exists
    if not username:
        return False

    # get cookies of user
    stored_cookies = database.get_cookies(chatroomId, username)

    # if the user has no stored cookies
    if not stored_cookies:
        return False

    # check if the cookie of the user is among the stored ones
    if cookie in stored_cookies:
        return True
    else:
        return False


def add_user(username, email, nickname, password, chatroomId):
    if not username  or not nickname or not password or not chatroomId:
        log(level='error', msg="[users/add_user/0] || Some values required by the function were not supplied")
        return "[users/add_user/0] || Internal server error", 500



    # NOTE could later make this a server setting as well
    if len(password) < 10:
        return "[users/add_user/1] || Password has to be at least 10 characters", 400



    # check if the chatroom requires emails
    response, status_code = database.check_settings(chatroomId, "require_email")
    if status_code != 200:
        return response, status_code
    need_email = response



    # if email is needed then make sure the use sends it
    if need_email != False and not email:
        return "[users/add_user/2] || This chatrooms policy requires you to send verify with an email address", 400
    else:
        # make sure email is actually none if the chatroom doesnt require it
        email = None


    #check incase user has already registered
    response, status_code = database.check_user_exists(chatroomId, username, email)
    if status_code != 200:
        return response, status_code


    # dont allow the reuse of usernames or passwords
    if response != False:
        return "[usrs/add_user/3] Username or email has already been registered", 400



    log(level='log', msg=f'new user: "{username}", just registered to chatroom: "{chatroomId}"')
    return "succesfully registered", 200





