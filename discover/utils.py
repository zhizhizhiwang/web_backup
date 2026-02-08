import json
from pathlib import Path
from typing import Iterable
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from datetime import datetime, timezone, timedelta

from models import RecentUpdate


def update_to_dict(u: RecentUpdate) -> dict:
    return {
        "url": u.url,
        "title": u.title,
        "updated_at": u.updated_at,
        "updated_ts": u.updated_ts,
        "editor": u.editor,
        "editor_url": u.editor_url,
    }



def write_updates_json(updates: Iterable[RecentUpdate], path: str):
    data = [update_to_dict(u) for u in updates]
    Path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

def format_local_time(ts: int, tz=timezone.utc) -> str:
    return datetime.fromtimestamp(ts, tz).strftime("%Y-%m-%d %H:%M")

# =========================
# 渲染
# =========================

def render_updates_table(updates: list[RecentUpdate], limit: int = 20):
    console = Console()

    table = Table(
        title="📌 SCP-CN 最近更新页面",
        show_lines=False,
        header_style="bold cyan",
    )

    table.add_column("标题", style="bold", overflow="fold")
    table.add_column("更新时间(CST)", style="green", no_wrap=True)
    table.add_column("编辑者", style="yellow", no_wrap=True)
    table.add_column("URL", style="blue", overflow="fold")

    for u in updates[:limit] if limit != -1 else updates:
        table.add_row(
            u.title or "-",
            u.updated_at or "-",
            u.editor or "-",
            u.url,
        )

    console.print(table)

    if len(updates) > limit and limit != -1:
        console.print(
            f"[dim]… 还有 {len(updates) - limit} 条未显示[/dim]"
        )