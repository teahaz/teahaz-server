import os
import sys
import subprocess









if __name__ == "__main__":
    print("Some configuration files like nginx_config require the hostname of the server.\nIMPORANT: When typing the hostname below, make sure TO NOT mistype it and DO NOT ADD 'http(s)://' to the beginning")
    hostname = input("server hostname [eg: teahaz.co.uk]: ")
    hostname = hostname.strip('\n')
    hostname = hostname.strip(' ')
    hostname = hostname.strip('/')
    hostname = hostname.strip('http://')
    hostname = hostname.strip('https://')
    hostname = hostname.strip('/')


    path = input("absolute path to teahaz repository: ")
    path.strip(' ')

    p = subprocess.Popen(f"cd {path}/static;python3 -m http.server 80 --bind 0.0.0.0 &", shell=True)

    os.makedirs(f'.keys/live/{hostname}')
    os.makedirs(f'.keys/archive/{hostname}')

    res = os.system(f"sed -i 's/<REPLACE_SERVER_HOSTNAME>/{hostname}/g' docker/*")
    if res != 0: sys.exit(-1)
    res = os.system(f"sudo certbot certonly --webroot -w {path}/static -d {hostname}")
    if res != 0: sys.exit(-1)

    res = os.system("cp -R /etc/letsencrypt/archive/teahaz.co.uk /teahaz/.keys/archive/teahaz.co.uk")
    if res != 0: sys.exit(-1)
    res = os.system("cp -R /etc/letsencrypt/live/teahaz.co.uk /teahaz/.keys/live/teahaz.co.uk")
    if res != 0: sys.exit(-1)


    print("everything setup successfully")
