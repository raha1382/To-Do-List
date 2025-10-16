from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from .task import Task
from ..utils.utils import MAX_PROJECT_NAME_WORDS, MAX_PROJECT_DESCRIPTION_WORDS

@dataclass
class Project:
    name: int
    description: str = ""
    tasks: list[Task] = field(default_factory = list)
    created_time: datetime = field(default_factory = datetime.now)

    def __post_init__(self):
        """Validate initial data after initialization."""
        if len(self.name.split()) <= MAX_PROJECT_NAME_WORD:
            raise ValueError("Project name exceeds 30 words")
        if len(self.description.split()) <= MAX_PROJECT_DESCRIPTION_WORD:
            raise ValueError("Project description exceeds 150 words")