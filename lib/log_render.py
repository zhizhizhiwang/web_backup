# lib/log_render.py
from datetime import datetime
from collections import defaultdict
from lib.log_utils import normalize_details
import time


def short_url(url: str, max_len=60) -> str:
    if not url:
        return ""
    if len(url) <= max_len:
        return url
    return url[:max_len - 3] + "..."


def fmt_ts(ts: str) -> str:
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%H:%M:%S")


_seen = defaultdict(float)

def should_print(key, interval=5):
    now = time.time()
    if now - _seen[key] > interval:
        _seen[key] = now
        return True
    return False


def render_human_log(obj: dict, enable_skip: bool = True) -> str:
    ts = fmt_ts(obj.get("timestamp", ""))
    level = obj.get("logLevel", "info").upper()
    ctx = obj.get("context", "-")

    raw_details = obj.get("details")
    details = normalize_details(raw_details)
    worker = details.get("workerid")
    
    worker_str = f"worker#{worker}" if worker is not None else ""

    msg = obj.get("message", "")

    if ctx == "fetch" and details.get("type") == "exception":
        return (
            f"[{ts}][{level}][{ctx}]"
            f"{'[' + worker_str + ']' if worker_str else ''}\n"
            f"  页面: {short_url(details.get('page'))}\n"
            f"  资源: {short_url(details.get('url'))}\n"
            f"  原因: {details.get('message')}"
        )

    key = (ctx, details.get("message"), details.get("url"))
    if enable_skip and not should_print(key):
        return ""

    return f"[{ts}][{level}][{ctx}] {msg}"
