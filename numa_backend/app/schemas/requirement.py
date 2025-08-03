from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseSchema

class RequirementBase(BaseModel):
    title: str
    description: str
    status: Optional[str] = "pending"
    application_id: Optional[int] = None

class RequirementCreate(RequirementBase):
    user_id: int
    pass

class Requirement(RequirementBase, BaseSchema):
    user_id: int