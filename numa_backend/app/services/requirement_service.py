from sqlalchemy.orm import Session
from app.models.requirement import Requirement as RequirementModel
from app.schemas.requirement import RequirementCreate

def create_requirement(db: Session, requirement: RequirementCreate):
    db_requirement = RequirementModel(**requirement.dict())
    db.add(db_requirement)
    db.commit()
    db.refresh(db_requirement)
    return db_requirement

def get_requirement(db: Session, requirement_id: int):
    return db.query(RequirementModel).filter(RequirementModel.id == requirement_id).first()

def get_requirements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(RequirementModel).offset(skip).limit(limit).all()