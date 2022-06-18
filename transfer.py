import sys
import os
import subprocess
from pathlib import Path

def call(cmd):
    status,out = subprocess.getstatusoutput(cmd)
    if status != 0:
        raise Exception(f"Error on call {cmd}, status:{status} out:{out}")
    return out


if sys.argv[1] == "save":

    out = call('docker images --format "{{.ID}},{{.Repository}},{{.Tag}},{{.Size}}"')

    for line in out.splitlines():
        id, repo, tag, size = line.split(",")
        image = repo + ":" + tag
        target = "docker-images/"+image
        
        Path(target).parent.mkdir(parents=True,exist_ok=True)
        cmd = f"docker save {image} -o {target}.tar"
        # print(id,repo,tag,size)
        print(cmd)
        os.system(cmd)

if sys.argv[1] == "load":

    files = list(Path("docker-images").rglob("*.tar"))
    for f in files:
        cmd = f"docker load -i {f}"
        print(cmd)
        os.system(cmd)
