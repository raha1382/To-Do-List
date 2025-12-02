from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime
from todo.utils.validators import (
    validate_name_of_task,
    validate_description_of_task,
    validate_status_of_task,
    validate_deadline,
)


def strip_text(value: Optional[str | datetime]):
    if value is None:
        return value

    if isinstance(value, str):
        value = value.strip()
        if value == "":
            raise ValueError("Value cannot be empty or whitespace only.")

    elif isinstance(value, datetime):
        value = validate_deadline(value)

    return value

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    project_name: str = Field(..., description="Name of the existing project")

    @validator("title", "description", "project_name", "deadline", pre=True)
    def strip_fields(cls, v):
        return strip_text(v)

    @validator("title")
    def validate_title(cls, value):
        return validate_name_of_task(value)

    @validator("description", pre=True)
    def validate_desc(cls, value):
        if value is None:
            return value
        return validate_description_of_task(value)

    @validator("deadline", pre=True)
    def validate_deadline_field(cls, value):
        return validate_deadline(value)
    

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[datetime] = None

    @validator("title", "description", "status", "deadline", pre=True)
    def strip_fields(cls, v):
        return strip_text(v)

    @validator("title")
    def validate_title(cls, value):
        if value is None:
            return value
        return validate_name_of_task(value)

    @validator("description")
    def validate_desc(cls, value):
        if value is None:
            return value
        return validate_description_of_task(value)

    @validator("status", pre=True)
    def validate_status(cls, value):
        if value is None:
            return value
        return validate_status_of_task(value)

    @validator("deadline", pre=True)
    def validate_deadline_field(cls, value):
        return validate_deadline(value)
    
    
class TaskStatusUpdate(BaseModel):
    status: str = Field(..., min_length=1)

    @validator("status", pre=True)
    def clean_and_validate_status(cls, value):
        value = strip_text(value)
        return validate_status_of_task(value)
    
    

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