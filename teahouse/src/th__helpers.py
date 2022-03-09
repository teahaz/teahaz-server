"""
A few misc functions that could not be categorised into
any of the other files.
"""

from th__database import Database
import th__filesystem as filesystem


def check_default_and_get_data(chatroom_id: str, request) -> tuple[dict, int]:
    """
        Function checks a few things that need to be true for
        every request (including that the chatroom exists, and username is sent).

        Returns the either the headers or json_data of the request
        depending on the method. GET request have to send data
        in the header, but everything else can send it in the data.
    """
    data: dict = (request.headers if request.method == "GET" else request.get_json())


    if not data:
        return {"error": "No data has been sent to the server."}, 400


    if not data.get('username'):
        return {"error": "The username variable has to be sent with every request."}, 400


    if not chatroom_exists(chatroom_id):
        return {"error": "The requested chat-room does not exist on this server."}, 404


    return data, 200


def chatroom_exists(chatroom_id: str) -> bool:
    """
        Function checks both the filesystem
        and the database to determine whether
        a chatroom exists or not.
    """
    if not filesystem.chatroom_directories_exist(chatroom_id):
        return False

    # TODO: test and see if this actually creates the chatroom.
    #       (We don't want that to happen)
    db_class = Database(chatroom_id, "bs non-existing user")
    return db_class.exists





def bad(status: int) -> bool:
    """
    Simple function to check whether a status is within the
    range 200-300.
    This gets called so many times, it was worth making
    it into a function.
    """
    return status not in range(199, 299)
