import os
import sys
import json
import subprocess
from typing import List

CONFIG_FILE = "config.json"


class DockerError(RuntimeError):
    """Docker 环境相关错误"""


# ---------------------------
# 配置管理
# ---------------------------

def _load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _save_config(cfg: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def get_config_docker_path() -> str:
    cfg = _load_config()
    return cfg.get("docker_path", "")


def set_config_docker_path(path: str):
    cfg = _load_config()
    cfg["docker_path"] = path
    _save_config(cfg)


# ---------------------------
# subprocess 封装
# ---------------------------

def _run(cmd: List[str], timeout: int = 8) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout
    )


def _docker_works(cmd: List[str]) -> bool:
    try:
        cp = _run(cmd + ["version"])
        return cp.returncode == 0
    except Exception:
        return False


# ---------------------------
# docker 路径规范化
# ---------------------------

def _normalize_docker_path(path: str) -> str:
    """
    将用户输入路径规范化为 docker 可执行文件
    - 如果是目录 → 自动补 docker / docker.exe
    - 如果是文件 → 检查可执行
    """
    path = os.path.expanduser(path)
    path = os.path.abspath(path)

    if os.path.isdir(path):
        exe_name = "docker.exe" if sys.platform == "win32" else "docker"
        candidate = os.path.join(path, exe_name)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
        raise DockerError(f"在目录中未找到 docker 可执行文件: {path}")

    if os.path.isfile(path) and os.access(path, os.X_OK):
        return path

    raise DockerError(f"无效的 docker 路径: {path}")


# ---------------------------
# 用户输入
# ---------------------------

def _ask_user_for_docker_path() -> str:
    print("未配置 docker 路径，请输入 docker 可执行文件完整路径，或直接回车自动探测:")
    path = input("docker 路径: ").strip()
    return path if path else None


# ---------------------------
# docker 命令探测
# ---------------------------

def docker_cmd() -> List[str]:
    """
    获取可用 docker 命令前缀
    优先使用配置，首次运行自动探测并写入配置
    """
    path = get_config_docker_path()

    # 使用配置
    if path:
        if path in ["docker", "wsl docker"]:
            parts = path.split()
            if _docker_works(parts):
                return parts
        else:
            try:
                path = _normalize_docker_path(path)
                if _docker_works([path]):
                    return [path]
            except DockerError:
                pass
        print(f"已配置 docker 路径 '{path}' 无效，将自动探测或重新配置。")

    # 首次输入
    user_path = _ask_user_for_docker_path()
    if user_path:
        try:
            norm_path = _normalize_docker_path(user_path)
            if _docker_works([norm_path]):
                set_config_docker_path(norm_path)
                return [norm_path]
            else:
                print(f"用户指定的 docker 路径 '{norm_path}' 无效，将自动探测。")
        except DockerError as e:
            print(f"{e}，将自动探测。")

    # 自动探测 PATH docker
    if _docker_works(["docker"]):
        set_config_docker_path("docker")
        return ["docker"]

    # 自动探测 Windows WSL docker
    if sys.platform == "win32" and _docker_works(["wsl", "docker"]):
        set_config_docker_path("wsl docker")
        return ["wsl", "docker"]

    raise DockerError("未找到可用的 Docker，请安装 Docker 或检查路径配置。")


# ---------------------------
# docker 调用
# ---------------------------

def docker_run(args: List[str]) -> subprocess.CompletedProcess:
    """
    阻塞 docker 调用
    """
    prefix = docker_cmd()
    return subprocess.run(prefix + args)


def docker_popen(args: List[str], **kwargs) -> subprocess.Popen:
    """
    非阻塞 docker 调用
    """
    prefix = docker_cmd()
    return subprocess.Popen(prefix + args, **kwargs)


# ---------------------------
# 镜像管理
# ---------------------------

def image_exists(image: str) -> bool:
    """
    检查镜像是否存在
    """
    prefix = docker_cmd()
    cp = _run(prefix + ["image", "inspect", image])
    return cp.returncode == 0


def ensure_image(image: str, pull: bool = True):
    """
    确保镜像存在，pull=True 时不存在自动拉取
    """
    if image_exists(image):
        return
    if not pull:
        raise DockerError(f"本地未找到 Docker 镜像: {image}")
    print(f"本地未找到镜像 {image}，正在拉取...")
    cp = subprocess.run(docker_cmd() + ["pull", image])
    if cp.returncode != 0:
        raise DockerError(f"拉取镜像失败: {image}")


# ---------------------------
# 调试信息
# ---------------------------

def docker_summary() -> dict:
    """
    返回 Docker 环境摘要，用于调试
    """
    summary = {
        "docker_path": get_config_docker_path(),
        "platform": sys.platform,
    }

    try:
        cp = _run(docker_cmd() + ["--version"])
        summary["version"] = cp.stdout.strip()
    except Exception:
        summary["version"] = "未知"

    return summary
