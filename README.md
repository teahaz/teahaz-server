Teahaz / teahouse
=================
a messaging platform a friend and I are building.
Server is mostly self hosted, thus file size limits are configurable


Also plan on adding a method to stream files to each other, creating essentially and unlimited file transfer


IMPORTANT
=========
This server is nowhere near done yet!


usage
=====
dependencies
------------
* docker
* python3
* certbot (if you want to use ssl)



setup
-----
**with ssl:**
```bash
python3 setup.py
```
You will need to enter your hostname (WITHOUT https or trailing slashes). Next you will have to enter the ABSOLUTE path to your teahaz installation repo [eg /teahaz]. Next certbot will ask you a few questions that you need to asnwer.
<br />
<br />
If the program runs successfully, you should be almost done. Setup uses a temporary http server for certbot verification. This server doesnt always shutdown correctly, for best practice search for `python3 -m http.server` in ps aux/top/htop and kill it or run `killall python`.
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


**without ssl:**
```
python3 setup.py nossl
```
You will need to enter your hostname (WITHOUT https or trailing slashes). Next you will have to enter the ABSOLUTE path to your teahaz installation repo [eg /teahaz].
<br />
<br />
If this runs without errors then your setup is complete


usage
-----
There are four possible operations with the server:
<br />

* run container:
```
sudo ./run
```
This should setup itslef and run teahaz.
<br />
<br />

* kill container:
`sudo ./run kill`
This should stop teahaz.
<br />
<br />

* get shell in container:
`sudo ./run shell`
Method allows you to get an unprivilaged shell inside the container, to make sure everything works fine.
<br />
<br />

* rebuild container:
`sudo ./run shell`
If something breaks, or gets outdated. Rebuilding the container should try update and fix itself

<br />
<br />



this readme doesn't really have anything useful in it
----------------------------------------------------
TODO: fix this ^^


