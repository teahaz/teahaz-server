import base64
import sqlite3


def authenticate(usrname, cookie):
    return True

def check_access(username, chatroom_id):
    return True

def decode_messages(data):
    return base64.b64decode(data).decode('utf-8')

def save_message(time=0, username='', message='', chatroom_id=''):
    db_connection = sqlite3.connect(f'{chatroom_id}/messages.db')
    db_cursor = db_connection.cursor()
    c.execute("INSERT INTO messages VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    just realized that maybe combining into one or two database might be better
    not yet detailed in sqlite version2 in notes but will be soon
    return True

