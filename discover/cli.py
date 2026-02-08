import argparse
import time
from rich.console import Console

from wikidot import main_crawl, LAST_TS
from browsertrix import write_browsertrix_seeds
from utils import  write_updates_json, render_updates_table



def main():
    console = Console()
    ap = argparse.ArgumentParser(
        prog="discover",
        description="Incremental discovery for web archiving",
    )

    ap.add_argument("site", choices=["wikidot"])
    ap.add_argument("--pages", type=int, default=5)
    ap.add_argument("--out", default="recent_updates.json")
    ap.add_argument("--browsertrix", help="output seeds.yaml")
    ap.add_argument("--since", help="time set (UTC)")

    args = ap.parse_args()

    if args.site == "wikidot":
        updates = main_crawl(
            max_pages=args.pages,
            since_ts=args.since or LAST_TS,
        )
    
    render_updates_table(updates, limit=15)
    
    write_updates_json(updates, args.out)
    if args.browsertrix:
        write_browsertrix_seeds(updates, args.browsertrix)
        console.print(f"[+] Browsertrix seeds written to {args.browsertrix}")

    console.print(f"[+] {len(updates)} updates discovered")


if __name__ == "__main__":
    main()
