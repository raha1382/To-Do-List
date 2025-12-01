from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from todo.utils.validators import (
    validate_name_of_project,
    validate_description_of_project,
)

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Project name")
    description: Optional[str] = Field(None, description="Project description")

    @validator("name", "description", pre=True)
    def strip_and_reject_empty(cls, value):
        if value is None:
            return value

        value = value.strip()

        if value == "":
            raise ValueError("Value cannot be empty or whitespace.")

        return value

    @validator("name")
    def validate_name(cls, value):
        return validate_name_of_project(value)

    @validator("description")
    def validate_description(cls, value):
        if value is None:
            return value
        return validate_description_of_project(value)
    

class ProjectUpdatePut(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)

    @validator("name", "description", pre=True)
    def strip_and_reject_empty(cls, value):
        if value is None:
            return value
        value = value.strip()
        if value == "":
            raise ValueError("Value cannot be empty.")
        return value

    @validator("name")
    def validate_name(cls, value):
        return validate_name_of_project(value)

    @validator("description")
    def validate_description(cls, value):
        return validate_description_of_project(value)
    

class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    description: Optional[str] = None

    @validator("name", "description", pre=True)
    def strip_and_reject_empty(cls, value):
        if value is None:
            return value
        value = value.strip()
        if value == "":
            raise ValueError("Value cannot be empty.")
        return value

    @validator("name")
    def validate_name(cls, value):
        if value is None:
            return value
        return validate_name_of_project(value)

    @validator("description")
    def validate_description(cls, value):
        if value is None:
            return value
        return validate_description_of_project(value)
    

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_time: datetime

    class Config:
        from_attributes = True