from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.models.base import BaseModel

class Application(BaseModel):
    __tablename__ = "applications"
    
    name = Column(String, index=True)
    description = Column(Text)
    repository_url = Column(String)
    status = Column(String, default="created")  # created, building, built, deployed
    development_task_id = Column(Integer, ForeignKey("development_tasks.id"))
    created_by = Column(Integer, ForeignKey("users.id"))
    built_at = Column(DateTime(timezone=True), nullable=True)