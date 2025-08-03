from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseSchema

class QuestionBase(BaseModel):
    content: str
    requirement_id: int
    created_by: int

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    answer: Optional[str] = None
    answered_by: Optional[int] = None
    clarified: Optional[bool] = None
    clarified_by: Optional[int] = None

class Question(QuestionBase, BaseSchema):
    answer: Optional[str] = None
    answered_by: Optional[int] = None
    clarified: bool = False
    clarified_by: Optional[int] = None