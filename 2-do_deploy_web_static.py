#!/usr/bin/python3
"""Function to deploy a compressed folder"""
from datetime import datetime
from fabric.api import env, put, run
import shlex
import os

env.hosts = ['44.211.97.124', '34.228.52.136']
env.user = "ubuntu"

def deploy_folder(archive_path):
    """Deploys a compressed folder"""
    if not os.path.exists(archive_path):
        return False

    try:
        archive_basename = os.path.basename(archive_path)
        archive_name = os.path.splitext(archive_basename)[0]

        releases_path = "/data/web_static/releases/{}".format(archive_name)
        tmp_path = "/tmp/{}".format(archive_basename)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(releases_path))
        run("tar -xzf {} -C {}".format(tmp_path, releases_path))
        run("rm {}".format(tmp_path))
        run("mv {}/web_static/* {}".format(releases_path, releases_path))
        run("rm -rf {}/web_static".format(releases_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(releases_path))
        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed:", str(e))
        return False
