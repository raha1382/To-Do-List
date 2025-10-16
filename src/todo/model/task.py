from dataclasses import dataclass, field
from typing import List
from datetime import datetime

class Task:
    name: int
    description: str = ""
    status: str = "todo"
    deadline : datetime = field(default_factory = datetime.now)

    def __post_init__(self):
        """Validate initial data after initialization."""
        if len(self.name.split()) > 30:
            raise ValueError("Project name exceeds 30 words")
        if len(self.description.split()) > 150:
            raise ValueError("Project description exceeds 150 words")