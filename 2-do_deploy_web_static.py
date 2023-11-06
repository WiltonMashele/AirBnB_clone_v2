#!/usr/bin/python3
"""
 Fabric script that distributes an archive to your web servers
"""


from fabric import Connection
import os


def do_deploy(archive_path):
    if not archive_path or not os.path.exists(archive_path):
        return False

    try:
        with Connection(env.hosts[0]) as server1, Connection(env.hosts[1]) as server2:
            for server in [server1, server2]:
                archived_file = os.path.basename(archive_path)
                newest_version = f"/data/web_static/releases/{archived_file[:-4]}"

                server.put(archive_path, "/tmp/")

                server.sudo(f"mkdir -p {newest_version}")
                server.sudo(f"tar -xzvf /tmp/{archived_file} -C {newest_version}")

                server.sudo(f"rm /tmp/{archived_file}")
                server.sudo("rm -rf /data/web_static/current")

                server.sudo(f"ln -s {newest_version} /data/web_static/current")

            print("New version deployed to both servers!")
            return True
    except Exception as e:
        print(f"Deployment failed: {str(e)}")
        return False
