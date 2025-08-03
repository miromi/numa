from pydantic import BaseModel
from typing import Optional
from app.schemas.base import BaseSchema

class SolutionBase(BaseModel):
    title: str
    description: str
    status: Optional[str] = "proposed"

class SolutionCreate(SolutionBase):
    requirement_id: int
    pass

class Solution(SolutionBase, BaseSchema):
    requirement_id: int
    pass