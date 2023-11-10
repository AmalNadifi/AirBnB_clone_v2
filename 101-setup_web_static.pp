# The following puppet script is to setup web servers for web_static

# Ensuring Nginx is installed
package { 'nginx':
  ensure => 'installed',
}

# Ensuring the existence of required directories
file { '/data':
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
} ->
file { '/data/web_static':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
} ->
file { '/data/web_static/releases':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
} ->
file { '/data/web_static/releases/test':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
} ->
file { '/data/web_static/shared':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Creating an 'index.html' file for the test release
file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => @(HTML)
    <html>
      <head>
      </head>
      <body>
        Holberton School
      </body>
    </html>
  HTML
}

# Setting ownership for the 'index.html' file
exec { 'set_owner_index_html':
  command => 'chown ubuntu:ubuntu /data/web_static/releases/test/index.html',
  path    => '/bin:/usr/bin',
  require => File['/data/web_static/releases/test/index.html'],
}

# Setting mode for the 'index.html' file
exec { 'set_mode_index_html':
  command => 'chmod 0644 /data/web_static/releases/test/index.html',
  path    => '/bin:/usr/bin',
  require => File['/data/web_static/releases/test/index.html'],
}

# Creating or recreating the symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  force  => true,
}

# Updating Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => "
    server {
      listen 80 default_server;
      listen [::]:80 default_server;
      add_header X-Served-By ${hostname};
      root   /var/www/html;
      index  index.html index.htm;

      location /hbnb_static {
          alias /data/web_static/current;
          index index.html index.htm;
      }

      location /redirect_me {
          return 301 http://github.com/AmalNadifi;
      }

      error_page 404 /404.html;
      location /404 {
        root /var/www/html;
        internal;
      }
    }
  ",
} ->

# Restarting Nginx service
exec { 'nginx_restart':
  command => '/bin/systemctl restart nginx',
  path    => '/bin:/usr/bin',
  require => File['/etc/nginx/sites-available/default'],
}
