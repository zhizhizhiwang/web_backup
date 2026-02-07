# lib/stats.py
from collections import defaultdict

class CrawlStats:
    def __init__(self):
        self.crawled = 0
        self.total = 0
        self.pending = 0
        self.failed = 0

        self.worker_pages = {}
        self.failed_urls = set()
        self.error_count = defaultdict(int)

    def update_progress(self, d: dict):
        self.crawled = d.get("crawled", self.crawled)
        self.total = d.get("total", self.total)
        self.pending = d.get("pending", self.pending)
        self.failed = d.get("failed", self.failed)

    def update_worker(self, obj: dict):
        d = obj.get("details") or {}
        wid = d.get("workerid")
        page = d.get("page")
        if wid is not None and page:
            self.worker_pages[wid] = page

    def record_error(self, obj: dict):
        d = obj.get("details") or {}
        url = d.get("url")
        if url:
            self.failed_urls.add(url)
            self.error_count[obj.get("context")] += 1
