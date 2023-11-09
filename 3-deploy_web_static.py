#!/usr/bin/python3
from fabric.api import put, run, local, env
from time import strftime
from datetime import date
from os import path

# Defining the target web server IP addresses
web_server_1_IP = '54.152.65.207'
web_server_2_IP = '52.206.72.6'

# SSH username and path to the private key
ssh_username = 'ubuntu'
path_to_private_key = '~/.ssh/school'

# Configuring Fabric environment
env.hosts = [web_server_1_IP, web_server_2_IP]
env.user = ssh_username
env.key_filename = path_to_private_key


def do_pack():
    """
    This method creates a .tgz archive from the contents of
    the web_static folder
    Returns:
        Archive path (success) or None (failure)
    """
    timestamp = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(timestamp))

        return "versions/web_static_{}.tgz".format(timestamp)

    except:
        return None


def do_deploy(archive_path):
    """The following function distributes an archive to web servers"""
    # Checking if the specified archive file exists
    if not (path.exists(archive_path)):
        return False
    try:
        # Extracting the filename and path
        tgz_file = archive_path.split("/")[-1]
        print(tgz_file)
        file_name = tgz_file.split(".")[0]
        print(file_name)
        path_name = "/data/web_static/releases/" + file_name

        # Uploading the archive to the /tmp/ dir on the web servers
        put(archive_path, '/tmp/')

        # Creating the release directory
        run("sudo mkdir -p /data/web_static/releases/{}/".format(file_name))

        # Uncompressing the archive into the release directory
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(tgz_file, file_name))

        # Removing the uploaded archive from the /tmp/ directory
        run("sudo rm /tmp/{}".format(tgz_file))

        # Moving the contents from the web_static subdir to the release dir
        run("sudo mv /data/web_static/releases/{}/web_static/* \
/data/web_static/releases/{}/".format(file_name, file_name))

        # Removing the now empty web_static/ subdir in the release dir
        run("sudo rm -rf /data/web_static/releases/{}/web_static"
            .format(file_name))

        # Removing the old symbolic link /data/web_static/current
        run("sudo rm -rf /data/web_static/current")

        # Creating a new symbolic link /data/web_static/current
        run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(file_name))
        return True
    except:
        return False


def deploy():
    """ This function run the function do_pack() and do_deploy() """

    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
