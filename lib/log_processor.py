# lib/log_processor.py
import json
from collections import defaultdict
from .stats import CrawlStats
from .renderer import Renderer
from .log_utils import normalize_details

class LogProcessor:
    def __init__(self, fail_output="failed_urls.txt"):
        self.stats = CrawlStats()
        self.renderer = Renderer()
        self.fail_output = fail_output

    def process_line(self, line: str):
        if not line:
            return

        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            self.renderer.print_raw(line)
            return

        self._dispatch(obj)

    def _dispatch(self, obj: dict):
        ctx = obj.get("context")
        level = obj.get("logLevel")
        details = normalize_details(obj.get("details"))
        msg = obj.get("message")

        # crawl 进度
        if ctx == "crawlStatus" and isinstance(details, dict):
            self.stats.update_progress(details)
            self.renderer.update_progress(self.stats)
            return
        
        # init
        if ctx == "general" and msg in ("Seeds", "Behavior Options", "Link Selectors"):
            self.renderer.render_dict(details, msg = msg)
            return
        # worker 状态
        if ctx == "worker":
            self.stats.update_worker(obj)
            self.renderer.render_worker(obj)
            return

        # 页面状态
        if ctx == "pageStatus":
            self.renderer.render_page_status(obj)
            return

        # 错误（失败资源）
        if level in ("warn", "error"):
            self.stats.record_error(obj)
            self.renderer.render_error(obj)
            return

        # 其他信息
        self.renderer.render_info(obj)

    def finalize(self):
        if self.stats.failed_urls:
            with open(self.fail_output, "w", encoding="utf-8") as f:
                for url in sorted(self.stats.failed_urls):
                    f.write(url + "\n")
