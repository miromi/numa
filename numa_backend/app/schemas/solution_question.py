from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseSchema

class SolutionQuestionBase(BaseModel):
    content: str
    solution_id: int
    created_by: int

class SolutionQuestionCreate(SolutionQuestionBase):
    pass

class SolutionQuestionUpdate(BaseModel):
    answer: Optional[str] = None
    answered_by: Optional[int] = None
    clarified: Optional[bool] = None
    clarified_by: Optional[int] = None

class SolutionQuestion(SolutionQuestionBase, BaseSchema):
    answer: Optional[str] = None
    answered_by: Optional[int] = None
    clarified: bool = False
    clarified_by: Optional[int] = None