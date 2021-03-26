Setup your own server
====================
dependencies
------------
* docker
* python3
* certbot (Only for ssl)

<br />
<br />


Automatic setup
---------------
A script called `setup.py` is included with the repository. This script will attempt to automate the server setup, however its incredibly unstable and if it fails we recomend doing the manual setup.
<br />
<br />
### with ssl:
```bash
python3 setup.py
```
You will need to enter your hostname (WITHOUT https or trailing slashes). Next you will have to enter the ABSOLUTE path to your teahaz installation repo [eg /teahaz]. Next certbot will ask you a few questions that you need to answer.
<br />
<br />
If the program runs successfully, you should be almost done. Setup uses a temporary http server for certbot verification. This server doesn't always shutdown correctly, for best practice search for `python3 -m http.server` in ps aux/top/htop and kill it or run `killall python3`.
<br />
<br />
Finally we need to sort out renewing certificates. You can manually run cert-renew.sh every couple months, or we suggest adding the following line to your root crontab. (`sudo crontab -e`)
```
0 0 1 * * sh <PATH_TO_TEAHAZ_DIR>/cert-renew.sh 
```
**NOTE:** replace `<PATH_TO_TEAHAZ_DIR>` with the directory you installed teahaz to [eg /teahaz]
<br />
<br />
Your ssl setup should be complete :)

<br />
<br />


### without ssl:
```
python3 setup.py nossl
```
You will need to enter your hostname (WITHOUT https or trailing slashes). Next you will have to enter the ABSOLUTE path to your teahaz installation repo [eg /teahaz].
<br />
<br />
If this runs without errors then your setup is complete


<br />
<br />
<br />


Manual setup
------------
**Note**: if you are doing the manual setup because the automatic setup failed, it might be wise to re-clone the repository. The setup script can mess some config-files up.

### With ssl:
0. What you will need:
    - A domain name. This will be later refered to as `{hostname}`. Anywhere you see `{hostname}` in the next sections, you should replace it with your domain. **Do not** add http(s) to the end of the domain.
    - A linux server
    - port 80 and 443 exposed
<br />
<br />


1. Downloading the server:
```
git clone https://github.com/tHoMaStHeThErMoNuClEaRbOmB/teahaz-server
cd teahaz-server/
```
<br />
<br />
2. getting ssl certificates

* Creating direcorories for certbot keys

```
mkdir static/
mkdir -p .keys/live/{hostname}
mkdir -p .keys/archive/{hostname}
```

**Remember** to replace `{hostname}` with your servers domain name
<br />
<br />
* seting up a temporary http server
<br />
For certbot to verify your certificate it needs to be able to contact your server. Teahaz currently doesnt have the capacity to do this without going through 2 different setups. For this reasont we are going to run a simple http server that comes with python3.

```
cd static/
python3 -m http.server 80 --bind 0.0.0.0
```

Let the server run and open a new terminal for the next parts of the walkthrough.
<br />
* Run certbot to get certificates:

```
cd {TEAHAZ_REPOSITORY}
sudo certbot certonly --webroot -w static/ -d {hostname}
```

**NOTE:** replace `{TEAHAZ_REPOSITORY}` with the absolute path of your teahaz git repository
<br />
<br />
* copy ssl keys to the repository directory so they can be included with docker:

```
cp -R /etc/letsencrypt/archive/{hostname} {TEAHAZ_REPOSITORY}/.keys/archive/
cp -R /etc/letsencrypt/live/{hostname} {TEAHAZ_REPOSITORY}/.keys/live/
```

<br />
<br />
3. Configuring nginx
<br />
Make a copy of the sample nginx file, and call it nginx\_config:

```
cd docker/
cp nginx_default_config nginx_config
```

* Editing the config file:
Open the config config file (`nginx_config`) with your preferred text editor, the examples will use `vim`, but you can use any text editor you prefer.
<br />

```
vim nginx_config
```

The config file *should* look something like this:

```
server {
    listen 80;
    server_name <REPLACE_SERVER_HOSTNAME>;

    location ~ /.well-known {
        root /home/teahaz/static;
    }

    location / {
        include proxy_params;
        return 301 https://$host$request_uri;
    }
}


server {
    listen 443 ssl;
    server_name <REPLACE_SERVER_HOSTNAME>;
    ssl_certificate /home/teahaz/.keys/live/<REPLACE_SERVER_HOSTNAME>/fullchain.pem;
    ssl_certificate_key /home/teahaz/.keys/live/<REPLACE_SERVER_HOSTNAME>/privkey.pem;
    client_max_body_size 1G;

    location ~ /.well-known {
        root /home/teahaz/static;
    }

    location / {
        include proxy_params;
        proxy_pass http://localhost:13337;
    }
}
```

You will need to replace `<REPLACE_SERVER_HOSTNAME>` with the hostname of your server. Following the syntax layed out in section `0`.
<br />
<br />
If all of this ran without any issues then you should be all setup :)
<br />
<br />
### without ssl
yea ill come back to this




<br /><br /><br />


usage
-----
There are four possible operations with the server:
<br />

* run container:
```
sudo ./run
```
This should setup itself and run teahaz.
<br />
<br />

* kill container:
```
sudo ./run kill
```
This should stop teahaz.
<br />
<br />

* get shell in container:
```
sudo ./run shell
```
Method allows you to get an unprivileged shell inside the container, to make sure everything works fine.
<br />
<br />

* rebuild container:
```
sudo ./run shell
```
If something breaks, or gets outdated. Rebuilding the container should try update and fix itself

<br />
<br />

