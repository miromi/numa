from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseSchema

class ApplicationBase(BaseModel):
    name: str
    description: str
    repository_url: Optional[str] = None
    status: Optional[str] = "created"

class ApplicationCreate(ApplicationBase):
    development_task_id: int
    created_by: int
    pass

class Application(ApplicationBase, BaseSchema):
    development_task_id: int
    created_by: int
    built_at: Optional[datetime] = None