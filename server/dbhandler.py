import os
import sys
import uuid
import base64
import sqlite3


import security_th as security
from logging_th import logger as log



#--------------------------------------------- encoding ---------------------------------------------
# encode/decode shit to stop any sort of injection
def b(a):
    return base64.b64encode(a.encode('utf-8')).decode('utf-8')

def d(a):
    return base64.b64decode(a.encode('utf-8')).decode('utf-8')




################################################# user stuff ###############################################
#-------------------------------------------------  init ----------------------------------------------------
# creates a users database
def init_user_db():
    if os.path.exists(f'storage/users.db'):
        log(level='warning', msg=f'[server/dbhandler/init_user_db] cannot redifine userdb')
        return False
    else:
        log(level='log', msg=f"creating usersdb")

    db_connection = sqlite3.connect(f'storage/users.db')
    db_cursor = db_connection.cursor()
    # cookies is a list of cookies, that is turned into a string with json, and base64/hex encoded
    db_cursor.execute(f"CREATE TABLE users ('userID', 'nickname', 'password', cookies)")
    db_connection.commit()
    db_connection.close()
    return True


#------------------------------------------------  testing --------------------------------------------------
# tis only for testing
def get_all_users():
    db_connection = sqlite3.connect(f'storage/users.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"SELECT * FROM users")
    a = db_cursor.fetchall()
    db_connection.close()
    for i in a:
        print(i)


def adduser_internal(userId=None, nickname=None, password=None):
    userId = b(userId)
    nickname = b(nickname)
    password = b(security.hashpw(password))
    cookie = b('[]')

    db_connection = sqlite3.connect(f'storage/users.db')
    db_cursor = db_connection.cursor()
    # cookies are being stored as a list that has been converted to string, this makes it easy to add new cookies
    db_cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?)", (userId, nickname, password, cookie))
    db_connection.commit()
    db_connection.close()


#-------------------------------------------------- access control ------------------------------------------
def checkuser(userId, password):
    if not os.path.isfile(f'storage/users.db'):
        log(level='error', msg=f'users.db does not exits')
        init_user_db()

    userId = b(userId)
    print('userId: ',userId , type(userId))

    # get all passwords for the user from the db
    db_connection = sqlite3.connect(f'storage/users.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"SELECT password FROM users WHERE userId = ?", (userId,))
    storedPassword = db_cursor.fetchall()
    db_connection.close()

    # check if the user has a password set
    print('storedPassword: ',storedPassword , type(storedPassword))
    # string has to be greater than 10 to have a password in it (password + [])
    if len(storedPassword) > 0:
        storedPassword = d(storedPassword[0][0])
    else:
        return False

    # check if the password is correct
    if security.checkpw(password, storedPassword):
        return True
    else:
        return False


# this function should not be in dbhandler
def check_access(userId, chatroom_id):
    return True


def get_nickname(userId):
    userId = b(userId)
    db_connection = sqlite3.connect(f'storage/users.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"SELECT nickname FROM users WHERE userId = ?", (userId,))
    data = db_cursor.fetchall()
    db_connection.close()

    # sqlite3 wraps the username in a tuple inside of a list
    print(data)
    return d(data[0][0])


def store_cookie(userId, new_cookie):
    print("storing cookies -------------------------------------------")
    db_connection = sqlite3.connect("storage/users.db")
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT cookies FROM users WHERE userId = ?", (userId,))
    cookies = db_cursor.fetchall()

    # cookies are being stored as a list that has been converted to string, this makes it easy to add new cookies
    cookies = list(cookies)
    cookies.append(new_cookie)
    cookies = str(cookies)
    print('cookies: ',cookies , type(cookies))

    # return the new cookies list back
    db_cursor = db_connection.cursor()
    db_cursor.execute('UPDATE users SET cookies = ? WHERE userId = ?', (cookies, userId))
    db_connection.commit()
    db_connection.close()

    get_all_users()

    return True


def get_cookies(userId):
    userId = b(userId)

    db_connection = sqlite3.connect(f'storage/users.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"SELECT cookies FROM users WHERE userId = ?", (userId,))
    data = db_cursor.fetchall()
    db_connection.close()

    # cookies are stored in a base64 encoded str(list)
    print(data)
    sys.exit()
    data = list(d(data))

    # sqlite3 wraps the username in a tuple inside of a list
    return data[0][0]








################################################# chat stuff ###############################################
#------------------------------------------------  testing ---------------------------------------------------
# tis only for testing
def get_all_messages(chatroom_id):
    db_connection = sqlite3.connect(f'storage/{chatroom_id}/messages.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"SELECT * FROM messages")
    a = db_cursor.fetchall()
    for b in a:
        print(b)
    db_connection.close()


#-------------------------------------------------  init ------------------------------------------------------
def init_chat(chatroom_id):
    if os.path.isfile(f'storage/{chatroom_id}'):
        log(level='error', msg=f'attempting to redifine chatroom:  {chatroom_id}')
        return False
    else:
        log(level='log', msg=f'creating chatroom:  {chatroom_id}')
        os.mkdir(f'storage/{chatroom_id}')
        os.mkdir(f'storage/{chatroom_id}/uploads/')

    db_connection = sqlite3.connect(f'storage/{chatroom_id}/messages.db')
    db_cursor = db_connection.cursor()
    # removed list of users here, might need this later
    db_cursor.execute(f"CREATE TABLE messages ('time', 'userId', 'chatroom_id', 'type', 'message', 'filename', 'extension')")
    db_connection.commit()
    db_connection.close()
    return True


#---------------------------------------------------- messages ------------------------------------------------
# va=None means that the fild is not used
# var=0 means that the field is not set AND IS NEEDED FOR THE FUNCTION
# this destiction is for readability, the None values are not required but the 0 ones are
def save_in_db(time=0, userId=0, chatroom_id=0, message_type=0, message=None, filename=None, extension=None ):
    if time == 0 or userId == 0 or chatroom_id == 0 or message_type == 0:
        log(level='error', msg='[server/dbhandler/save_in_db/0] one or more of the required fields passed to function "save_in_db" are not present [time, userId, chatroom_id, message_type]')
        return False

    # check if db exists
    # in dont then it will fail but create currently
    try:
        db_connection = sqlite3.connect(f'storage/{chatroom_id}/messages.db') # chatroom_id is the folder name that data to do with chatroom resides in
        db_cursor = db_connection.cursor()
    except:
        log(level='error', msg=f'[server/dbhandler/save_in_db/1] server could not connect to database')
        return False
    # a safe-ish way of adding sql
    # all of these values should be encoded as a sort of paranoid model
    db_cursor.execute(f"INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?)", (time, userId, chatroom_id, message_type, message, filename, extension))
    # :wq
    db_connection.commit()
    db_connection.close()

    # this call is only here for debugging, pls ignore
    #get_all_messages(chatroom_id)

    return True


def get_messages(last_time=0, chatroom_id=''):
    try:
        db_connection = sqlite3.connect(f'storage/{chatroom_id}/messages.db') # chatroom_id is the folder name that data to do with chatroom resides in
        db_cursor = db_connection.cursor()
    except:
        log(level='error', msg=f'[server/dbhandler/get_messages/0] server could not connect to database')
        return False

    # im not putting try here bc there could be many erorrs with the db and i need to know them
    db_cursor.execute("SELECT * FROM messages WHERE time >= ?", (last_time,))

    data = db_cursor.fetchall()
    db_connection.close()

    # sqlite returns a list of lists
    # we should convert this back to json
    json_data = []
    for element in data:
        nickname = get_nickname(element[1])
        a = {
            'time': element[0],
            'userId': element[1],
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
    adduser_internal(userId="42138947328947329847", nickname="default", password="password")


