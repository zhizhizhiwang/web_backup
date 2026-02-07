# lib/ui.py
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.console import Group
from rich.text import Text


class CrawlUI:
    def __init__(self, console, state):
        self.console = console
        self.state = state

        self.progress = Progress(
            TextColumn("[bold blue]Crawl"),
            BarColumn(),
            TextColumn("{task.completed} pages"),
            TimeElapsedColumn(),
            console=console,
            transient=False,
        )

        self.task_id = self.progress.add_task("crawl", total=None)

    def update_progress(self):
        self.progress.update(
            self.task_id,
            completed=self.state.finished_pages,
        )

    def render_panel(self):
        lines = [
            f"[bold]当前页面[/bold]: {self.state.current_page or '-'}",
            f"[bold]已完成页[/bold]: {self.state.finished_pages}",
            f"[bold red]错误数[/bold red]: {self.state.error_count}",
            f"[bold yellow]失败 URL[/bold yellow]: {len(self.state.failed_urls)}",
        ]
        return Panel("\n".join(lines), title="Crawl Status", expand=True)

    def render(self):
        self.update_progress()
        return Group(
            self.progress,
            self.render_panel(),
        )
