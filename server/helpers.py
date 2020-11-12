import base64
import hashlib
import os
import sqlite3

from server_logger import server_log as log
from server_logger import server_error as error
from server_logger import server_warning as warning


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



def authenticate(usrname, cookie):
    return True

def check_access(username, chatroom_id):
    return True



def save_message(time=0, username='', message='', chatroom_id='conv1'):
    db_connection = sqlite3.connect(f'storage/{chatroom_id}/messages.db') # chatroom_id is the folder name that data to do with chatroom resides in
    db_cursor = db_connection.cursor()
    # a safe-ish way of adding sql
    # all of these values should be encoded as a sort of paranoid model
    db_cursor.execute(f"INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?)", (time, username, chatroom_id, 'text', message, None, None))
    # :wq
    db_connection.commit()
    db_connection.close()

    # just for debug
    get_all_messages('conv1')

    return True



def init_chat(chatroom_id):
    if os.path.exists(f'storage/{chatroom_id}'):
        error('attempting to redifine chatroom: ', chatroom_id)
        return False
    else:
        log('creating chatroom: ', chatroom_id)
        os.mkdir(f'storage/{chatroom_id}')

    db_connection = sqlite3.connect(f'storage/{chatroom_id}/messages.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"CREATE TABLE users ('name', 'colour')")
    db_cursor.execute(f"CREATE TABLE messages ('time', 'username', 'chatroom_id', 'type', 'message', 'filename', 'mimetype')")
    db_connection.commit()
    db_connection.close()
    return True


def get_messages(last_time=0, chatroom_id=''):
    db_connection = sqlite3.connect(f'storage/{chatroom_id}/messages.db') # chatroom_id is the folder name that data to do with chatroom resides in
    db_cursor = db_connection.cursor()

    db_cursor.execute("SELECT * FROM messages WHERE time >= ?", (last_time,))

    data = db_cursor.fetchall()
    db_connection.close()

    return data


def save_file(data, mime_type, extension):
    filename = hashlib.sha1().update(data).hexdigest()
    print(filename)

    return filename


