from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.models.base import BaseModel

class Deployment(BaseModel):
    __tablename__ = "deployments"
    
    name = Column(String, index=True)
    description = Column(Text)
    development_task_id = Column(Integer, ForeignKey("development_tasks.id"))
    status = Column(String, default="pending")  # pending, in_progress, success, failed
    deployed_at = Column(DateTime(timezone=True), nullable=True)
    deployed_by = Column(Integer, ForeignKey("users.id"))