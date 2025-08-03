from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.models.base import BaseModel

class EventLog(BaseModel):
    __tablename__ = "event_logs"
    
    event_type = Column(String, nullable=False)  # 事件类型：question_created, question_answered, question_clarified
    description = Column(Text, nullable=False)  # 事件描述
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 操作用户
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=True)  # 关联的需求（可选）
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=True)  # 关联的问题（可选）