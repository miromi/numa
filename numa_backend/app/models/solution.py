from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from app.models.base import BaseModel

class Solution(BaseModel):
    __tablename__ = "solutions"
    
    title = Column(String, index=True)
    description = Column(Text)
    requirement_id = Column(Integer, ForeignKey("requirements.id"))
    application_id = Column(Integer, ForeignKey("applications.id"))  # 新增：与应用的关联关系
    status = Column(String, default="clarifying")  # clarifying, confirmed, implemented
    created_by = Column(Integer, ForeignKey("users.id"))  # 方案负责人（即需求接受人）
    clarified = Column(Boolean, default=False)  # 是否已澄清