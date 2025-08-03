from sqlalchemy import Column, Integer, String
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)