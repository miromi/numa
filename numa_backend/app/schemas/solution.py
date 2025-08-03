from pydantic import BaseModel
from typing import Optional
from app.schemas.base import BaseSchema
from app.schemas.requirement import Requirement
from app.schemas.application import Application

class SolutionBase(BaseModel):
    title: str
    description: str
    status: Optional[str] = "clarifying"
    created_by: Optional[int] = None
    clarified: Optional[bool] = False
    application_id: Optional[int] = None

class SolutionCreate(SolutionBase):
    requirement_id: int
    created_by: int
    application_id: int

class SolutionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    clarified: Optional[bool] = None
    application_id: Optional[int] = None

class Solution(SolutionBase, BaseSchema):
    requirement_id: int
    created_by: int
    application_id: Optional[int]  # 修改为可选
    # 关联对象
    requirement: Optional[Requirement] = None
    application: Optional[Application] = None