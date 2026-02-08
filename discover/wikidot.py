import re
import time
import requests
from lxml import html
from urllib.parse import urljoin
from dataclasses import dataclass
from typing import List, Optional
from rich.console import Console
from datetime import datetime, timezone, timedelta


from models import RecentUpdate
from utils import write_updates_json, format_local_time, render_updates_table


BASE = "https://scp-wiki-cn.wikidot.com"
LIST_URL = BASE + "/most-recently-edited/p/{}"
TIME_RE = re.compile(r"time_(\d+)")

LAST_TS = 1770336000 #2026-02-06 00:00:00 CST

CST = timezone(timedelta(hours=8)) # UTC+8


# =========================
# HTTP Client（反爬层）
# =========================

def build_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": BASE + "/",
    })
    return s


def warmup(session: requests.Session):
    r = session.get(BASE + "/", timeout=20)
    r.raise_for_status()


# =========================
# Wikidot 解析逻辑
# =========================

def parse_page(session: requests.Session, page: int) -> List[RecentUpdate]:
    url = LIST_URL.format(page)
    r = session.get(url, timeout=20)
    r.raise_for_status()

    tree = html.fromstring(r.text)

    rows = tree.xpath(
        r'''//*[@id="page-content"]/div[2]/div[3]/div/table/tr[position()>1]'''
    )

    items: List[RecentUpdate] = []

    for tr in rows:
        href = tr.xpath(r"./td[1]/div/div[1]/a[1]/@href")
        title = tr.xpath(r"./td[1]/div/div[1]/a[1]/text()")

        time_text = tr.xpath(r"./td[2]/span/text()") # no use: 没法控制是按照哪个时区算出来的
        time_class = tr.xpath(r"./td[2]/span/@class")

        editor = tr.xpath(r"./td[3]/span[last()]/a[last()]/text()")
        editor_url = tr.xpath(r"./td[3]/span[last()]/a[last()]/@href")

        if not href:
            continue

        ts = None
        if time_class:
            m = TIME_RE.search(time_class[0])
            if m:
                ts = int(m.group(1))

        items.append(RecentUpdate(
            url=urljoin(BASE, href[0]),
            title=title[0].strip() if title else None,
            updated_at=format_local_time(ts) if ts else None,
            updated_ts=ts,
            editor=editor[0].strip() if editor else None,
            editor_url=editor_url[0] if editor_url else None,
        ))

    return items


def crawl_recent(session: requests.Session, max_pages=50, after_ts = LAST_TS) -> List[RecentUpdate]:
    results: List[RecentUpdate] = []

    for page in range(1, max_pages + 1):
        print(f"[*] Fetch page {page}")
        items = parse_page(session, page)

        if not items:
            break

        for item in items:
            if item.updated_ts and item.updated_ts <= after_ts:
                print("[*] Reached old entries, stop.")
                return results
            results.append(item)

    return results

# =========================
# 入口
# =========================

def main_crawl(max_pages: int = 30, since_ts = LAST_TS):
    console = Console()

    session = build_session()
    console.print("[cyan]Warming up session…[/cyan]")
    warmup(session)

    console.print("[cyan]Fetching recent updates…[/cyan]")
    updates = crawl_recent(session, max_pages, since_ts)
    
    return updates
    

if __name__ == "__main__":
    console = Console()
    
    updates = main_crawl(max_pages=5)
    
    render_updates_table(updates, limit=-1)
    output_path = "recent_updates.json"
    write_updates_json(updates, output_path)

    console.print(
        f"[green]✔ JSON 已写入[/green] [bold]{output_path}[/bold]"
    )

