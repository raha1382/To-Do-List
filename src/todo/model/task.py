from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from ..utils.validators import  validate_name_of_task, validate_description_of_task, validate_status_of_task

@dataclass
class Task:
    name: int
    description: str = ""
    status: str = "todo"
    deadline : datetime = field(default_factory = datetime.now)

    def __post_init__(self):
        validate_name_of_task(self.name)
        validate_description_of_task(self.description)
        self.status = validate_status_of_task(self.status)