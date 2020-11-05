import base64
import os
import sqlite3

from server_logger import server_log as log
from server_logger import server_error as error
from server_logger import server_warning as warning

def authenticate(usrname, cookie):
    return True

def check_access(username, chatroom_id):
    return True

def save_message(time=0, username='', message='', chatroom_id='conv1'):
    db_connection = sqlite3.connect(f'storage/{chatroom_id}/messages.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"INSERT INTO messages VALUES ('{time}','{username}','{chatroom_id}','{message}')")
    db_connection.commit()
    db_connection.close()
    return True


def init_chat(chatroom_id):
    if os.path.exists('storage/{chatroom_id}'):
        warning('attempting to redifine chatroom: ', chatroom_id)
        return False
    db_connection = sqlite3.connect(f'storage/{chatroom_id}/messages.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"CREATE TABLE users ('name', 'colour')")
    db_cursor.execute(f"CREATE TABLE messages ('time', 'username', 'chatroom_id', 'type', 'message', 'filename', 'mimetype')")
    db_connection.commit()
    db_connection.close()
    return True


