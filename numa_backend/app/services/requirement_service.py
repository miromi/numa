from sqlalchemy.orm import Session
from app.models.requirement import Requirement as RequirementModel
from app.models.user import User as UserModel
from app.models.application import Application as ApplicationModel
from app.schemas.requirement import RequirementCreate, RequirementUpdate
from app.services.question_service import check_all_questions_clarified
import uuid

def create_requirement(db: Session, requirement: RequirementCreate):
    # Check if the user exists
    user = db.query(UserModel).filter(UserModel.id == requirement.user_id).first()
    if not user:
        raise ValueError("User not found")
    
    # Check if application exists (if provided)
    if requirement.application_id:
        application = db.query(ApplicationModel).filter(ApplicationModel.id == requirement.application_id).first()
        if not application:
            raise ValueError("Application not found")
    
    db_requirement = RequirementModel(**requirement.dict())
    db.add(db_requirement)
    db.commit()
    db.refresh(db_requirement)
    return db_requirement

def get_requirement(db: Session, requirement_id: int):
    return db.query(RequirementModel).filter(RequirementModel.id == requirement_id).first()

def get_requirements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(RequirementModel).offset(skip).limit(limit).all()

def update_requirement(db: Session, requirement_id: int, requirement_update: RequirementUpdate):
    db_requirement = get_requirement(db, requirement_id)
    if db_requirement:
        # 如果需求已澄清，则不允许修改内容
        if db_requirement.clarified and requirement_update.description is not None:
            raise ValueError("已澄清的需求不允许修改内容")
        
        update_data = requirement_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_requirement, key, value)
        db.commit()
        db.refresh(db_requirement)
    return db_requirement

def update_requirement_status(db: Session, requirement_id: int, status: str):
    return update_requirement(db, requirement_id, RequirementUpdate(status=status))

def assign_requirement(db: Session, requirement_id: int, assigned_to: int):
    # Check if the assigned user exists
    user = db.query(UserModel).filter(UserModel.id == assigned_to).first()
    if not user:
        raise ValueError("Assigned user not found")
    
    # 更新需求状态为clarifying并设置接手人
    return update_requirement(
        db, 
        requirement_id, 
        RequirementUpdate(status="clarifying", assigned_to=assigned_to)
    )

def confirm_requirement(db: Session, requirement_id: int):
    # 确认需求澄清完毕，进入开发阶段
    return update_requirement_status(db, requirement_id, "confirmed")

def clarify_requirement(db: Session, requirement_id: int, clarified: bool = True):
    """标记需求为已澄清"""
    db_requirement = get_requirement(db, requirement_id)
    if not db_requirement:
        raise ValueError("需求未找到")
    
    # 检查是否所有问题都已澄清
    if clarified and not check_all_questions_clarified(db, requirement_id):
        raise ValueError("还有未澄清的问题，请先澄清所有问题")
    
    # 更新需求
    db_requirement.clarified = clarified
    db.commit()
    db.refresh(db_requirement)
    return db_requirement

def generate_branch_name(requirement_id: int, title: str) -> str:
    # 生成分支名称：req-{requirement_id}-{title_slug}
    slug = title.lower().replace(" ", "-")[:20]  # 限制长度
    return f"req-{requirement_id}-{slug}"

def generate_spec_document(db: Session, requirement_id: int):
    # 生成需求规范文档（简化版本，实际实现中可以集成AI）
    requirement = get_requirement(db, requirement_id)
    if not requirement:
        raise ValueError("Requirement not found")
    
    spec = f"""# 需求规范文档

## 需求标题
{requirement.title}

## 需求描述
{requirement.description}

## 自动生成的澄清问题
1. 请确认该需求的优先级是高、中还是低？
2. 该需求是否需要在特定时间点前完成？
3. 是否有其他相关的功能或需求需要考虑？

## 下一步行动
请回答以上问题，以便我们继续进行需求开发。
"""
    
    return spec