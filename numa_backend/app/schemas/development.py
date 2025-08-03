from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseSchema
from app.schemas.solution import Solution
from app.schemas.requirement import Requirement
from app.schemas.application import Application

class DevelopmentTaskBase(BaseModel):
    title: str
    description: str
    status: Optional[str] = "todo"
    assigned_to: Optional[int] = None
    code_branch: Optional[str] = None

class DevelopmentTaskCreate(DevelopmentTaskBase):
    solution_id: int
    requirement_id: int
    application_id: int

class DevelopmentTaskUpdate(DevelopmentTaskBase):
    pass

class DevelopmentTask(DevelopmentTaskBase, BaseSchema):
    solution_id: int
    requirement_id: int
    application_id: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    # 关联对象
    solution: Optional[Solution] = None
    requirement: Optional[Requirement] = None
    application: Optional[Application] = None