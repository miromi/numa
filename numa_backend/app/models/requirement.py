from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.models.base import BaseModel

class Requirement(BaseModel):
    __tablename__ = "requirements"
    
    title = Column(String, index=True)
    description = Column(Text)
    status = Column(String, default="pending")  # pending, approved, rejected, implemented
    user_id = Column(Integer, ForeignKey("users.id"))
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=True)  # 可选的应用关联