#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static
sudo apt-get update -y
sudo apt-get install -y nginx

sudo mkdir -p /data/web_static/{releases,test,shared}
echo "Test deploying web_static" | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

nginx_config="/etc/nginx/sites-available/default"
nginx_config_location="/etc/nginx/sites-available/hbnb_static"
if [ ! -f "$nginx_config_location" ]; then
    echo "location /hbnb_static {" | sudo tee "$nginx_config_location"
    echo "    alias /data/web_static/current;" | sudo tee -a "$nginx_config_location"
    echo "}" | sudo tee -a "$nginx_config_location"
    sudo ln -s "$nginx_config_location" "/etc/nginx/sites-enabled/hbnb_static"
fi

sudo service nginx restart
