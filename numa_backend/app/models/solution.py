from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.models.base import BaseModel

class Solution(BaseModel):
    __tablename__ = "solutions"
    
    title = Column(String, index=True)
    description = Column(Text)
    requirement_id = Column(Integer, ForeignKey("requirements.id"))
    status = Column(String, default="proposed")  # proposed, accepted, rejected