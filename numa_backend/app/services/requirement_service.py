from sqlalchemy.orm import Session
from app.models.requirement import Requirement as RequirementModel
from app.models.user import User as UserModel
from app.models.application import Application as ApplicationModel
from app.schemas.requirement import RequirementCreate

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

def update_requirement_status(db: Session, requirement_id: int, status: str):
    db_requirement = get_requirement(db, requirement_id)
    if db_requirement:
        db_requirement.status = status
        db.commit()
        db.refresh(db_requirement)
    return db_requirement