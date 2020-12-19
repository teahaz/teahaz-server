import base64
import uuid
import os
import sqlite3

from server_logger import logger as log


# encode/decode shit to stop any sort of injection
def b(a):
    return base64.b64encode(a.encode('utf-8')).decode('utf-8')

def d(a):
    return base64.b64decode(a.encode('utf-8')).decode('utf-8')


# tis only for testing
def get_all_messages(chatroom_id):
    db_connection = sqlite3.connect(f'storage/{chatroom_id}/messages.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"SELECT * FROM messages")
    a = db_cursor.fetchall()
    for b in a:
        print(b)
    db_connection.close()



# tis only for testing
def get_all_users(chatroom_id):
    db_connection = sqlite3.connect(f'storage/{chatroom_id}/messages.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"SELECT * FROM users")
    print(db_cursor.fetchall())
    db_connection.close()



def check_access(username, chatroom_id):
    return True



# va=None means that the fild is not used
# var=0 means that the field is not set AND IS NEEDED FOR THE FUNCTION
# this destiction is for readability, the None values are not required but the 0 ones are
def save_in_db(time=0, username=0, chatroom_id=0, message_type=0, message=None, filename=None, extension=None ):
    if time == 0 or username == 0 or chatroom_id == 0 or message_type == 0:
        log(level='error', msg='[server/messagesdb/save_in_db/0] one or more of the required fields passed to function "save_in_db" are not present [time, username, chatroom_id, message_type]')
        return False

    # check if db exists
    # in dont then it will fail but create currently
    try:
        db_connection = sqlite3.connect(f'storage/{chatroom_id}/messages.db') # chatroom_id is the folder name that data to do with chatroom resides in
        db_cursor = db_connection.cursor()
    except:
        log(level='error', msg=f'[server/messagesdb/save_in_db/1] server could not connect to database')
        return False
    # a safe-ish way of adding sql
    # all of these values should be encoded as a sort of paranoid model
    db_cursor.execute(f"INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?)", (time, username, chatroom_id, message_type, message, filename, extension))
    # :wq
    db_connection.commit()
    db_connection.close()

    # this call is only here for debugging, pls ignore
    get_all_messages(chatroom_id)

    return True



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
    db_cursor.execute(f"CREATE TABLE users ('name', 'colour')")
    db_cursor.execute(f"CREATE TABLE messages ('time', 'username', 'chatroom_id', 'type', 'message', 'filename', 'extension')")
    db_connection.commit()
    db_connection.close()
    return True



def get_messages(last_time=0, chatroom_id=''):
    try:
        db_connection = sqlite3.connect(f'storage/{chatroom_id}/messages.db') # chatroom_id is the folder name that data to do with chatroom resides in
        db_cursor = db_connection.cursor()
    except:
        log(level='error', msg=f'[server/messagesdb/get_messages/0] server could not connect to database')
        return False

    # im not putting try here bc there could be many erorrs with the db and i need to know them
    db_cursor.execute("SELECT * FROM messages WHERE time >= ?", (last_time,))

    data = db_cursor.fetchall()
    db_connection.close()

    # sqlite returns a list of lists
    # we should convert this back to json
    json_data = []
    for element in data:
        a = {
            'time': element[0],
            'username': element[1],
            'chatroom': element[2],
            'type': element[3],
            'message': element[4],
            'filename': element[5],
            'extension': element[6],
                }
        json_data.append(a)

    return json_data



