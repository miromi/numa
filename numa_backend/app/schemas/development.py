from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseSchema

class DevelopmentTaskBase(BaseModel):
    title: str
    description: str
    status: Optional[str] = "todo"
    assigned_to: Optional[int] = None

class DevelopmentTaskCreate(DevelopmentTaskBase):
    solution_id: int
    pass

class DevelopmentTask(DevelopmentTaskBase, BaseSchema):
    solution_id: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None