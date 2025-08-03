from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.models.base import BaseModel

class Requirement(BaseModel):
    __tablename__ = "requirements"
    
    title = Column(String, index=True)
    description = Column(Text)
    status = Column(String, default="pending")  # pending, clarifying, confirmed, in_progress, completed
    user_id = Column(Integer, ForeignKey("users.id"))
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=True)  # 可选的应用关联
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)  # 需求接手人
    branch_name = Column(String, nullable=True)  # 自动生成的分支名称
    spec_document = Column(Text, nullable=True)  # 自动生成的需求规范文档