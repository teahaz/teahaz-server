import os
import sys
import json
import uuid
import base64
import sqlite3


import security_th as security
from logging_th import logger as log



#--------------------------------------------- encoding ---------------------------------------------
# encode/decode shit to stop any sort of injection
def b(a):
    return base64.b64encode(str(a).encode('utf-8')).decode('utf-8')

def d(a):
    return base64.b64decode(str(a).encode('utf-8')).decode('utf-8')




################################################# user stuff ###############################################
#-------------------------------------------------  init ----------------------------------------------------
# creates a users database
def init_user_db():
    if os.path.exists(f'storage/users.db'):
        log(level='fail', msg=f'[server/dbhandler/init_user_db] cannot redifine userdb')
        return False
    else:
        log(level='warning', msg=f"creating usersdb")

    db_connection = sqlite3.connect(f'storage/users.db')
    db_cursor = db_connection.cursor()
    # cookies is a list of cookies, that is turned into a string with json, and base64/hex encoded
    db_cursor.execute(f"CREATE TABLE users ('username', 'email', 'nickname', 'password', cookies)")
    db_connection.commit()
    db_connection.close()
    return True


#------------------------------------------------  testing --------------------------------------------------
# tis only for testinerror
def get_all_users():
    db_connection = sqlite3.connect(f'storage/users.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"SELECT * FROM users")
    a = db_cursor.fetchall()
    db_connection.close()
    for i in a:
        print(i)


#-------------------------------------------------- access control ------------------------------------------
def save_new_user(username=None, email=None, nickname=None, password=None):
    try:

        # encode email if compulsary
        if email != None:
            email = b(email)


        # encode username and nickname (no injection pls)
        username = b(username)
        nickname = b(nickname)


        # hash pw (no plain-text pls)
        password = b(security.hashpw(password))


        # NOTE: issue in todo.md
        # default cookie should be removed soon
        cookie = b(json.dumps(['cookie time']))


    # if some of the data was corrupt and couldnt be encoded/hahsed
    except Exception as e:
        log(level='error', msg=f"[server/dbhandler/save_new_user/0] malformed data, could not be encloded\nTraceback: {e}")
        return "Internal server error", 500


    # save all the encoded data in the database
    try:
        db_connection = sqlite3.connect(f'storage/users.db')
        db_cursor = db_connection.cursor()
        # cookies are being stored as a list that has been converted to string, this makes it easy to add new cookies
        db_cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?)", (username, email, nickname, password, cookie))
        db_connection.commit()
        db_connection.close()


    # fail on sqlite errors. This usually happens when the server is run without properly set up databases
    except sqlite3.OperationalError as e:
        log(level='fail', msg=f'[server/dbhandler/checkuser/3] database operation failed:  {e}')
        return "Login failed. Internal database error", 500


    # everything okay
    return "OK", 200



def checkuser(username=None, email=None, password=None):
    if not os.path.isfile(f'storage/users.db'): #  check if there is a database
        # i dont think database should be autoinitialized bc on some error it could delete the old database
        log(level='fail', msg=f'could not find users.db')
        return "Login failed. Internal server error", 500


    # check if password exists
    # this should not happen as there are tests before, but it doesnt hurt to check again :)
    if password == None:
        log(level="warning", msg="no password")
        return "Login failed. no password sent", 400


    # email takes priority over username, so if email is present then use that for login
    if email != None:
        key = b(email)
        using = 'email'


    # if no email then login with username
    else: 
        key = b(username)
        using = 'username'




    # get all passwords for the user from the db
    try:
        db_connection = sqlite3.connect(f'storage/users.db')
        db_cursor = db_connection.cursor()
        db_cursor.execute(f"SELECT password FROM users WHERE username = ?", (key,))
        storedPassword = db_cursor.fetchall()
        db_connection.close()


    # fail on sqlite errors. This usually happens when the server is run without properly set up databases
    except sqlite3.OperationalError as e:
        log(level='fail', msg=f'[server/dbhandler/checkuser/3] database operation failed:  {e}')
        return "Login failed. Internal database error", 500


    # check for passwords with for said user
    # if there are none then the user is not registered
    if len(storedPassword) > 0:
        storedPassword = d(storedPassword[0][0])
    else:
        log(level='warning', msg=f'[server/dbhandler/checkuser/4] un-recognised username')
        return "Login failed. Username/email or password is incorrect!", 401


    # check if the password is correct
    if security.checkpw(password, storedPassword):
        return "OK", 200
    else:
        return "Login failed. Username/email or password is incorrect!", 401


# this function should not be in dbhandler
def check_access(username, chatroom_id):
    #return "chatroom doesnt exist or user doesnt have access to view it", 404
    return "OK", 200


def get_nickname(username):
    try:
        username = b(username)
        db_connection = sqlite3.connect(f'storage/users.db')
        db_cursor = db_connection.cursor()
        db_cursor.execute(f"SELECT nickname FROM users WHERE username = ?", (username,))
        data = db_cursor.fetchall()
        db_connection.close()
    except sqlite3.OperationalError as e:
        log(level='fail', msg=f'[server/dbhandler/get_nickname/0] database operation failed:  {e}')
        return False

    # sqlite3 wraps the username in a tuple inside of a list
    #print(data)
    return d(data[0][0])


def store_cookie(username=None, email=None, new_cookie=None):
    log(level="log", msg=f"user {username} just logged in")

    # check if the function was called without cookies, this should only happen if the sever code is brokent
    if new_cookie == None:
        log(level="error", msg=f'[server/dbhandler/store_cookie/0] function was called without a cookie supplied to it')
        return "Internal server error", 500


    # email takes priority over username, so if email is present then use that as the key
    if email != None:
        key = b(email)
        using = 'email'


    # if no email then key is username
    else: 
        key = b(username)
        using = 'username'


    # get stored cookies
    try:
        db_connection = sqlite3.connect("storage/users.db")
        db_cursor = db_connection.cursor()
        db_cursor.execute(f"SELECT cookies FROM users WHERE {using} = ?", (key,))
        cookies = db_cursor.fetchall()
        db_connection.close()


    # fail on sqlite errors. This usually happens when the server is run without properly set up databases
    except sqlite3.OperationalError as e:
        log(level='fail', msg=f'[server/dbhandler/store_cookie/1] database operation getting cookies failed:  {e}')
        return "Internal database error", 500


    # al users should have at least '[]' stored as cookes, if they dont then the database is corrupted somehow
    if len(cookies) == 0:
        log(level='error', msg=f'[server/dbhandler/store_cookie/2] user does not exists or did not get initialized properly\n (database cookies entry doesnt exist)')
        return "Internal database error", 500


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
        log(level='error', msg=f'[server/dbhandler/store_cookie/3] malformed cookie data in databse')
        return "Internal database error", 500


    # update server with new cookes list
    try:
        db_connection = sqlite3.connect("storage/users.db")
        db_cursor = db_connection.cursor()
        db_cursor.execute(f'UPDATE users SET cookies = ? WHERE {using} = ?', (cookies, key))
        db_connection.commit()
        db_connection.close()


    # fail on sqlite errors. This usually happens when the server is run without properly set up databases
    except sqlite3.OperationalError as e:
        log(level='fail', msg=f'[server/dbhandler/store_cookie/3] database operation, saving cookie: failed:  {e}')
        return "Internal database error", 5000


    # everything worked out fine
    return "OK", 200


def get_cookies(username):
    username = b(username)

    # get all  stored cookies of the user
    try:
        db_connection = sqlite3.connect(f'storage/users.db')
        db_cursor = db_connection.cursor()
        db_cursor.execute(f"SELECT cookies FROM users WHERE username = ?", (username,))
        data = db_cursor.fetchall()
        db_connection.close()
    except sqlite3.OperationalError as e:
        log(level='fail', msg=f'[server/dbhandler/get_cookies/2] database operation failed:  {e}')
        return False

    # cookies are stored in a base64 encoded str(list)
    if len(data) == 0:
        return False

    # decode and load the data as json
    try:
        data = d(data)
        data = json.loads(data)
    except:
        log(level='error', msg=f'[server/dbhandler/get_cookies/0] failed to process cookie data of user {username}\n Data is probably corrupted')

    return data







################################################# chat stuff ###############################################
#------------------------------------------------  testing ---------------------------------------------------
# tis only for testing
def get_all_messages(chatroom_id):
    try:
        db_connection = sqlite3.connect(f'storage/{chatroom_id}/messages.db')
        db_cursor = db_connection.cursor()
        db_cursor.execute(f"SELECT * FROM messages")
    except sqlite3.OperationalError as e:
        log(level='fail', msg=f'[server/dbhandler/get_all_users/0] database operation failed:  {e}')
        return False

    a = db_cursor.fetchall()
    for b in a:
        print(b)
    db_connection.close()


#-------------------------------------------------  init ------------------------------------------------------
def init_chat(chatroom_id):
    if os.path.exists(f'storage/{chatroom_id}'):
        log(level='error', msg=f'attempting to redifine chatroom:  {chatroom_id}')
        return False
    else:
        log(level='log', msg=f'creating chatroom:  {chatroom_id}')
        os.mkdir(f'storage/{chatroom_id}')
        os.mkdir(f'storage/{chatroom_id}/uploads/')

    db_connection = sqlite3.connect(f'storage/{chatroom_id}/messages.db')
    db_cursor = db_connection.cursor()
    # removed list of users here, might need this later
    db_cursor.execute(f"CREATE TABLE messages ('time', 'username', 'chatroom_id', 'type', 'message', 'filename', 'extension')")
    db_connection.commit()
    db_connection.close()

    return True


#---------------------------------------------------- messages ------------------------------------------------
# va=None means that the fild is not used
# var=0 means that the field is not set AND IS NEEDED FOR THE FUNCTION
# this destiction is for readability, the None values are not required but the 0 ones are
def save_in_db(time=0, username=0, chatroom_id=0, message_type=0, message=None, filename=None, extension=None ):
    if time == 0 or username == 0 or chatroom_id == 0 or message_type == 0: #values marked with 0 are needed while ones marked with None are optional
        # making sure that all values that are needed exist
        log(level='error', msg='[server/dbhandler/save_in_db/0] one or more of the required fields passed to function "save_in_db" are not present [time, username, chatroom_id, message_type]')
        return "internal server error", 500


    # make sure the database exists
    try:
        db_connection = sqlite3.connect(f'storage/{chatroom_id}/messages.db') # chatroom_id is the folder name that data to do with chatroom resides in
        db_cursor = db_connection.cursor()
    except:
        log(level='error', msg=f'[server/dbhandler/save_in_db/1] server could not connect to database')
        return "internal database error", 500


    # all of these values should be encoded as a sort of paranoid model
    try:
        db_cursor.execute(f"INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?)", (time, username, chatroom_id, message_type, message, filename, extension))
        db_connection.commit()
        db_connection.close()
    except sqlite3.OperationalError as e:
        log(level='fail', msg=f'[server/dbhandler/save_in_db/2] database operation failed:  {e}')
        return "internal database error", 500


    # all is well
    return "OK", 200


def get_messages(last_time=0, chatroom_id=''):
    try:
        db_connection = sqlite3.connect(f'storage/{chatroom_id}/messages.db') # chatroom_id is the folder name that data to do with chatroom resides in
        db_cursor = db_connection.cursor()
    except:
        log(level='error', msg=f'[server/dbhandler/get_messages/0] server could not connect to database')
        return False

    try:
        # im not putting try here bc there could be many erorrs with the db and i need to know them
        db_cursor.execute("SELECT * FROM messages WHERE time >= ?", (last_time,))

        data = db_cursor.fetchall()
        db_connection.close()
    except sqlite3.OperationalError as e:
        log(level='fail', msg=f'[server/dbhandler/get_messages/1] database operation failed:  {e}')
        return False

    # sqlite returns a list of lists
    # we should convert this back to json
    json_data = []
    for element in data:
        nickname = get_nickname(element[1])
        a = {
            'time': element[0],
            'username': element[1],
            'nickname': nickname,
            'chatroom': element[2],
            'type': element[3],
            'message': element[4],
            'filename': element[5],
            'extension': element[6],
                }


        json_data.append(a)

    return json_data



# create databases, THIS IS ONLY FOR TESTING
if __name__ == "__main__":
    init_user_db()
    init_chat('conv1')
    save_new_user(username="defaultId", nickname="default", password="password")


