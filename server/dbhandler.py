import os
import sys
import json
import time
import uuid
import base64
import sqlite3


import security_th as security
from logging_th import logger as log



# base64 encode messages
def b(a):
    return base64.b64encode(str(a).encode('utf-8')).decode('utf-8')


# base64 decode messages
def d(a):
    return base64.b64decode(str(a).encode('utf-8')).decode('utf-8')



def database_execute(chatroom='', statement='', variables=()):
    chatroom = chatroom.strip(' ')
    res, status = security.check_uuid(chatroom)
    if status != 200:
        return res, status



    if not os.path.exists(f'storage/chatrooms/{chatroom}/main.db'):
        return "[database/database_execute/1] || Chatroom does not exist", 500


    try:
        db_connection = sqlite3.connect(f'storage/chatrooms/{chatroom}/main.db')
        db_cursor = db_connection.cursor()
        db_cursor.execute(statement, variables)
        data = db_cursor.fetchall()
        db_connection.commit()
        db_connection.close()

    except Exception as e:
        return f"[database/database_execute/2] || Database operation failed: {e}", 500


    return data, 200



#=================================================== init ==================================================



# create and setup chatroom.db
def init_chat(chatroomId, chatroom_name):
    log(level='log', msg=f"[dbhandler/init_chat/0] || creating chatroom: {chatroomId}")

    try:
        chatroom_name = b(chatroom_name)
    except Exception as e:
        log(level='error', msg=f"[dbhandler/init_chat/1] || could not encode chatroom name: {e}")
        return "[dbhandler/init_chat/1] || Chatroom name could not be encoded: Invalid data", 400

    # create users table
    #                          |                       auth                          | settings | perms |
    sql = "CREATE TABLE users ('username', 'email', 'nickname', 'password', 'cookies', 'colour', 'admin')"
    data, status_code = database_execute(chatroomId, sql, ())
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/init_chat/2] || {data}")
        return "[dbhandler/init_chat/2] || Failed to create chatroom: Internal datase error", 500


    # create invites table
    sql = "CREATE TABLE invites ('inviteId', 'expr_time', 'uses')"
    data, status_code = database_execute(chatroomId, sql, ())
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/init_chat/3] || {data}")
        return "[dbhandler/init_chat/3] || Internal database error", status_code


    # create messages table
    #                          |                    general                  | type | message |          files         |
    sql = "CREATE TABLE messages ('time', 'messageId', 'replyId', 'username', 'type', 'message', 'fileId', 'filename')"
    data, status_code = database_execute(chatroomId, sql, ())
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/init_chat/4] || {data}")
        return "[dbhandler/init_chat/4] || Failed to create chatroom: Internal datase error", 500


    # create settings table
    #                             |       setting general       | perms to change |
    sql = "CREATE TABLE settings ('setting_name', 'setting_value', 'need_admin')"
    data, status_code = database_execute(chatroomId, sql, ())
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/init_chat/5] || {data}")
        return "[dbhandler/init_chat/5] || Failed to create chatroom: Internal datase error", 500


    # set the chatroom name
    sql = "INSERT INTO settings VALUES (?, ?, ?)"
    data, status_code = database_execute(chatroomId, sql, ("chatroom_name", chatroom_name, True))
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/init_chat/6] || Failed to set chatroom name {data}")
        return "[dbhandler/init_chat/6] || Failed to create chatroom: Internal datase error", 500


    # set use email to false by default
    sql = "INSERT INTO settings VALUES (?, ?, ?)"
    data, status_code = database_execute(chatroomId, sql, ("require_email", False, True))
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/init_chat/7] || Failed to set settting 'require_email': {data}")
        return "[dbhandler/init_chat/7] || Failed to create chatroom: Internal datase error", 500



    return "OK", 200



#=================================================== !init =================================================
#===================================================  auth =================================================



# save details of a new user
#'username', 'email', 'nickname', 'password', 'cookies', 'colour', 'admin'
def save_new_user(username, nickname, password, chatroomId, email=None, admin=False):
    if not username or not nickname or not password or not chatroomId:
        log(level='error', msg=f"[dbhandler/save_new_user/0] || some required data was not passed to the function")
        return "[server/dbhandler/save_new_user/0] || Failed to register user: Internal server error", 500



    # encode data
    try:
        # encode data
        username = b(username)
        nickname = b(nickname)

        # email is not always compulsary
        if email != None:
            email = b(email)

        # hashpw
        password = b(security.hashpw(password))

        # save empty list of user cookies
        cookie = b(json.dumps([]))


        # colour is None by default
        colour = None


    # could not encode data
    except Exception as e:
        log(level='error', msg=f"[server/dbhandler/save_new_user/1] || Failed to encode/hash data\nTraceback: {e}")
        return "[server/dbhandler/save_new_user/1] || Failed to register user: Internal server error", 500



    # save user in database. format = 'username', 'email', 'nickname', 'password', 'cookies', 'colour', 'admin'
    sql = "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)"
    data, status_code = database_execute(chatroomId, sql, (username, email, nickname, password, cookie, colour, admin))
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/save_new_user/2] || Error occured while adding user to database: {data}")
        return "[dbhandler/save_new_user/2] || Failed to register user: Internal datase error", 500


    # everything okay
    return "OK", 200



# check if a username or email already exists (main purpose is to not register the same user 2x)
def check_user_exists(chatroomId, username=None, email=None):
    try:
        if username: username = b(username)
        if email: email = b(email)

    except:
        return "[server/dbhanler/check_user_exitst/0] username or email corrupt", 400


    # run slightly different checks depending on the data supplied
    if username and email:
        sql = "SELECT * FROM users WHERE username = ? OR email = ?"
        variables = (username,email)

    elif username and not email:
        sql = "SELECT * FROM users WHERE username = ? "
        variables = (username,)

    elif not username and email:
        sql = "SELECT * FROM users WHERE email = ?"
        variables = (email,)




    data, status_code = database_execute(chatroomId, sql, variables)
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/check_user_exitst/1] || Database operation failed {data}")
        return "[dbhandler/check_user_exitst/1] || Could not verify user: Internal datase error", 500



    if len(data) > 0:
        return True, 200
    else:
        return False, 200



# check username and password of user
def checkuser(chatroomId, username=None, email=None, password=None):
    if not password:
        return "[server/checkuser/0] || Login failed. no password sent", 400


    # email takes priority over username, so if email is present then use that for login
    if email != None:
        key = b(email)
        using = 'email'


    # if no email then login with username
    else: 
        key = b(username)
        using = 'username'


    # get password
    sql = f"SELECT password FROM users WHERE {using} = ?"
    data, status_code = database_execute(chatroomId, sql, (key,))
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/checkuser/1] || Failed to check user login: {data}")
        return "[dbhandler/checkuser/1] || Checking user failed: Internal database error", 500



    # if the user has a password, unwap it
    if len(data) > 0:
        storedPassword = d(data[0][0])
    else:
        return "[dbhandler/checkuser/2] || Login failed. Unrecognized username. Are you registered?", 401


    # check if the password is correct
    if security.checkpw(password, storedPassword):
        return "OK", 200
    else:
        return "[dbhandler/checkuser/3] || Login failed. Username/email or password is incorrect!", 401



# add a cookie to the users list of cookies
def store_cookie(chatroomId, username=None, email=None, new_cookie=None):
    if new_cookie == None: # check if the function was called without cookies, this should only happen if the sever code is broken
        log(level="error", msg=f'[server/dbhandler/store_cookie/0] function was called without a cookie supplied to it')
        return "[server/dbhandler/store_cookie/0] || Failed to verify user: Internal server error", 500


    # email takes priority over username, so if email is present then use that as the key
    if email != None:
        key = b(email)
        using = 'email'


    # if no email then key is username
    else: 
        key = b(username)
        using = 'username'



    sql = f"SELECT cookies FROM users WHERE {using} = ?"
    data, status_code = database_execute(chatroomId, sql, (key,))
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/store_cookie/1] || Failed to get cookies from database: {data}")
        return "[dbhandler/store_cookie/1] || login failed: Internal database error", 500

    cookies = data



    # al users should have at least '[]' stored as cookes, if they dont then the database is corrupted somehow
    if len(cookies) == 0:
        log(level='error', msg=f'[dbhandler/store_cookie/2] || user does not exists or did not get initialized properly\n (database cookies entry doesnt exist)')
        return "[dbhandler/store_cookie/2] || Login failed: Internal database error", 500


    # add new cookie to cookies list
    ## cookies are being stored as a list that has been converted to string, this makes it easy to add new cookies
    try:
        #decode
        cookies = d(cookies[0][0])

        #append
        cookies = json.loads(cookies)
        cookies.append(new_cookie)
        cookies = json.dumps(cookies)

        # encode
        cookies = b(cookies)


    # if the cookies cannot be decoded/encoded than the data is malformed, which is a server issue
    except:
        log(level='error', msg=f'[dbhandler/store_cookie/3] || malformed cookie data in databse')
        return "[dbhandler/store_cookie/3] || Login failed: Internal database error", 500



    sql = f'UPDATE users SET cookies = ? WHERE {using} = ?'
    data, status_code = database_execute(chatroomId, sql, (cookies, key))
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/store_cookie/3] || Failed update user cookies: {data}")
        return "[dbhandler/store_cookie/1] || login failed: Internal database error", 500


    # everything worked out fine
    return "OK", 200



# return all active cookies of a user
def get_cookies(chatroomId, username):
    try:
        username = b(username)
    except Exception as e:
        log(level='error', msg=f"[dbhandler/get_cookies/0] || Could not encode username: {e}")
        return "[dbhandler/get_cookies/0] username could not be encoded", 400


    # get all  stored cookies of the user
    sql = f"SELECT cookies FROM users WHERE username = ?"
    data, status_code = database_execute(chatroomId, sql, (username,))
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/get_cookies/1] || Failed to get cookies from database: {data}")
        return "[dbhandler/get_cookies/1] || Failed to verify user: Internal database error", 500


    # cookies are stored in a base64 encoded str(list)
    if len(data) == 0:
        return False


    # decode and load the data as json
    try:
        data = d(data)
        data = json.loads(data)
    except:
        log(level='error', msg=f'[server/dbhandler/get_cookies/2] failed to process cookie data of user {username}\n Data is probably corrupted')
        return False

    return data



#=================================================== !auth =================================================
#============================================== other user stuff ===========================================



# get the nickname of a user
def get_nickname(chatroomId, username_encoded):
    sql = f"SELECT nickname FROM users WHERE username = ?"
    data, status_code = database_execute(chatroomId, sql, (username_encoded,))
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/get_nickname/0] || Failed to get nickname: {data}")
        return "ERR: could not get nickname"


    # sqlite3 wraps the username in a tuple inside of a list
    try:
        nickname = d(data[0][0])
    except Exception as e:
        log(level='warning', msg=f"[dbhandler/get_nickname/1] || could not get users nickname: {e}")
        nickname = "ERR: could not get nickname"


    return nickname



# check the permissons of one user
def check_perms(username, chatroomId, permission="admin"):
    try:
        username   = b(username)


    except Exception as e:
        log(level="warning", msg=f"[dbhandler/check_perms/0] ||  could not encode data sent from user\n Traceback: {e}")
        return "[dbhandler/check_perms/0] || Failed to check permission: Internal server error"


    # the option needs to be in this list to pass, this should avoid arbitrary things bing injected into the sql statement
    userPerms = [ "admin" ] # NOTE this cold be global, idk yet
    if permission not in userPerms:
        log(level='error', msg="[dbhandler.py/check_perms/1] attemted to check invalid permission. Make sure you are only checking things in userPerms list")
        return "Attempted to check invialid permission", 500


    sql = f"SELECT * FROM users WHERE username = ? and {permission} = true"
    data, status_code = database_execute(chatroomId, sql, (username,))
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/check_perms/1] || Databse opertion, getting permission failed: {data}")
        return "[dbhandler/check_perms/1] || Failed to cehck permission: Internal database error", 500


    if len(data) == 0 or not data:
        return False, 200


    return True, 200



#============================================= !other user stuff ===========================================
#================================================== chatroom ===============================================




# check the permissons of one user
def check_settings(chatroomId, setting):
    sql = f"SELECT setting_value FROM settings WHERE setting_name = ?"
    data, status_code = database_execute(chatroomId, sql, (setting,))
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/check_settings/0] || Databse opertion, getting setting value failed: {data}")
        return "[dbhandler/check_settings/0] || Internal database error while checking chatroom settings", 500

    try:
        # unwrap data
        value = data[0][0]

        # if its a string then its encoded
        if type(value) == str:
            value = d(value)


    except Exception as e:
        log(level='error', msg=f"[dbhandler/check_settings/1] || An error occured while formatting setting value: {data}\n TRACEBACK: {e}")
        return "[dbhandler/check_settings/1] || Internal server error while checking chatroom settings", 500


    return value, 200




#================================================== !chatroom ==============================================
#=================================================== invites ===============================================




def save_invite(chatroomId, inviteId, expr_time, uses):
    if not chatroomId or not inviteId or not expr_time or not uses:
        log(level='error', msg="[dbhandler.py/save_invite/0] || missing arguments to save_invite function")
        return "internal server error: missing arguments", 500


    # encode data: no sqli pls
    try:
        inviteId   = b(inviteId)
        # expr_time and uses are not encoded so we can do cool sql statements


    # could not encode the data for some reason
    except Exception as e:
        log(level='error', msg="[dbhandler.py/save_invite/1] || Error occured while encoding data: {e}")
        return "[dbhanler/save_invite/1] || failed to encode data: Internal server error", 500



    # save inivte
    sql = f"INSERT INTO invites VALUES (?, ?, ?)"
    data, status_code = database_execute(chatroomId, sql, (inviteId, expr_time, uses))
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/save_invite/2] || Failed to save invite in datbase: {data}")
        return "[dbhandler/save_invite/3] || Failed to save invite in database: Internal database error", 500


    # ok
    return "OK", 200



# verify and use invite
def use_invite(chatroomId, inviteId):
    if not inviteId:
        log(level='error', msg="[dbhandler.py/use_invite/0] || missing arguments to function")
        return "internal server error: missing arguments", 500



    # encode inviteId
    try:
        inviteId = b(inviteId)

    except Exception as e:
        log(level='warning', msg="[dbhandler.py/use_invite/1] inviteId could not be encoded\n Traceback: {e}")
        return "inviteID format incorrect", 400



    # get all invite data from database
    # NOTE  TODO IMPORTANT: inivte time is not checked rn
    #sql = f"SELECT * FROM invites WHERE inviteId = ? AND (expr_time > ? OR expr_time = 0)", (inviteId, str(int(time.time())))
    sql = f"SELECT * FROM invites WHERE inviteId = ? "
    data, status_code = database_execute(chatroomId, sql, (inviteId,))
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/use_invite/2] || Database operation, gettting invite data failed: {data}")
        return "[dbhandler/use_invite/2] || Could not check invite: Internal database error", 500

    invite = data



    # check if there weren't any valid invites
    if len(invite) == 0:
        return "[dbhandler/use_invite/3] || Invite ID incorrect or expired", 400



    # get data from the invite
    try:
        invite = invite[0]
        uses = int(invite[2])



    # somethings wrong with the database format
    except Exception as e:
        log(level='error', msg=f"[dbhandler/use_invite/4] || error occured while processing invite database possibly corrupted\nTraceback: {e}")
        return "Internal databse error: could not process data from databse", 500



    # cehck if the invite is overused
    if uses > 0:
        uses = uses - 1
    else:
        return "[dbhandler/use_invite/5] || invite cannot be used as it has exeeded its maximum capacity", 403



    sql = f"UPDATE invites SET uses = ? WHERE inviteId = ?"
    data, status_code = database_execute(chatroomId, sql, (str(uses), inviteId))
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/use_invite/6] || Could not return decremented uses value to database: {data}")
        return "[dbhandler/use_invite/6] || Could not check invite: Internal database error", 500



    # all is well
    return "OK", 200




#=================================================== !invites ==============================================
#=================================================== messages ==============================================



# save a message in the database (both texts and files)
def save_in_db(time, messageId, username, chatroomId, message_type, replyId=None, message=None, fileId=None, filename=None ):
    if not time  or not messageId  or not username  or not chatroomId  or not message_type :
        # making sure that all values that are needed exist
        log(level='error', msg='[dbhandler/save_in_db/0] || one or more of the required fields passed to function "save_in_db" are not present ')
        return "[dbhandler/save_in_db/0] || internal server error: missing arguments", 500


    # encode cumpolsary values
    try:
        username = b(username)
        messageId = b(messageId)
        message_type = b(message_type)


    # if this fails its bc the user sent bad data
    except Exception as e:
        log(level='error', msg=f'[dbhandler/save_in_db/1] || could not encode some data: {e}')
        return "[dbhandler/save_in_db/1] || corrupted data sent to server", 400


    # encode non compulsary values
    if message: message = b(message)
    if filename: filename = b(filename)


    # validate, and encode uuids
    if fileId:
        res, status = security.check_uuid(fileId)
        if status != 200:
            return res, status

        if filename: filename = b(filename)
        else: return "[database/save_in_db/2] || Invalid uuid sent for filename", 400


    if replyId:
        res, status = security.check_uuid(replyId)
        if status != 200:
            return res, status

        if replyId: replyId = b(replyId)
        else: return "[database/save_in_db/2] || Invalid uuid sent for replyId", 400




    sql = f"INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    variables = (time, messageId, replyId, username, message_type, message, fileId, filename)
    data, status_code = database_execute(chatroomId, sql, variables)
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/save_in_db/2] || Failed to save message: {data}")
        return "[dbhandler/save_in_db/2] || Failed to send message: Internal datase error", 500



    # all is well
    return "OK", 200



# get all messages from database since `last_time`
def get_messages_db(chatroomId, last_time=0):
    sql = "SELECT * FROM messages WHERE time >= ?"
    data, status_code = database_execute(chatroomId, sql, (last_time,))
    if status_code != 200:
        log(level='error', msg=f"[dbhandler/get_messages_db/0] || Could not get messages from db: {data}")
        return "[dbhandler/get_messages_db/0] || Failed to get messages: Internal database error", 500



    # sqlite returns a list of lists, we should convert this back to json
    json_data = []

    # format messages for returning
    # try:
    if True:
        for element in data:
            nickname = get_nickname(chatroomId, element[3])

            # get compulsary data, all but time need to be decoded
            send_time = element[0]
            messageId = d(element[1])
            username  = d(element[3])
            msg_type  = d(element[4])

            # get optional data, they may or may not be present
            message = element[5]
            if message: message = d(message)
            fileId = element[6]
            if fileId: fileId = d(fileId)
            filename = element[7]
            if filename: filename = d(filename)
            replyId   = element[2]
            if replyId: replyId = d(replyId)

            # make return dict
            a = {
                'time': send_time,
                'messageId': messageId,
                'replyId' : replyId,
                'username': username,
                'nickname': nickname,
                'type': msg_type,
                'message': message,
                'fileId': fileId,
                'filename': filename
                    }

            # add to list
            json_data.append(a)


    # message format error
    # except Exception as e:
    else:
        # log(level='error', msg=f"[dbhandler/get_messages/1] || Error while formatting message data: {e}")
        return "[dbhandler/get_messages/1] || Could not format data: Internal databse error", 500


    # all is well
    return json_data, 200




#================================================== !messages ==============================================
#=================================================== testing ================-==============================



def check_databses():
    log(level='log', msg='running system checks')


    # check if storage folder exists
    log(level='log', msg='checking storage folder')

    # check if folder exists, and try to create it if not
    if not os.path.isdir("storage/"):
        try:
            log(level='warning', msg='[health check] creating storage folder')
            os.mkdir("storage")

        except Exception as e:
            return f"could not create storage folder: {e}\n Please make sure you have to correct permissions", 500

    if not os.path.isdir("storage/chatrooms"):
        try:
            log(level='warning', msg='[health check] creating chatrooms folder')
            os.mkdir("storage/chatrooms")

        except Exception as e:
            return f"could not create chatrooms folder: {e}\n Please make sure you have to correct permissions", 500


    for chatroom in os.listdir('storage/chatrooms/'):
        log(level='log', msg=f'checking chatroom: {chatroom}')

        if not os.path.exists(f"storage/chatrooms/{chatroom}/main.db"):
            log(level="error", msg=f'[healthcheck/1] || chatroom: "{chatroom}" does not have a database file')
            # returning 200 bc this is not bad enough to kill the server
            return f"{chatroom} does not have a database file", 200

        sql = "SELECT * FROM users"
        data, status_code = database_execute(chatroom, sql, ())
        if status_code != 200:
            log(level="error", msg=f'[healthcheck/1] || chatroom: "{chatroom}" database is corrupted: {data}')
            # returning 200 bc this is not bad enough to kill the server
            return f"{chatroom} database is corrupted: {data}", 200

        sql = "SELECT * FROM invites"
        data, status_code = database_execute(chatroom, sql, ())
        if status_code != 200:
            log(level="error", msg=f'[healthcheck/1] || chatrom: "{chatroom}" database is corrupted: {data}')
            # returning 200 bc this is not bad enough to kill the server
            return f"{chatroom} database is corrupted: {data}", 200

        sql = "SELECT * FROM messages"
        data, status_code = database_execute(chatroom, sql, ())
        if status_code != 200:
            log(level="error", msg=f'[healthcheck/1] || chatroom: "{chatroom}" database is corrupted: {data}')
            # returning 200 bc this is not bad enough to kill the server
            return f"{chatroom} database is corrupted: {data}", 200

        sql = "SELECT * FROM settings"
        data, status_code = database_execute(chatroom, sql, ())
        if status_code != 200:
            log(level="error", msg=f'[healthcheck/1] || chatroom: "{chatroom}" database is corrupted: {data}')
            # returning 200 bc this is not bad enough to kill the server
            return f"{chatroom} database is corrupted: {data}", 200




    log(level='success', msg='[health check] System is healthy :)')
    return "OK", 200
