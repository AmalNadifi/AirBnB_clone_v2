#!/usr/bin/python3
"""
The following script defines a Fabric task to clean
out-of-date archives on web servers
"""
import os
from fabric.api import *


# Setting the Fabric environment to the target IPs
env.hosts = ['54.152.65.207', '52.206.72.6']


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
    [local_archives.pop() for x in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(arch)) for arch in local_archives]

    # Deleting remote out-of-date archives
    with cd("/data/web_static/releases"):
        r_archives = run("ls -tr").split()
        r_archives = [arch for arch in r_archives if "web_static_" in arch]
        [r_archives.pop() for x in range(number)]
        [run("rm -rf ./{}".format(arch)) for arch in r_archives]
