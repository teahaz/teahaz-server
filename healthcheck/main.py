"""
    A few healthchecks running on a loop to make sure the server is functioning correctly
"""

import os
import sys
import time
import json
import subprocess

from on_error import on_error

# adding teahaz paths so we can import files
if os.getenv('PROD') == True:
    teahazpath = '/usr/src/teahaz'
else:
    teahazpath = '../teahaz/src'
sys.path.insert(1, teahazpath)
# os.chdir(teahazpath)

import dbhandler as database
from logging_th import logger as log



# get settings
with open('settings.json', 'r')as infile:
    settings = json.loads(infile.read())

sleep_time = (settings.get('check_interval_seconds') if type(settings.get('check_interval_seconds')) == int else 60 )
autoupdate = (settings.get('auto_apply_non-breaking_updates') if type(settings.get('auto_apply_non-breaking_updates')) == bool else False )
print('autoupdate: ',autoupdate , type(autoupdate))



while True:
    time.sleep(sleep_time)

    # check the databases
    response, status_code = database.check_databases()
    if status_code != 200:
        log(level='warning', msg="[ Warning ]  healthcheck failed, could cause major issues!")
        on_error(response, tp='dbcheck')


    # autoupdate
    # TODO for now this just does git-pull but it should actually refresh the running container too
    if autoupdate:
        result = subprocess.run(['git', 'pull'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout)
        print(result.stderr)
        if result.returncode != 0:
            log(level='warning', msg="[ Warning ] autoupdate failed to pull updates from git")
            on_error(f"failed to pull updates from git. stdout:  {result.stdout} stderr: {result.stderr}", tp='autoupdate')



