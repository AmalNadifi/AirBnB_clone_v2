#!/usr/bin/env bash
# The following script sets up my web servers for the deployment of web_static

# Installing Nginx if not already installed
sudo apt-get update
sudo apt-get -y install nginx

# Creating necessary directories if they do not exist
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# Creating a fake HTML FILE
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Creating or recreating the symbolic link
sudo rm -f /data/web_static/current
sudo ln -s /data/web_static/releases/test /data/web_static/current

# Giving the ownership to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Updating the nginx configurations
config_file="/etc/nginx/sites-available/default"
config_str="location /hbnb_static {\n    alias /data/web_static/current/;\n}\n"
if grep -q "location /hbnb_static" "$config_file"; then
  sudo sed -i "s|location /hbnb_static {.*}|$config_str|g" "$config_file"
else
  sudo sed -i "/location /i $config_str" "$config_file"
fi

# Restarting Nginx
sudo service nginx restart
