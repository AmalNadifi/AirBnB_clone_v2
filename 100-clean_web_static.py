#!/usr/bin/python3
"""
The following script defines a Fabric task to clean
out-of-date archives on web servers.
"""

import os
from fabric.api import *

# Defining the target web server IP addresses
web_server_1_IP = '54.152.65.207'
web_server_2_IP = '52.206.72.6'

# Setting the Fabric environment to the target IPs
env.hosts = [web_server_1_IP, web_server_2_IP]

def do_clean(number=0):
    """
    Delete out-of-date archives.

    Args:
        archives_to_keep (int): The number of archives to keep.

    This function deletes older archives, keeping the specified number of
    most recent archives in the 'versions' directory and on the remote server

    Returns:
        None
    """
    number = 1 if int(number) == 0 else int(number)

    # Deleting local out-of-date archives
    local_archives = sorted(os.listdir("versions"))
    [local_archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(archive)) for archive in local_archives]

    # Deleting remote out-of-date archives
    with cd("/data/web_static/releases"):
        remote_archives = run("ls -tr").split()
        remote_archives = [archive for archive in remote_archives if "web_static_" in archive]
        [remote_archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(archive)) for archive in remote_archives]
