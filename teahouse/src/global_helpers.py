"""
    A few functions that need to be called many times, often in different files.
"""
# setup logging
from logging_th import logger
global log
log = logger()


def db_format_channel(channel_info: list):
    """
        Format the list of tuples that the channels db returns into a dict

        return:
            {
                channelID: "channelID",
                channel_name: "channel_name",
                public: False
            }
    """



    # this type of operation can crash the server if I fuck something up in the table
    # I need an error message bc this seems like it would be really hard to debug otherwise
    try:
        channel_obj = {
                "channelID": channel_info[0],
                "channel_name": channel_info[1],
                "public": channel_info[2]
                }
    except Exception as e:
        log.error(db_format_channel, f"Corrupted information in channels table. {e = }")
        return "Internal database error while fetching channel information", 500


    return channel_obj, 200
