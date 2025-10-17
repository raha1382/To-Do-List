from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from ..utils.validators import validate_name_of_task, validate_description_of_task, validate_status_of_task

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    status: str = "todo"
    deadline: Optional[datetime] = field(default_factory=datetime.now)
    project_name: Optional[str] = None

    def __post_init__(self):
        self.title = validate_name_of_task(self.title)
        validate_description_of_task(self.description)
        self.status = validate_status_of_task(self.status)