# disclaimer
The setup changes often enough that I dont find it worth writing proper setup documentation *yet*. These docs will be updated before the first release



# dependancies
1. docker
2. docker-compose
3. Python3
4. nginx
5. certbot (by letsencrypt)


# Important setup notes
Please read this before continuing with the install

- Most of the installation has to be done as root
- Anywhere where the installation talks about the server hostname it means the domain of your server **without** `http[s]` or port numbers




# setup steps:
1. Clone the newest version of the repo into `/teahouse`
```
git clone https://github.com/tHoMaStHeThErMoNuClEaRbOmB/teahaz-server/ /teahouse
```
**Note:** you can use a different directory, but you may have to change things in the docker confg and numerous other places


2. setup nginx server
    * copy `templates/nginx_config` to the root dir of the repo
    ```
    cp templates/nginx.conf .
    ```

    * replace `<REPLACE_SERVER_HOSTNAME>` with your hostname
    ```
    sed -i 's/<REPLACE_SERVER_HOSTNAME>/teahaz.co.uk/g' nginx_config
    ```
       Where teahaz.co.uk is replaced by your domain name.

    * Move the modified example config to the nginx default config file.
        if you already have some nginx config then just edit that
    ```
    cp nginx.conf /etc/nginx/nginx.conf
    ```

    * start/enable nginx
    ```
    systemctl enable nginx
    systemctl start nginx
    ```


2. Get ssl certificate from certbot (you can ofcourse use other services but some parts of the documentation might not apply to you)
   ```
    certbot certonly --webroot -w /teahouse/static -d YOUR_HOST_NAME
   ```
   **Note2:** replace `YOUR_HOST_NAME` with your servers hostname. **Do not**  include http[s]



3. run the server :)
 ```
 make run
 ```
 or 
 ```
 docker-compose up
 ```





