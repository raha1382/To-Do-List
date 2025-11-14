from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from .task import Task
from ..utils.validators import validate_name_of_project, validate_description_of_project
from ..db.base import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

@dataclass
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    created_time = Column(DateTime, default=datetime.now)

    def __post_init__(self):
        validate_name_of_project(self.name)
        validate_description_of_project(self.description)