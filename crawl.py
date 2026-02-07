import subprocess
from pathlib import Path
import sys
import os
import json
from rich.live import Live
from lib.ui import CrawlUI
from lib.log_processor import LogProcessor

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


def crawl(input_path: Path):
    input_path = resolve_warc_input(input_path.resolve())

    mount_dir = input_path.parent
    wsl_mount = win_to_wsl_path(mount_dir)

    input_inside = f"/data/{input_path.name}"
    

    cmd = [
        "wsl",
        "docker", "run", "--rm" ,
        "-v", f"{wsl_mount}:/data", 
        "-v", f"{wsl_mount}/crawls:/crawls/",
        "webrecorder/browsertrix-crawler",
        "crawl",
        "--config" , input_inside
    ]

    print("Running:", " ".join(cmd))
    proc = subprocess.Popen(
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
            for url in sorted(processor.state.failed_urls):
                f.write(url + "\n")
    
    return_code = proc.wait()
    
    if return_code != 0:
        raise RuntimeError(f"crawler exited with {return_code}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python crawl.py <path/to/config.yml>")
        sys.exit(1)

    crawl(Path(sys.argv[1]))
