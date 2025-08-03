from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.models.base import BaseModel

class Application(BaseModel):
    __tablename__ = "applications"
    
    name = Column(String, index=True)
    description = Column(Text)
    repository_url = Column(String, unique=True)
    status = Column(String, default="created")  # created, building, built, deployed
    created_by = Column(Integer, ForeignKey("users.id"))
    owner = Column(String)  # 应用所有者
    app_id = Column(String, unique=True)  # 应用唯一标识符
    built_at = Column(DateTime(timezone=True), nullable=True)
    
    # 添加唯一性约束
    __table_args__ = (
        UniqueConstraint('name', name='uq_application_name'),
        UniqueConstraint('app_id', name='uq_application_app_id'),
        UniqueConstraint('repository_url', name='uq_application_repository_url'),
    )