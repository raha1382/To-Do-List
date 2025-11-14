from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from ..utils.validators import validate_name_of_task, validate_description_of_task, validate_status_of_task, validate_deadline
from ..db.base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

class TaskStatus(PyEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

@dataclass
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title= Column(String, unique=True, nullable=False)
    description= Column(String, nullable=True)
    status = Column(
        Enum(TaskStatus, name="task_status", native_enum=True),
        default=TaskStatus.TODO,
        nullable=False,
    )
    deadline = Column(DateTime, nullable=True, default=datetime.now)
    project_name = Column(String, ForeignKey("projects.name", ondelete="CASCADE"))
    # project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    project = relationship("Project", back_populates="tasks")

    def __post_init__(self):
        self.title = validate_name_of_task(self.title)
        validate_description_of_task(self.description)
        self.status = validate_status_of_task(self.status)
        if self.deadline is not None:
            validate_deadline(self.deadline)