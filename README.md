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
requirements
------------
* docker

run
---
run server:
`sudo ./run`

kill server:
`sudo ./run kill`

get shell in server:
`sudo ./run shell`







## setup notes
* if you mess up ssl_setup then you will have to delete and reclone, as it does a lot of find and replace in config files
* sometimes it complains that port 80 is in use after setup.py. In this case just find `python3 simple http.server` in (h)top and kill it
this readme doesn't really have anything useful in it
----------------------------------------------------
TODO: fix this ^^


