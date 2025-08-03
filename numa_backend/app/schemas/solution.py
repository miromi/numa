from pydantic import BaseModel
from typing import Optional
from app.schemas.base import BaseSchema

class SolutionBase(BaseModel):
    title: str
    description: str
    status: Optional[str] = "clarifying"
    created_by: Optional[int] = None
    clarified: Optional[bool] = False

class SolutionCreate(SolutionBase):
    requirement_id: int
    created_by: int

class SolutionUpdate(BaseModel):
    status: Optional[str] = None
    clarified: Optional[bool] = None

class Solution(SolutionBase, BaseSchema):
    requirement_id: int
    created_by: int