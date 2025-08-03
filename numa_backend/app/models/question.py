from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from app.models.base import BaseModel

class Question(BaseModel):
    __tablename__ = "questions"
    
    content = Column(Text, nullable=False)  # 问题内容
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)  # 关联的需求
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # 提问人
    answered_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # 回答人
    answer = Column(Text, nullable=True)  # 回答内容
    clarified = Column(Boolean, default=False)  # 是否已澄清
    clarified_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # 澄清人（必须是需求接受人）