"this file should sort out everything related to users"

import time
import json

import dbhandler as database
import security_th as security
from logging_th import logger as log



# handle logins
def set_cookie(json_data, chatroomId):
    email_ad   = json_data.get('email')
    username   = json_data.get('username')
    password   = json_data.get('password')


    # check if email verification is available, if not then clear email variable just in case
    response, status_code = database.check_settings(chatroomId, "require_email")
    if status_code != 200:
        return response, status_code
    need_email = response
    if not need_email:
        email_ad = None


    # if both email and username are missing then it cannot login
    if not email_ad and not username:
        return '[users/set_cookie/0] || no email or username sent', 401


    # password has to be at least 10 chars, this will also be checked during sign up
    elif len(password) < 10:
        return '[users/set_cookie/1] || password must be at least 10 chars', 401


    # check if the username and password combination exists
    response, status = database.checkuser(chatroomId, username=username, email=email_ad, password=password)
    if status != 200:
        return response, status


    #get a randomly generated cookie
    cookie = security.gen_uuid()


    # store the cookies in teh database
    response, status = database.store_cookie(chatroomId, username=username, email=email_ad, new_cookie=cookie)


    # check if storing was succesful
    if status == 200:
        log(level='log', msg=f'[users/set_cookie/2] || "{username}" just logged in')
        # return a cookie and the chatname, that will be expanded later
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
        return "[usrs/add_user/3] || Username or email has already been registered", 400


    response, status_code = database.save_new_user(username, nickname, password, chatroomId, email, admin=True)
    if status_code != 200:
        return response, status_code



    # log new user
    response , status_code = database.save_in_db(
                                    chatroomId   = chatroomId,
                                    time         = time.time(),
                                    messageId    = security.gen_uuid(),
                                    kId          = None,
                                    replyId      = None,
                                    username     = username,
                                    message_type = 'system',
                                    message      = security.encode(json.dumps({ "action": "New user registered!", }))
                                    )
    if status_code != 200:
        return response, status_code

    log(level='log', msg=f'[users/add_user/4] || new user: "{username}", just registered to chatroom: "{chatroomId}"')
    return "succesfully registered", 200



def process_invite(json_data, chatroomId):
    username   = json_data.get('username')
    email      = json_data.get('email')
    nickname   = json_data.get('nickname')
    password   = json_data.get('password')
    inviteId   = json_data.get('inviteId')



    # make sure we got all the data
    if not username or not nickname or not password or not inviteId or not chatroomId:
        return "[users/process_invite/0] || one or more of the required arguments were not supplied. Required=[username, nickname, password, inviteId, chatroomId]", 400


    if len(password) < 10:
        return "[users/process_invite/1] || Password has to be at least 10 characters", 400



    # we need to sanitize
    res, status = security.check_uuid(inviteId)
    if status != 200:
       return res, status



    # check if the chatroom requires emails
    response, status_code = database.check_settings(chatroomId, "require_email")
    if status_code != 200:
        return response, status_code
    need_email = response



    # if email is needed then make sure the use sends it
    if need_email != False and not email:
        return "[users/process_invite/2] || This chatrooms policy requires you to send verify with an email address", 400
    else:
        # make sure email is actually none if the chatroom doesnt require it
        email = None



    #check incase user has already registered
    response, status_code = database.check_user_exists(chatroomId, username, email)
    if status_code != 200:
        return response, status_code

    # dont allow the reuse of usernames or passwords
    if response != False:
        return "[usrs/process_invite/3] || Username or email has already been registered", 400



    # check if invite is valid, and decrement uses
    response, status_code = database.use_invite(chatroomId, inviteId)
    if status_code != 200:
       return response, status_code



    # save a user to the database
    response, status_code = database.save_new_user(username, nickname, password, chatroomId, email, admin=False)
    if status_code != 200:
       return response, status_code


    # log new user
    response , status_code = database.save_in_db(
                                    chatroomId   = chatroomId,
                                    time         = time.time(),
                                    messageId    = security.gen_uuid(),
                                    kId          = None,
                                    replyId      = None,
                                    username     = username,
                                    message_type = 'system',
                                    message      = json.dumps({
                                            "action": "New user registered!",
                                        })
                                    )
    if status_code != 200:
        return response, status_code


    # get the name of the chat
    chatname, status_code = database.check_settings(chatroomId, "chatroom_name")
    if status_code != 200:
        return chatname, status_code


    # create object for returning
    chat_obj = {
           "name": chatname,
           "chatroom": chatroomId
           }


    # bye
    return chat_obj, 200







