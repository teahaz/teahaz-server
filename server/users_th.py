#this file should sort out everything related to users
import dbhandler as database
import security_th as security
from logging_th import logger as log



# handle logins
def set_cookie(json_data, email=True):
    email_ad = json_data.get('email')
    username = json_data.get('username')
    password = json_data.get('password')

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
    response, status = database.checkuser(username=username, email=email_ad, password=password)
    if status != 200:
        return response, status


    #get a randomly generated cookie
    cookie = security.generate_cookie()

    # store the cookies in teh database
    response, status = database.store_cookie(username=username, email=email_ad, new_cookie=cookie)

    # check if storing was succesful
    if status == 200:
        log(level='log', msg=f'"{username}" just logged in')
        return cookie, 200
    else:
        # if not succesful, send the response back to the user
        return response, status


def check_cookie(cookie, data):
    username = data.get('username')

    # check if username exists
    if not username:
        return False

    # get cookies of user
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
    email_ad = json_data.get('email')
    username = json_data.get('username')
    nickname = json_data.get('nickname')
    password = json_data.get('password')


    # username, nickname, and password are required. Thus server will error if not supplied
    if not username or not nickname or not password:
        return 'username, nickname or password empty', 400


    # if the server policy requires an email then it must be sent, and will fail if not
    if email == True and not email_ad:
        return 'This servers policy requires an email address for registering', 400

    # if the server doesnt require and email then it should not be set, and should be cleared just in case stupid users set it
    if email == False:
        email_ad = None


    #check incase user has already registered
    response, status_code = database.check_user_exists(username=username, email=email_ad)
    if status_code != 200:
        return response, status_code


    # response is true, then the user already exists
    if response:
        return "username or email already registered", 400


    # save details of new user
    response, status = database.save_new_user(username=username, email=email_ad, nickname=nickname, password=password)


    # if saving failed
    if status != 200:
        log(level='fail', msg=f'[server/users/register/0] error while saving new user. Traceback: {response}')
        return response, status


    # everything OK, registered
    log(level='log', msg=f'new user: "{username}" just registered')
    return "succesfully registered", 200





