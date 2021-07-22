import os
import sys
import time
from hashlib import md5


filename = sys.argv[1]


oldhash = ''

while True:
    time.sleep(1)

    with open(filename, 'rb')as infile:
        data = infile.read()

    md5hash = md5(data).hexdigest()

    if md5hash != oldhash:
        os.system(f'pydown -f {filename}')

    oldhash = md5hash



