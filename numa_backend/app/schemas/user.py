from pydantic import BaseModel
from typing import Optional
from app.schemas.base import BaseSchema

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase, BaseSchema):
    pass