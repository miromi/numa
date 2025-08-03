from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseSchema

class ApplicationBase(BaseModel):
    name: str
    description: str
    repository_url: Optional[str] = None
    status: Optional[str] = "created"
    owner: Optional[str] = None
    app_id: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    development_task_id: int
    created_by: int
    repository_url: str  # 创建时必须提供仓库地址
    owner: str  # 创建时必须提供所有者
    app_id: str  # 创建时必须提供应用ID
    
    class Config:
        # 确保验证在模型级别执行
        validate_assignment = True

class Application(ApplicationBase, BaseSchema):
    development_task_id: int
    created_by: int
    built_at: Optional[datetime] = None