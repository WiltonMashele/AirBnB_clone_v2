#!/usr/bin/python3
"""Deployment script for web_static"""

from datetime import datetime
from fabric import Connection, task
import os

env.hosts = ['35.231.33.237', '34.74.155.163']
env.user = "ubuntu"


@task
def deploy():
    """Deploys the web_static content to the server"""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)


@task
def do_pack():
    """Creates a compressed archive of the web_static directory"""
    try:
        if not os.path.exists("versions"):
            local('mkdir versions')
        t = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f'versions/web_static_{t}.tgz'
        local('tar -czvf {} web_static'.format(archive_path))
        return archive_path
    except Exception as e:
        return None


@task
def do_deploy(archive_path):
    """Deploys the archive to the server"""
    if not os.path.exists(archive_path):
        return False

    try:
        remote_path = "/data/web_static/releases/"
        tmp_path = "/tmp/"

        with Connection(env.hosts[0]) as c:
            archive_name = archive_path.split('/')[-1]
            release_folder = archive_name.replace('.tgz', '').replace('.', ' ').split()[-1]

            c.put(archive_path, tmp_path)
            c.run(f'mkdir -p {remote_path}{release_folder}')
            c.run(f'tar -xzf {tmp_path}{archive_name} -C {remote_path}{release_folder}')
            c.run(f'rm {tmp_path}{archive_name}')
            c.run(f'mv {remote_path}{release_folder}/web_static/* {remote_path}{release_folder}')
            c.run(f'rm -rf {remote_path}{release_folder}/web_static')
            c.run('rm -rf /data/web_static/current')
            c.run(f'ln -s {remote_path}{release_folder} /data/web_static/current')
            print("New version deployed!")

        return True
    except Exception as e:
        return False
