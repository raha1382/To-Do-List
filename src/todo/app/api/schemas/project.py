from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Project name")
    description: Optional[str] = Field(None, description="Project description")

class ProjectUpdatePut(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)

class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_time: datetime

    class Config:
        from_attributes = True