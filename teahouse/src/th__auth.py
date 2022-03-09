"""
Series of functions to handle authentication related issues.

This includes functions for checking if the user is logged in,
as well as setting cookies, and checking passwords. (and some others)
"""

import codectrl
import th__helpers as helpers


def check_cookie_before(chatroom_id: str, request, callback) -> tuple[dict, int]:
    """
        This function is meant to be placed between functions in
        main.py and api.py.

        The function checks if a user is logged in before
        calling the intended api function.
    """


    data, status = helpers.check_default_and_get_data(chatroom_id, request)
    if helpers.bad(status):
        return data, status


    if not request.cookies.get(chatroom_id):
        return {"error": "No cookies supplied for this chatroom. Client not logged in!"}, 401


    codectrl.log("Need to get cookies from the database to check login!")
    return callback(chatroom_id, data)
    # cookies, status = database.get_cookies(chatroom_id, username, cookie)
    # if status != 200:
    #     return False
    #
    # for i in cookies:
    #     if i == cookie:
    #         return True
    #
    # return False


