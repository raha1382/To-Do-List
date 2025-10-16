from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from ..utils.utils import  MAX_TASK_TITLE_WORDS, MAX_TASK_DESCRIPTION_WORDS, TASK_STATUS

class Task:
    name: int
    description: str = ""
    status: str = "todo"
    deadline : datetime = field(default_factory = datetime.now)

    def __post_init__(self):
        """Validate initial data after initialization."""
        if len(self.name.split()) <= MAX_TASK_NAME_WORD:
            raise ValueError("Project name exceeds 30 words")
        if len(self.description.split()) <= MAX_TASK_DESCRIPTION_WORD:
            raise ValueError("Project description exceeds 150 words")