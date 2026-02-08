import yaml
import os
from pathlib import Path
from typing import Iterable
from models import RecentUpdate

def write_browsertrix_seeds_yaml(
    updates: Iterable[RecentUpdate],
    path: str,
):
    
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data:dict = yaml.load(f, Loader=yaml.FullLoader)
            tmp = data.get('seeds', [{}])[0]
            data['seeds'] =  \
                data.get('seeds', []) + \
                [
                    {
                        **tmp,
                        'url': u.url
                    } for u in updates
                ]
    else:
        data = {
            "seeds": [
                {
                    "url": u.url,
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

def write_browsertrix_seeds_txt(
    updates: Iterable[RecentUpdate],
    path:str
):
    with open(path, "w+", encoding="utf-8") as f:
        f.writelines([f"""'{u.url}'\n""" for u in updates])
            