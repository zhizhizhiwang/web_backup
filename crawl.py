import subprocess
from pathlib import Path
import sys
import argparse
from lib.log_processor import LogProcessor
from lib.docker_utils import docker_cmd, docker_popen

def win_to_wsl_path(path: Path) -> str:
    path = path.resolve()
    drive = path.drive[0].lower()
    rest = path.as_posix()[2:]
    return f"/mnt/{drive}{rest}"


def crawl(input_path: Path, seedfile: Path | None):
    mount_dir = input_path.parent
    wsl_mount_config = win_to_wsl_path(mount_dir)

    input_inside = f"/data/{input_path.name}"

    docker_opts = [
        "run", "--rm",
        "-v", f"{wsl_mount_config}:/data/",
        "-v", f"{wsl_mount_config}/crawls:/crawls/",
    ]

    container_args = [
        "crawl",
        "--config", input_inside,
    ]

    if seedfile:
        wsl_mount_seed = win_to_wsl_path(seedfile.parent)
        seed_inside = f"/seedfile/{seedfile.name}"
        docker_opts.extend([
            "-v", f"{wsl_mount_seed}:/seedfile/",
        ])
        container_args.extend([
            "--seedFile", seed_inside,
        ])

    cmd = docker_opts + [
        "webrecorder/browsertrix-crawler"
    ] + container_args

    print("Running:"," ".join(docker_cmd() + cmd))
    proc = docker_popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    processor = LogProcessor()

    for line in proc.stdout:
        processor.process_line(line.rstrip())

    for line in proc.stderr:
        processor.process_line(line.rstrip())

    processor.finalize()

    if processor.stats.failed_urls:
        with open("failed_urls.txt", "w", encoding="utf-8") as f:
            for url in sorted(processor.stats.failed_urls):
                f.write(url + "\n")
    
    return_code = proc.wait()
    
    if return_code != 0:
        raise RuntimeError(f"crawler exited with {return_code}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        prog="crawl",
        description="使用 browsertrix存档网页并生成warc",
    )

    ap.add_argument("--config", type=str, default="config.yaml", required=True)
    ap.add_argument("--seedfile", help="种子文件", default="")

    args = ap.parse_args()

    crawl(Path(args.config), Path(args.seedfile) if args.seedfile != "" else None)
