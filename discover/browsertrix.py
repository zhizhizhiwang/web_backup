import yaml
from typing import Iterable
from models import RecentUpdate

def write_browsertrix_seeds(
    updates: Iterable[RecentUpdate],
    path: str,
):
    data = {
        "seeds": [
            {
                "url": u.url,
                "metadata": {
                    "lastmod": u.updated_ts,
                }
            }
            for u in updates
        ]
    }

    with open(path, "w+", encoding="utf-8") as f:
        yaml.safe_dump(
            data,
            f,
            allow_unicode=True,
            sort_keys=False,
        )
