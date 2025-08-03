from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseSchema

class RequirementBase(BaseModel):
    title: str
    description: str
    status: Optional[str] = "pending"
    application_id: Optional[int] = None
    assigned_to: Optional[int] = None
    branch_name: Optional[str] = None
    spec_document: Optional[str] = None

class RequirementCreate(RequirementBase):
    user_id: int
    pass

class RequirementUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[int] = None
    branch_name: Optional[str] = None
    spec_document: Optional[str] = None

class Requirement(RequirementBase, BaseSchema):
    user_id: int