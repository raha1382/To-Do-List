from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from .task import Task
from ..utils.validators import validate_name_of_project, validate_description_of_project

@dataclass
class Project:
    name: int
    description: str = ""
    tasks: list[Task] = field(default_factory = list)
    created_time: datetime = field(default_factory = datetime.now)

    def __post_init__(self):
        validate_name_of_project(self.name)
        validate_description_of_project(self.description)