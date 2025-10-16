from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from .task import Task

@dataclass
class Project:
    name: int
    description: str = ""
    tasks: list[Task] = field(default_factory = list)
    created_time: datetime = field(default_factory = datetime.now)

    def __post_init__(self):
        """Validate initial data after initialization."""
        if len(self.name.split()) > 30:
            raise ValueError("Project name exceeds 30 words")
        if len(self.description.split()) > 150:
            raise ValueError("Project description exceeds 150 words")