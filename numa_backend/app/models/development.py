from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.models.base import BaseModel

class DevelopmentTask(BaseModel):
    __tablename__ = "development_tasks"
    
    title = Column(String, index=True)
    description = Column(Text)
    solution_id = Column(Integer, ForeignKey("solutions.id"))
    status = Column(String, default="todo")  # todo, in_progress, done
    assigned_to = Column(Integer, ForeignKey("users.id"))
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)