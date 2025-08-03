from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas.requirement import Requirement, RequirementCreate
from app.services.requirement_service import create_requirement, get_requirement, get_requirements
from app.core.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=Requirement)
def create_new_requirement(requirement: RequirementCreate, db: Session = Depends(get_db)):
    return create_requirement(db, requirement)

@router.get("/{requirement_id}", response_model=Requirement)
def read_requirement(requirement_id: int, db: Session = Depends(get_db)):
    db_requirement = get_requirement(db, requirement_id)
    if db_requirement is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return db_requirement

@router.get("/", response_model=List[Requirement])
def read_requirements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_requirements(db, skip=skip, limit=limit)