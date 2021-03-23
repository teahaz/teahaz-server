# this file handles all things connected to local files
import os
import shutil
import security_th as security
from logging_th import logger as log


def save_file_chunk(data, chatroom, extension, fileId, username):
    print('fileId: ',fileId , type(fileId))
    res, status = security.check_uuid(fileId)
    if status != 200:
        return res, status


    # make sure the uploads folder exists
    if not os.path.exists(f'storage/chatrooms/{chatroom}/uploads'): # make sure uploads folder exists
        log(level='error', msg=f'[filesystem_th/save_file/0] || uploads forlder does not exist for chatroom:  {chatroom}')
        return "internal server error while saving file", 500


    
    # write the file owner to the beginning of the file
    if not os.path.exists(f'storage/chatrooms/{chatroom}/uploads/{fileId}'):
        try:
            with open(f'storage/chatrooms/{chatroom}/uploads/{fileId}', 'a+')as outfile:
                outfile.write(security.encode(username)+';')

        except Exception as e:
            log(level='error', msg=f'[filesystem/save_file/1] || An error occured while setting the file owner.\n Traceback: {e}')
            return '[filesystem/save_file/1] || An error occured while setting the file owner.', 500



    # read the file owner from the file
    else:
        try:
            f = open(f'storage/chatrooms/{chatroom}/uploads/{fileId}')
            owner = ''
            while True:
                char = f.read(1)

                if not char:
                    return "[filesystem/save_file/2] || an error occured while getting file owner", 500

                elif char == ';':
                    break

                else:
                    owner += char

            f.close()
            if owner != security.encode(username):
                return "[filesystem/save_file/3] || This file was not created by you, and you dont have permission to edit it", 403

        except Exception as e:
            log(level='error', msg=f'[filesystem/save_file/4] || An error occured while getting the file owner.\n Traceback: {e}')
            return '[filesystem/save_file/4] || An error occured while getting the file owner.', 500



    # save file
    try:
        with open(f'storage/chatrooms/{chatroom}/uploads/{fileId}', 'a')as outfile:
            outfile.write(data+';')


    # failed to save file
    except Exception as e:
        log(level='error', msg=f'[filesystem_th/save_file/2] || failed to write file: storage/{chatroom}/uploads/{fileId}   exeption: {e}')
        return "internal server error while saving file", 500


    # all is well
    return "OK", 200

def read_file_chunk(chatroom, fileId, section):
    print(f'storage/chatrooms/{chatroom}/uploads/{fileId}')

    if not os.path.isfile('storage/chatrooms/{chatroom}/uploads/{fileId}'):
        return '[filesystem/read_file_chunk/0] || requested file does not exist', 404



    # try open file
    try:
        f = open('storage/chatrooms/{chatroom}/uploads/{fileId}', 'r')
    except Exception as e:
        log(level='error', msg=f"[filesystem/read_file_chunk/1] || could not open file for reading. \n Traceback: {e}")
        return '[filesystem/read_file_chunk/1] || could not open file for reading.', 500


    # try read file
    # NOTE this might get incredibly slow in large files, and we might want to find a better way
    try:
        data = ''
        current_section = 0
        while 1:
            #read one byte
            c = f.read(1)

            # if byte is a section delimiter then mark new section and continu
            if c == ';':
                current_section += 1

            # if in the right section then add it to the return data
            elif current_section == section:
                data += c

            # dont waste time by scanning sections we dont need
            elif current_section > section:
                break


    except Exception as e:
        log(level='error', msg=f"[filesystem/read_file_chunk/2] || An error occured while reading file \n Traceback: {e}")
        return '[filesystem/read_file_chunk/2] || An error occured while reading file', 500


    return data, 200



def remove_file(chatroom, filename):
    try: # remove file
        os.remove(f'storage/{chatroom}/{filename}')
    except:
        return "internal server error while removeing file", 500


    # all is well
    return "OK", 200


def create_chatroom_folders(chatroomId):
    if os.path.exists(f"storage/{chatroomId}"):
        return "Internal server error: tried to assing existing chatroom ID", 400

    try:
        os.mkdir(f'storage/chatrooms/{chatroomId}')
        os.mkdir(f'storage/chatrooms/{chatroomId}/uploads')
        a = open(f"storage/chatrooms/{chatroomId}/main.db", "w+")
        a.close()

    except Exception as e:
        log(level='error', msg=f'[server/filehanler/create_chatroom_folders/0] could not create chatroom folders\n Traceback: {e}')
        return f"Internal server error: failed while setting up the chatroom", 500

    return "OK", 200


def remove_chatroom(chatroom):
    try:
        shutil.rmtree(f'storage/chatrooms/{chatroom}', ignore_errors=True)


    except Exception as e:
        log(level='error', msg=f"[server/filehanler/remove_chatroom/0] could not remove chatroom\n Traceback: {e}")
        return "could not remove the chatroom", 500


    return "OK", 200
