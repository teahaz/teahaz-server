"""
    A few healthchecks running on a loop to make sure the server is functioning correctly
"""

import os
import sys
import time

from on_error import on_error

# adding teahaz paths so we can import files
if os.getenv('PROD') == True:
    sys.path.insert(1,'/usr/src/teahaz')
else:
    sys.path.insert(1,'../teahaz/src')


import dbhandler as database
from logging_th import logger as log





while True:
    time.sleep(6)

    response, status_code = database.check_databases()
    if status_code != 200:
        log(level='warning', msg="[ Warning ]  healthcheck failed, could cause major issues!")
        on_error(response)







