# lib/log_state.py
from dataclasses import dataclass, field
from typing import Optional, Set
from lib.log_utils import normalize_details


@dataclass
class CrawlState:
    finished_pages: int = 0
    current_page: Optional[str] = None
    error_count: int = 0
    failed_urls: Set[str] = field(default_factory=set)

    def on_event(self, obj: dict):
        ctx = obj.get("context")
        details = normalize_details(obj.get("details"))

        # 当前页面
        if ctx == "fetch":
            page = details.get("page")
            if page:
                self.current_page = page

            if details.get("type") == "exception":
                self.error_count += 1
                url = details.get("url")
                if url:
                    self.failed_urls.add(url)

        # 页面完成（这是经验规则）
        if ctx == "crawlStatus" and "finished" in obj.get("message", ""):
            self.finished_pages += 1
