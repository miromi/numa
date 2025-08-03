from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Task(BaseModel):
    """任务模型"""
    id: int
    title: str
    description: str
    status: str  # todo, in_progress, done
    assigned_to: Optional[int] = None
    code_branch: Optional[str] = None
    solution_id: int
    requirement_id: int
    application_id: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None