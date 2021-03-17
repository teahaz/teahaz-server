import os
import sys
import subprocess







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





if len(sys.argv) < 2:
    nginx_config = """
server {
    listen 80;
    server_name <REPLACE_SERVER_HOSTNAME>;

    location / {
        proxy_pass http://localhost:13337;
    }
}
"""

    res = os.system(f"sed -i 's/<REPLACE_SERVER_HOSTNAME>/{hostname}/g' docker/*")
    if res != 0: sys.exit(-1)
    sys.exit()



else:
    res = os.system("which certbot")
    if res != 0:
        print("ERR: please install certbot")
        sys.exit(-1)


    nginx_config = """
server {
    listen 80;
    server_name <REPLACE_SERVER_HOSTNAME>;

    location ~ /.well-known {
        root /home/teahaz/static;
    }

    location / {
        include proxy_params;
        proxy_pass http://localhost:13337;
    }
}


server {
    listen 443;
    ssl on;
    server_name <REPLACE_SERVER_HOSTNAME>;
    ssl_certificate /home/teahaz/.keys/live/<REPLACE_SERVER_HOSTNAME>/fullchain.pem;
    ssl_certificate_key /home/teahaz/.keys/live/<REPLACE_SERVER_HOSTNAME>/privkey.pem;

    location ~ /.well-known {
        root /home/teahaz/static;
    }

    location / {
        include proxy_params;
        proxy_pass http://localhost:13337;
    }
}

"""

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

        res = os.system(f"cp -R /etc/letsencrypt/archive/{hostname} /teahaz/.keys/archive/{hostname}")
        if res != 0: sys.exit(-1)
        res = os.system(f"cp -R /etc/letsencrypt/live/{hostname} /teahaz/.keys/live/{hostname}")
        if res != 0: sys.exit(-1)

    except Exception as e:
        print("process failed: ", e)
        p.kill()
        sys.exit(-1)


    p.kill()
    print("everything setup successfully")
