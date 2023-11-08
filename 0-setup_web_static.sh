#!/usr/bin/env bash
# The following script sets up my web servers for the deployment of web_static
# Installing Nginx if not already installed
sudo apt-get update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'
# Creating necessary directories if they do not exist
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared
sudo touch /data/web_static/releases/test/index.html
# Creating a fake HTML FILE
sudo echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html
# Creating or recreating the symbolic link
sudo rm -f /data/web_static/current
sudo ln -sf /data/web_static/releases/test /data/web_static/current
# Giving the ownership to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/
# Updating the nginx configuration
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default
# Restarting Nginx
sudo service nginx restart
