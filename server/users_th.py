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




def check_cookie(request):
    cookie = request.cookies.get('access')
    json_data = request.headers
    userId = json_data['userId']
    print('userId: ',userId , type(userId))


    print(database.get_cookies(userId))

    return True
