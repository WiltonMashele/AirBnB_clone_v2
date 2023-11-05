#!/usr/bin/python3
"""Pack all contents within the 'web_static' directory into a .tgz archive."""
from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Pack all contents within the 'web_static' directory into a .tgz archive.
    The archive will be placed in the 'versions' directory.
    Returns:
        Path to the created archive if successful, None otherwise.
    """
    if not os.path.exists("versions"):
        local("mkdir versions")
    
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_name = "versions/web_static_{}.tgz".format(timestamp)
    command = "tar -czvf {} web_static".format(archive_name)
    result = local(command)

    if result.failed:
        return None

    return archive_name
