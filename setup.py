import os
import sys
import signal
import subprocess







print("Some configuration files like nginx_config require the hostname of the server.\nIMPORANT: When typing the hostname below, make sure TO NOT mistype it and DO NOT ADD 'http(s)://' to the beginning")
hostname = input("server hostname [eg: teahaz.co.uk]: ")
hostname = hostname.strip('\n')
hostname = hostname.strip(' ')
hostname = hostname.strip('/')
hostname = hostname.replace('http://', '')
hostname = hostname.replace('https://', '')
hostname = hostname.strip('/')
print(hostname)
sys.exit


path = input("absolute path to teahaz repository: ")


os.system(f'rm -rf {path}/.keys')






if len(sys.argv) > 2:
    res = os.system("which certbot")
    if res != 0:
        print("ERR: please install certbot")
        sys.exit(-1)

    with open(f"{path}/docker/nginx_default_config", "r")as infile:
        nginx_config = infile.read()

    with open(f"{path}/docker/nginx_config", "w+")as outfile:
        outfile.write(nginx_config)


    os.system(f'mkdir {path}/static')
    p = subprocess.Popen(f"cd {path}/static; python3 -m http.server 80 --bind 0.0.0.0", shell=True)
    try:

        os.system(f'mkdir -p {path}/.keys/live/{hostname}')
        os.system(f'mkdir -p {path}/.keys/archive/{hostname}')

        res = os.system(f"sed -i 's/<REPLACE_SERVER_HOSTNAME>/{hostname}/g' {path}/run")
        if res != 0: sys.exit(-1)
        res = os.system(f"sed -i 's/<REPLACE_SERVER_HOSTNAME>/{hostname}/g' docker/*")
        if res != 0: sys.exit(-1)
        res = os.system(f"sudo certbot certonly --webroot -w {path}/static -d {hostname}")
        if res != 0: sys.exit(-1)

        res = os.system(f"cp -R /etc/letsencrypt/archive/{hostname} {path}/.keys/archive/")
        if res != 0: sys.exit(-1)
        res = os.system(f"cp -R /etc/letsencrypt/live/{hostname} {path}/.keys/live/")
        if res != 0: sys.exit(-1)

    except Exception as e:
        print("process failed: ", e)
        p.kill()
        sys.exit(-1)


    p.kill()
    os.kill(p.pid, signal.SIGKILL)
    print("everything setup successfully")


elif sys.argv[1] == 'nossl':
    with open(f"{path}/docker/nginx_default_config_no-ssl", "r")as infile:
        nginx_config = infile.read()

    with open(f"{path}/docker/nginx_config", "w+")as outfile:
        outfile.write(nginx_config)

    res = os.system(f"sed -i 's/<REPLACE_SERVER_HOSTNAME>/{hostname}/g' docker/nginx_config")
    if res != 0: sys.exit(-1)
    sys.exit()

