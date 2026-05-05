from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    id: Optional[int]
    title: str
    description: Optional[str]
    priority: int
    deadline: Optional[str]
    created_at: str
    completed_at: Optional[str]
    is_archived: int
