"""
    This module does things on the filesystem.

    No function outside this module should ever
    touch the filesystem in any way.
"""

import os
import th__security as security



def chatroom_exists(chatroom_id: str) -> bool:
    """ Check if chatroom_id is valid, and that it exists on disk """

    if not security.is_uuid(chatroom_id):
        return False
    if not os.path.exists(f'storage/chatrooms/{chatroom_id}'):
        return False
    return True
