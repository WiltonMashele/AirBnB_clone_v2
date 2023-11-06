#!/usr/bin/python3
"""
Distribute an archive to web servers using Fabric.
"""
from datetime import datetime
from fabric import Connection
import os


env.hosts = ["172.17.0.9", "172.17.255.255"]
env.user = "ubuntu"

def do_pack():
    """
    Create an archive and return its path if it's generated successfully.
    """
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archived_file_path = "versions/web_static_{}.tgz".format(date)
    result = local("tar -czvf {} web_static".format(archived_file_path))

    if result.succeeded:
        return archived_file_path
    else:
        return None

def do_deploy(archive_path):
    """
    Distribute an archive to web servers.
    """
    if os.path.exists(archive_path):
        archived_file = os.path.basename(archive_path)
        newest_version = "/data/web_static/releases/{}".format(archived_file[:-4])
        archived_file = "/tmp/{}".format(archived_file)
