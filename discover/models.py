from dataclasses import dataclass
from typing import List, Optional

@dataclass
class RecentUpdate:
    url: str
    title: Optional[str]
    updated_at: Optional[str]
    updated_ts: Optional[int]
    editor: Optional[str]
    editor_url: Optional[str]
