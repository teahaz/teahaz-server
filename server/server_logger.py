import time
import os

# the class stays here so we can easily add new templates if needed
class colours:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


# templates should be put on the begining of a line that is printed
## print(colour_templates['warning'] + "string")
colour_templates = {
        # increasing level of severity
        "success": colours.RESET + colours.BOLD + colours.GREEN +colours.UNDERLINE,
        "log": colours.RESET + colours.BOLD,
        "warning": colours.RESET + colours.YELLOW,
        "error": colours.RESET + colours.RED,
        "fail": colours.RESET + colours.BOLD + colours.RED + colours.UNDERLINE,
        }




# main logger function
def logger(level='log', msg=""):
    # level = the type of log [colours, etc]
    level = level.lower()
    msg_log = colour_templates[level] + f"[ {level} ] {time.time()}  ||  {msg} {colours.RESET}\n"
    print(msg_log)

    if not os.path.exists('./logs'):
        os.mkdir('./logs')

    # keep all logs in a file for later
    with open("logs/logfile", "a+")as outfile:
        outfile.write(msg_log+'\n')


