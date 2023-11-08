#!/usr/bin/python3
""" This module  generates a .tgz archive from the contents of the web_static
folder of the AirBnB Clone repo, using the function do_pack
"""
from fabric.api import local
from time import strftime
from datetime import date


def do_pack():
    """
    This method creates a .tgz archive from the contents of
    the web_static folder
    Returns:
        Archive path (success) or None (failure)
    """
    try:
        current_time = datetime.now()
        timestamp = current_time.strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)

        local("mkdir -p versions")
        local("tar -czvf {} web_static".format(archive_path))

        return archive_path
    except Exception as e:
        return None
