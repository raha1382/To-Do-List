from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

TaskStatus = Literal["todo", "doing", "done"]

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    project_name: str = Field(..., description="Name of the existing project")

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    deadline: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    deadline: Optional[datetime]
    closed_at: Optional[datetime]
    project_name: str

    class Config:
        from_attributes = True