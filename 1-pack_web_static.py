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
    timestamp = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf {} versions/web_static_{}.tgz web_static/"
              .format(timestamp))

        return "versions/web_static_{}.tgz".format(timestamp)

    except Exception as e:
        return None
