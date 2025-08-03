from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseSchema

class EventLogBase(BaseModel):
    event_type: str
    description: str
    user_id: int
    requirement_id: Optional[int] = None
    question_id: Optional[int] = None

class EventLogCreate(EventLogBase):
    pass

class EventLog(EventLogBase, BaseSchema):
    pass