#!/usr/bin/python3
""" generates a .tgz archive
"""
from fabric.api import local, env, put, run
from datetime import datetime
from os import path
from fabric.decorators import runs_once


env.hosts = ['54.152.65.207', '52.206.72.6']

# Set the username
env.user = "ubuntu"

# Set private key path
env.key_filename = "~/.ssh/school"


@runs_once
def do_pack():
    """ generates a .tgz archive from the contents of
    the web_static folder of your AirBnB Clone repo
    """

    local("mkdir -p versions")
    dformat = "%Y%m%d%H%M%S"
    archive_path = "versions/web_static_{}.tgz".format(
            datetime.strftime(datetime.now(), dformat))
    result = local("sudo tar -cvzf {} web_static".format(archive_path))
    if result.failed:
        return None
    return archive_path


def do_deploy(archive_path):
    """distributes an archive to your web servers"""

    try:
        if not path.exists(archive_path):
            return False

        dir_path = "/data/web_static/releases/"
        filename = path.basename(archive_path)
        file_no_ext, ext = path.splitext(filename)
        put(archive_path, "/tmp/{}".format(filename))
        run("sudo rm -rf {}{}".format(dir_path, file_no_ext))
        run("sudo mkdir -p {}{}".format(dir_path, file_without_ext))
        run("sudo tar -xzf /tmp/{} -C {}{}".format(filename, dir_path, file_no_ext))
        run("sudo rm /tmp/{}".format(filename))
        run("sudo mv {0}{1}/web_static/* {0}{1}/".format(dir_path, file_no_ext))
        run("sudo rm -rf {}{}/web_static".format(dir_path, file_no_ext))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {}{}/ /data/web_static/current".format(
            dir_path, file_no_ext))
        print("New version deployed!")
        return True
    except Exception:
        return False
    """# Checking if the specified archive file exists
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
        run("sudo tar -zxvf /tmp/{} -C /data/web_static/releases/{}/"
            .format(tgz_file, file_name))

        # Removing the uploaded archive from the /tmp/ directory
        run("sudo rm /tmp/{}".format(tgz_file))

        # Moving the contents from the web_static subdir to the release dir
        run("sudo mv /data/web_static/releases/{}/web_static/*\
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
    except Exception as e:
        return False"""
