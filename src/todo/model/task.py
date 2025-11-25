from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from ..utils.validators import validate_name_of_task, validate_description_of_task, validate_status_of_task, validate_deadline
from ..db.base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .enums import TaskStatus
@dataclass
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title= Column(String, unique=True, nullable=False)
    description= Column(String, nullable=True)
    status = Column(
        Enum(
            TaskStatus,
            name="task_status",
            native_enum=True,
            values_callable=lambda enum: [e.value for e in enum]
        ),
        server_default=TaskStatus.TODO.value ,
        nullable=False
    )
    deadline = Column(DateTime, nullable=True, default=datetime.now)
    project_name = Column(String, ForeignKey("projects.name", ondelete="CASCADE", onupdate="CASCADE"))
    # project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    project = relationship("Project", back_populates="tasks")

    def __post_init__(self):
        self.title = validate_name_of_task(self.title)
        validate_description_of_task(self.description)
        
        if isinstance(self.status, str):
            validated = validate_status_of_task(self.status)
            self.status = TaskStatus(validated)

        if self.deadline is not None:
            validate_deadline(self.deadline)