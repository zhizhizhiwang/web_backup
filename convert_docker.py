import subprocess
from pathlib import Path
import sys
import os
import argparse
from lib.docker_utils import docker_run, docker_cmd

def win_to_wsl_path(path: Path) -> str:
    path = path.resolve()
    drive = path.drive[0].lower()
    rest = path.as_posix()[2:]
    return f"/mnt/{drive}{rest}"


def resolve_warc_input(p: Path) -> Path:
    if p.is_file():
        return p

    archive = p / "archive"
    if archive.exists():
        return archive

    return p


def warc_to_zim_docker(input_path: Path, output_path: Path, args):
    input_path = resolve_warc_input(input_path.resolve())
    output_path = output_path.resolve()

    mount_dir = input_path.parent
    wsl_mount = win_to_wsl_path(mount_dir)

    input_inside = f"/data/{input_path.name}"
    output_inside = f"/data/{output_path.name}"
    os.mkdir(wsl_mount/output_path)
    

    cmd = [
        "run", "--rm",
        "-v", f"{wsl_mount}:/data",
        "ghcr.io/openzim/warc2zim",
        "warc2zim",    
        "--name", "test",
        input_inside,
        "--output", output_inside,
        *args
    ]

    print("Running:"," ".join(docker_cmd() + cmd))
    docker_run(cmd , check=True)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_docker.py <input> <output> [args]")
        sys.exit(1)

    
    warc_to_zim_docker(Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[2:])
