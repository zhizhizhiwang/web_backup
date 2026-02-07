# lib/renderer.py
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
from .log_utils import normalize_details

import json


def dict_to_panel(data, title="字典数据", expand=True):
    """将字典转换为面板显示"""
    if expand:
        content = json.dumps(data, indent=2, ensure_ascii=False)
    else:
        content = json.dumps(data, ensure_ascii=False)
    
    return Panel.fit(
        content,
        title=f"[bold]{title}[/bold]",
        border_style="green",
        padding=(1, 2)
    )

class Renderer:
    def __init__(self):
        self.console = Console()
        self.progress = Progress(
            TextColumn("[bold cyan]Crawl"),
            BarColumn(),
            TextColumn("{task.percentage:>3.0f}%"),
            TextColumn("({task.completed}/{task.total})"),
            console=self.console,
        )
        self.task = None
        self.progress.start()

    def update_progress(self, stats):
        if self.task is None:
            self.task = self.progress.add_task(
                "crawl", total=max(stats.total, 1)
            )
        self.progress.update(
            self.task,
            completed=stats.crawled,
            total=stats.total or 1
        )

    def render_dict(self, obj, msg):
        if not isinstance(obj, dict):
            return
        self.console.print(
            dict_to_panel(
                obj,
                title=msg
            )
        )

    def render_worker(self, obj):
        d = obj.get("details") or {}
        wid = d.get("workerid")
        page = d.get("page")
        if page:
            self.console.print(
                Panel.fit(
                    f"[bold]Worker {wid}[/bold]\n{page}",
                    title="Current Page",
                    border_style="cyan",
                )
            )

    def render_error(self, obj):
        ctx = obj.get("context")
        msg = obj.get("message")
        d = normalize_details(obj.get("details"))
        url = d.get("url")
        page = d.get("page")

        text = Text()
        text.append(f"[{ctx}] ", style="bold red")
        text.append(msg + "\n")
        if page:
            text.append(f"Page: {page}\n", style="dim")
        if url:
            text.append(f"URL: {url}", style="yellow")

        self.console.print(text)

    def render_page_status(self, obj):
        d = obj.get("details") or {}
        page = d.get("page")
        if page:
            self.console.print(f"[green]✔ Page Finished[/green] {page}")

    def render_info(self, obj):
        self.console.print(obj.get("message", ""), style="dim")

    def print_raw(self, line):
        self.console.print(line, style="dim")
