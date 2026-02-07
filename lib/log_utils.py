# lib/log_utils.py
from typing import Any, Dict
import json


def normalize_details(details: Any) -> Dict:
    """
    Browsertrix logs:
    - dict        → 原样返回
    - list[dict]  → 返回第一个 dict
    - 其它        → 返回空 dict
    """
    if isinstance(details, dict):
        return details

    if isinstance(details, list) and details:
        first = details[0]
        if isinstance(first, dict):
            return first

    return {}

