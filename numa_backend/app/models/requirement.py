from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from app.models.base import BaseModel

class Requirement(BaseModel):
    __tablename__ = "requirements"
    
    title = Column(String, index=True)
    description = Column(Text)
    status = Column(String, default="pending")  # pending, clarified, implemented
    user_id = Column(Integer, ForeignKey("users.id"))