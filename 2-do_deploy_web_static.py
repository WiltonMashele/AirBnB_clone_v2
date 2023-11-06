#!/usr/bin/python3
"""
Distribute an archive to web servers using Fabric.
"""
from fabric.api import env, put, run, sudo
from os.path import isfile

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = '<username>'
env.key_filename = '<SSH key path>'  # Replace with your SSH key path

def do_deploy(archive_path):
    """
    Distribute an archive to web servers.

    Args:
        archive_path: Path to the archive file to deploy.

    Returns:
        True if successful, False otherwise.
    """
    if not isfile(archive_path):
        return False

    # Get the filename without extension
    archive_filename = archive_path.split("/")[-1].split(".")[0]

    # Upload the archive to the /tmp/ directory of the web server
    put(archive_path, "/tmp/")

    # Uncompress the archive to the folder /data/web_static/releases/<archive_filename>
    run("mkdir -p /data/web_static/releases/{}".format(archive_filename))
    run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(archive_filename + ".tgz", archive_filename))

    # Delete the archive from the web server
    run("rm /tmp/{}".format(archive_filename + ".tgz"))

    # Delete the symbolic link /data/web_static/current
    run("rm /data/web_static/current")

    # Create a new symbolic link /data/web_static/current linked to the new version
    run("ln -s /data/web_static/releases/{} /data/web_static/current".format(archive_filename))

    return True
