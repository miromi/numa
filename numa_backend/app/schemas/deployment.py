from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseSchema

class DeploymentBase(BaseModel):
    name: str
    description: str
    status: Optional[str] = "pending"
    deployed_by: Optional[int] = None

class DeploymentCreate(DeploymentBase):
    development_task_id: int
    pass

class Deployment(DeploymentBase, BaseSchema):
    development_task_id: int
    deployed_at: Optional[datetime] = None