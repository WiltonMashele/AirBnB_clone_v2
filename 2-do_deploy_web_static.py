#!/usr/bin/python3
"""
 Fabric script that distributes an archive to your web servers
"""

from datetime import datetime
from fabric import Connection
import os

env = {
    "hosts": ["52.87.229.220", "100.26.240.45"],
    "user": "ubuntu",
    "archive_path": None,
}

def do_pack():
    """
    Create a compressed archive of the web_static folder.
    Returns the path to the archived file.
    """
    try:
        local("mkdir -p versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        archived_f_path = "versions/web_static_{}.tgz".format(date)
        local("tar -czvf {} web_static".format(archived_f_path))
        env["archive_path"] = archived_f_path
        return archived_f_path
    except Exception:
        return None

def do_deploy(archive_path):
    """
    Distribute the archive to the web servers and deploy it.
    """
    if not archive_path:
        archive_path = env.get("archive_path")

    if not archive_path or not os.path.exists(archive_path):
        return False

    try:
        with Connection(env["hosts"][0]) as conn:
            archived_file = os.path.basename(archive_path)
            newest_version = f"/data/web_static/releases/{archived_file[:-4]}"

            conn.put(archive_path, "/tmp/")
            conn.sudo(f"mkdir -p {newest_version}")
            conn.sudo(f"tar -xzvf /tmp/{archived_file} -C {newest_version}")
            conn.sudo(f"rm /tmp/{archived_file}")
            conn.sudo(f"mv {newest_version}/web_static/* {newest_version}/")
            conn.sudo(f"rm -rf {newest_version}/web_static")
            conn.sudo("rm -rf /data/web_static/current")
            conn.sudo(f"ln -s {newest_version} /data/web_static/current")
            print("New version deployed!")
            return True
    except Exception:
        return False

if __name__ == "__main__":
    env["archive_path"] = do_pack()
    if not env["archive_path"]:
        print("Packaging failed. Deployment aborted.")
    elif not do_deploy(env["archive_path"]):
        print("Deployment failed.")
