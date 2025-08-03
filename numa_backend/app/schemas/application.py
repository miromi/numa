from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseSchema

class ApplicationBase(BaseModel):
    name: str
    description: str
    repository_url: str
    status: Optional[str] = "created"
    owner: str
    app_id: str

class ApplicationCreate(ApplicationBase):
    development_task_id: int
    created_by: int
    
    class Config:
        # 确保验证在模型级别执行
        validate_assignment = True

class ApplicationInDB(BaseSchema):
    name: str
    description: str
    repository_url: Optional[str] = None
    status: Optional[str] = "created"
    owner: Optional[str] = None
    app_id: Optional[str] = None
    development_task_id: int
    created_by: int
    built_at: Optional[datetime] = None

# 用于API响应的模型，允许字段为None
Application = ApplicationInDB